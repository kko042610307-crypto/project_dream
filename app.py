import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import json
import os
import textwrap

# ==============================================================================
# 1. API 키 설정 (코드 내부 입력)
# ==============================================================================
UPSTAGE_API_KEY = "up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG"  # <--- 여기에 업스테이지 API 키를 입력하세요.

# Upstage Solar Client 초기화
client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1/solar"
)

# ==============================================================================
# 2. 폰트 로드 함수 (한글 깨짐 방지)
# ==============================================================================
def get_font(size=16):
    """운영체제별 한글 폰트를 검색하여 로드합니다."""
    font_paths = [
        "C:/Windows/Fonts/malgun.ttf",                     # Windows (맑은 고딕)
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf", # macOS (애플고딕)
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux (나눔고딕)
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ==============================================================================
# 3. LLM 처리 함수 (Upstage Solar Pro)
# ==============================================================================
def process_notes_with_solar(user_text, style, size):
    """업스테이지 LLM을 호출하여 입력된 수업 내용을 선택한 방식에 맞게 구조화합니다."""
    system_prompt = f"""
    당신은 수업 필기 및 학습 정리 전문 AI 도우미입니다.
    사용자가 입력한 수업 정리 내용을 바탕으로, 지정된 노트 필기 스타일('{style}')과 용지 크기('{size}')에 적합하도록 내용을 요약 및 구조화하세요.

    응답은 반드시 아래 JSON 형식으로만 출력해야 합니다 (추가적인 말은 하지 마세요):
    {{
        "title": "수업 주제/제목",
        "key_points": ["핵심 키워드 또는 질문 1", "핵심 키워드 또는 질문 2", "핵심 키워드 또는 질문 3"],
        "main_notes": ["상세 노트 내용 1", "상세 노트 내용 2", "상세 노트 내용 3"],
        "summary": "전체 내용을 한두 문장으로 요약한 설명",
        "explanation": "이 노트 템플릿이 작성된 구조 방식과 활용법에 대한 짧은 설명"
    }}
    """

    try:
        response = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"수업 정리 내용:\n{user_text}"}
            ],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        
        # JSON 추출
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(content)
    except Exception as e:
        st.error(f"Upstage API 처리 중 오류 발생: {e}")
        return None

# ==============================================================================
# 4. 노트 템플릿 이미지 생성 함수
# ==============================================================================
def draw_note_template(size_option, style_option, data):
    """구조화된 데이터를 바탕으로 실제 노트 템플릿 이미지를 시각적으로 그립니다."""
    # 노트 사이즈별 픽셀 해상도 설정
    size_map = {
        "A4": (800, 1131),
        "B5": (700, 990),
        "A5": (600, 848),
        "Letter": (800, 1035)
    }
    width, height = size_map.get(size_option, (800, 1131))
    
    # 캔버스 생성 (연한 아이보리 톤)
    img = Image.new("RGB", (width, height), color=(252, 252, 250))
    draw = ImageDraw.Draw(img)
    
    # 폰트 지정
    title_font = get_font(22)
    label_font = get_font(16)
    text_font = get_font(14)
    
    # 색상 정의
    border_color = (180, 190, 205)
    primary_color = (30, 50, 90)
    accent_bg = (235, 242, 250)
    text_color = (40, 40, 40)
    line_color = (220, 225, 230)
    
    # Outer Frame
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=border_color, width=2)
    
    # Header Area
    draw.rectangle([(30, 30), (width - 30, 100)], fill=accent_bg, outline=border_color)
    draw.text((45, 45), f"제목: {data.get('title', '수업 노트')}", fill=primary_color, font=title_font)
    draw.text((45, 75), f"규격: {size_option} | 필기 스타일: {style_option}", fill=(100, 100, 100), font=text_font)
    
    # Layout by Style
    if style_option == "코넬 노트 (Cornell)":
        summary_top = height - 180
        cue_width = int(width * 0.32)
        
        # Division Lines
        draw.line([(cue_width, 110), (cue_width, summary_top)], fill=border_color, width=2)
        draw.line([(30, summary_top), (width - 30, summary_top)], fill=border_color, width=2)
        
        # Labels
        draw.text((40, 115), "[ 핵심 단어 / 질문 ]", fill=primary_color, font=label_font)
        draw.text((cue_width + 15, 115), "[ 노트 필기 / 세부 내용 ]", fill=primary_color, font=label_font)
        draw.text((40, summary_top + 10), "[ 요약 (Summary) ]", fill=primary_color, font=label_font)
        
        # Draw Key Points (Left)
        y = 150
        for kp in data.get("key_points", []):
            lines = textwrap.wrap(f"• {kp}", width=18)
            for line in lines:
                draw.text((40, y), line, fill=text_color, font=text_font)
                y += 24
            y += 10
            
        # Draw Main Notes (Right)
        y = 150
        for note in data.get("main_notes", []):
            lines = textwrap.wrap(f"- {note}", width=45)
            for line in lines:
                draw.text((cue_width + 15, y), line, fill=text_color, font=text_font)
                y += 24
            y += 8
            
        # Draw Summary (Bottom)
        sum_lines = textwrap.wrap(data.get("summary", ""), width=65)
        sy = summary_top + 35
        for s_line in sum_lines:
            draw.text((40, sy), s_line, fill=text_color, font=text_font)
            sy += 22

    elif style_option == "3단 구획 (3-Column)":
        col_w = (width - 60) // 3
        draw.line([(30 + col_w, 110), (30 + col_w, height - 30)], fill=border_color, width=2)
        draw.line([(30 + col_w * 2, 110), (30 + col_w * 2, height - 30)], fill=border_color, width=2)
        
        sections = [
            ("1. 핵심 키워드", data.get("key_points", [])),
            ("2. 세부 내용", data.get("main_notes", [])),
            ("3. 요약 및 정리", [data.get("summary", "")])
        ]
        
        for idx, (col_title, col_content) in enumerate(sections):
            x_offset = 40 + (col_w * idx)
            draw.text((x_offset, 115), col_title, fill=primary_color, font=label_font)
            
            y = 150
            for item in col_content:
                lines = textwrap.wrap(f"• {item}", width=18)
                for line in lines:
                    draw.text((x_offset, y), line, fill=text_color, font=text_font)
                    y += 24
                y += 10

    else:  # 개요형 (Outline) / 박스형
        draw.text((40, 115), "[ 수업 개요 및 주요 내용 ]", fill=primary_color, font=label_font)
        
        y = 150
        for idx, note in enumerate(data.get("main_notes", []), 1):
            draw.rectangle([(40, y), (width - 40, y + 60)], outline=border_color, fill=(255, 255, 255))
            draw.text((50, y + 10), f"항목 {idx}", fill=primary_color, font=label_font)
            draw.text((50, y + 32), note, fill=text_color, font=text_font)
            y += 75
            
        # Summary Box
        draw.rectangle([(40, height - 150), (width - 40, height - 40)], outline=border_color, fill=accent_bg)
        draw.text((50, height - 140), "[ 전체 요약 ]", fill=primary_color, font=label_font)
        draw.text((50, height - 110), data.get("summary", ""), fill=text_color, font=text_font)

    return img

