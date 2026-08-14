import json
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ==============================================================================
# 1. API 키 설정 (코드 내부 고정)
# ==============================================================================
UPSTAGE_API_KEY = "up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG"  # 여기에 발급받으신 Upstage API Key를 입력하세요.

# Upstage Solar API 엔드포인트 설정
client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

# ==============================================================================
# 2. Streamlit UI 레이아웃 설정
# ==============================================================================
st.set_page_config(
    page_title="AI 맞춤형 수업 노트 생성기",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI 맞춤형 수업 노트 템플릿 생성기")
st.write("자연어로 작성한 수업 필기와 원하는 방식을 입력하면, Upstage Solar AI가 맞춤형 HTML/CSS 노트 템플릿을 디자인해 드립니다.")

st.divider()

# 좌/우 화면 분할
col_input, col_info = st.columns([1, 1])

with col_input:
    st.subheader("⚙️ 필기 옵션 및 내용 입력")
    
    # [고정 입력 1] 선호하는 노트 필기 방식
    note_style = st.selectbox(
        "📌 선호하는 노트 필기 방식",
        [
            "코넬 노트 (Cornell Notes - 핵심키워드 / 필기 / 요약 섹션)",
            "개요식 정리 (Outline Style - 위계구조 및 불릿포인트 중심)",
            "3분할 정리 (3-Column Style - 질문 / 내용 / 핵심 요약)",
            "Q&A 개념 정리 (Question & Answer Style)",
            "자유 요약 및 키워드 정리 (Freeform Summary)"
        ]
    )
    
    # [고정 입력 2] 노트 사이즈
    note_size = st.selectbox(
        "📐 노트 사이즈 / 규격",
        [
            "A4 (210 x 297 mm - 표준 문서 규격)",
            "B5 (176 x 250 mm - 일반 단권화 서식)",
            "Letter (215.9 x 279.4 mm)",
            "iPad / 태블릿 스크린 뷰 (16:9 가로 화면 맞춤)"
        ]
    )
    
    # [가변 입력] 자연어 수업 정리 내용
    class_notes = st.text_area(
        "✏️ 수업 정리 내용 (자연어)",
        height=250,
        placeholder="예시:\n오늘 데이터베이스 수업에서 정규화에 대해 배웠다.\n1정규형은 도메인이 원자값이어야 하고, 2정규형은 부분 함수 종속성을 제거해야 함.\n3정규형은 이행적 함수 종속성을 제거하는 것임. 주요 키워드는 기본키, 외래키, 완전 함수 종속..."
    )
    
    submit_btn = st.button("🚀 맞춤형 노트 템플릿 생성하기", use_container_width=True)

with col_info:
    st.subheader("💡 사용 안내")
    st.info(
        """
        **이 서비스는 어떻게 동작하나요?**
        1. **고정 옵션 선택**: 사용하실 노트 필기 양식과 규격을 선택합니다.
        2. **수업 내용 입력**: 수업 중 적어둔 막필기나 줄글 형태의 수업 정리를 자유롭게 작성합니다.
        3. **AI 처리**: Upstage의 Solar 모델이 내용을 구조화하여 최적의 레이아웃과 CSS 스타일링이 적용된 HTML 문서를 생성합니다.
        4. **결과 확인**: 생성된 노트를 화면에서 직접 확인하고 필요 시 HTML 파일로 저장할 수 있습니다.
        """
    )

# ==============================================================================
# 3. LLM 처리 및 결과 출력 로직
# ==============================================================================
if submit_btn:
    if not class_notes.strip():
        st.warning("수업 정리 내용을 입력해 주세요!")
    elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
        st.error("코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 Upstage API 키를 넣어주세요!")
    else:
        with st.spinner("Upstage Solar AI가 수업 내용을 분석하여 최적의 노트 템플릿을 제작 중입니다..."):
            try:
                # Prompt 구성
                prompt = f"""
[사용자 입력 정보]
1. 필기 양식 스타일: {note_style}
2. 노트 규격: {note_size}
3. 수업 정리 내용:
{class_notes}

[지시 사항]
- 사용자가 입력한 수업 정리 내용을 바탕으로, 지정된 필기 스타일과 규격에 맞는 고품질의 HTML/CSS 노트를 제작하세요.
- HTML 내부 `<style>` 태그에 CSS를 통합하여 완성된 단일 HTML 문서를 생성하세요.
- 눈이 편안한 깔끔한 색상 팔레트, 가독성 높은 폰트(Noto Sans KR 등), 여백 및 경계선 구분을 적용하세요.
- 선택된 노트 규격 비율 및 노트 필기 방식의 구조적 특징이 디자인에 명확히 반영되어야 합니다.

[응답 형식]
반드시 유효한 JSON 형식으로만 응답하세요. 다른 부연 설명이나 마크다운 코드 블록(```json 등)은 절대 작성하지 마세요.

{{
  "explanation": "작성된 노트 템플릿의 레이아웃 구성 및 활용법에 대한 2-3줄의 간단한 설명글",
  "html_code": "<!DOCTYPE html><html><head><style>...</style></head><body>...</body></html>"
}}
"""

                # Upstage Solar API 호출
                response = client.chat.completions.create(
                    model="solar-pro",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert UI/UX designer and educational content structure specialist. Always output valid JSON only."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3
                )

                # 응답 처리 및 JSON 파싱
                raw_response = response.choices[0].message.content.strip()
                
                # 마크다운 래핑 제거 예외 처리
                if raw_response.startswith("```json"):
                    raw_response = raw_response[7:]
                if raw_response.startswith("```"):
                    raw_response = raw_response[3:]
                if raw_response.endswith("```"):
                    raw_response = raw_response[:-3]
                
                data = json.loads(raw_response.strip())
                explanation = data.get("explanation", "노트 생성 결과입니다.")
                html_code = data.get("html_code", "")

                st.success("✨ 맞춤형 노트 템플릿 생성이 완료되었습니다!")
                
                st.divider()
                
                # 1. 간단한 설명 글 출력
                st.subheader("📋 노트 정리 안내")
                st.markdown(explanation)
                
                st.space = 10
                
                # 2. HTML/CSS 시각적 렌더링 출력
                st.subheader("🎨 맞춤형 노트 템플릿 미리보기")
                components.html(html_code, height=850, scrolling=True)

                # 3. HTML 소스 코드 및 다운로드 버튼 제공
                with st.expander("📄 HTML / CSS 코드 보기 및 다운로드"):
                    st.code(html_code, language="html")
                    st.download_button(
                        label="💾 HTML 문서로 다운로드",
                        data=html_code,
                        file_name="note_template.html",
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"처리 중 오류가 발생했습니다: {e}")