# ==============================================================================
# 5. Streamlit 메인 UI 구성
# ==============================================================================
st.set_page_config(page_title="AI 수업 노트 템플릿 생성기", layout="wide")

st.title("📝 AI 수업 노트 필기 템플릿 생성 서비스")
st.markdown("수업 정리 글을 입력하면 **Upstage AI**가 내용을 정리하고, 선택한 규격과 스타일의 **맞춤형 노트 필기 템플릿**을 생성해 드립니다.")

st.divider()

# 좌측: 고정 선택 입력 / 우측: 자연어 입력
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ 노트 옵션 선택")
    
    # 1. 고정 입력 1: 노트 필기 방식 선택
    style_option = st.selectbox(
        "선호하는 노트 필기 방식",
        ["코넬 노트 (Cornell)", "개요형 (Outline)", "3단 구획 (3-Column)"]
    )
    
    # 2. 고정 입력 2: 노트 사이즈 선택
    size_option = st.selectbox(
        "노트 사이즈",
        ["A4", "B5", "A5", "Letter"]
    )
    
    submit_btn = st.button("🚀 노트 템플릿 생성하기", use_container_width=True)

with col2:
    st.subheader("📖 수업 정리 내용 입력")
    # 자연어 입력 창
    user_notes = st.text_area(
        "수업 시간에 정리한 자연어 텍스트를 자유롭게 입력하세요:",
        height=280,
        placeholder="예시:\n오늘 인공지능 수업에서 파이썬 기초와 자료구조에 대해 배웠다.\n리스트는 순서가 있고 변경 가능한 배열 형태이며, 튜플은 순서는 있지만 수정이 불가능하다.\n딕셔너리는 Key-Value 구조로 빠른 탐색에 유용하다. 이 세 가지의 차이점을 파악하는 것이 중요하다."
    )

st.divider()

# 결과 출력 영역
if submit_btn:
    if not user_notes.strip():
        st.warning("수업 정리 내용을 입력해 주세요!")
    elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY":
        st.error("코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 업스테이지 API 키를 입력해 주세요.")
    else:
        with st.spinner("Upstage Solar LLM이 노트를 분석하고 템플릿을 생성 중입니다..."):
            # 1. LLM 구조화
            parsed_data = process_notes_with_solar(user_notes, style_option, size_option)
            
            if parsed_data:
                # 2. 이미지 생성
                template_img = draw_note_template(size_option, style_option, parsed_data)
                
                st.success("템플릿 생성이 완료되었습니다!")
                
                # 3. 최종 출력 (이미지 & 간단한 설명 글)
                out_col1, out_col2 = st.columns([1, 1])
                
                with out_col1:
                    st.subheader("🖼️ 생성된 노트 필기 템플릿")
                    st.image(template_img, caption=f"{size_option} / {style_option}", use_container_width=True)
                    
                with out_col2:
                    st.subheader("📋 노트 설명 및 요약 글")
                    st.markdown(f"### 📌 {parsed_data.get('title', '수업 제목')}")
                    
                    st.markdown("#### 💡 노트 구성 설명")
                    st.info(parsed_data.get("explanation", "요청하신 방식에 맞춰 노트를 구조화했습니다."))
                    
                    st.markdown("#### 📝 핵심 내용 요약")
                    st.write(parsed_data.get("summary", ""))
                    
                    st.markdown("#### 🔑 주요 키워드")
                    for kp in parsed_data.get("key_points", []):
                        st.markdown(f"- **{kp}**")
