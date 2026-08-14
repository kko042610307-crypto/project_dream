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
    page_title="AI 맞춤형 빈 노트 서식 생성기",
    page_icon="📐",
    layout="wide"
)

st.title("📐 AI 맞춤형 빈 노트 템플릿 생성기")
st.write("수업 정리 주제를 입력하면, 처음부터 끝까지 직접 필기하며 정리할 수 있는 **맞춤형 빈 노트 양식(HTML/CSS)**을 디자인해 드립니다.")

st.divider()

# 좌/우 화면 분할
col_input, col_info = st.columns([1, 1])

with col_input:
    st.subheader("⚙️ 필기 옵션 및 주제 입력")
    
    # [고정 입력 1] 선호하는 노트 필기 방식
    note_style = st.selectbox(
        "📌 선호하는 노트 필기 방식",
        [
            "코넬 노트 (Cornell Notes - 핵심키워드 컬럼 / 넓은 필기 영역 / 하단 요약 상자)",
            "줄글 노트 (Lined / Ruled Notebook - 세련된 줄눈 간격 및 섹션 구분)",
            "그리드/모눈 노트 (Grid Paper - 개념 정리 및 도표 작성에 유용한 격자 서식)",
            "3분할 노트 (3-Column Layout - 개념 / 상세 내용 / 개인 노트 영역)",
            "Q&A 질문 노트 (Question & Answer Layout - 질문 상자 및 답변 필기 공간)",
            "구조화 섹션 노트 (Sectioned Layout - 주제별 구분 박스 및 필기 공간)"
        ]
    )
    
    # [고정 입력 2] 노트 사이즈
    note_size = st.selectbox(
        "📐 노트 사이즈 / 규격",
        [
            "A4 (210 x 297 mm - 표준 인쇄 규격)",
            "B5 (176 x 250 mm - 일반 단권화 서식)",
            "Letter (215.9 x 279.4 mm)",
            "iPad / 태블릿 스크린 뷰 (16:9 가로 화면 맞춤)"
        ]
    )
    
    # [가변 입력] 자연어 수업 정리 내용
    class_notes = st.text_area(
        "📝 노트에 반영할 수업 정리 / 주제 개요",
        height=250,
        placeholder="예시:\n오늘 데이터베이스 수업에서 정규화에 대해 배웠다.\n1정규형(도메인 원자값), 2정규형(부분 함수 종속성 제거), 3정규형(이행적 함수 종속성 제거)에 대한 내용을 구분해서 작성하고 싶어. 하단에는 관련 핵심 키워드 정리 공간을 만들어줘."
    )
    
    submit_btn = st.button("🚀 맞춤형 빈 노트 서식 생성하기", use_container_width=True)

with col_info:
    st.subheader("💡 빈 노트 서식 활용 안내")
    st.info(
        """
        **이 서비스는 어떻게 동작하나요?**
        1. **완전 공백 양식 설계**: 입력된 수업 주제 구조에 맞춰 **내용이 완전히 비어있는 필기용 틀(상자, 줄글, 모눈, 섹션)**을 디자인합니다.
        2. **맞춤형 섹션 구성**: 사용자가 작성한 목차와 주제에 적합하도록 타이틀, 섹션 헤더, 필기 영역 크기가 레이아웃에 반영됩니다.
        3. **디지털 & 오프라인 겸용**: HTML 파일로 다운로드하여 태블릿 필기 앱(굿노트, 노타빌리티 등)의 서식으로 불러오거나, 인쇄하여 직접 손필기할 수 있습니다.
        """
    )

# ==============================================================================
# 3. LLM 처리 및 결과 출력 로직
# ==============================================================================
if submit_btn:
    if not class_notes.strip():
        st.warning("노트에 반영할 수업 정리/주제 내용을 입력해 주세요!")
    elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
        st.error("코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 Upstage API 키를 입력해 주세요!")
    else:
        with st.spinner("Upstage Solar AI가 직접 필기할 수 있는 맞춤형 빈 노트 양식을 디자인 중입니다..."):
            try:
                # Prompt 구성 (내용을 완전히 비우고 양식/틀만 생성하도록 강조)
                prompt = f"""
[사용자 입력 정보]
1. 필기 양식 스타일: {note_style}
2. 노트 규격: {note_size}
3. 수업 주제 및 구조 요구사항:
{class_notes}

[지시 사항]
- 입력된 수업 주제 및 요청 구조를 바탕으로, 사용자가 처음부터 끝까지 **직접 내용을 손필기하거나 작성할 수 있는 '완전한 빈 노트 양식(Blank Note Template)'**을 생성하세요.
- **주의사항 (절대 준수)**:
  1. 본문 영역에는 설명글, 요약 텍스트, 완료된 내용, 또는 빈칸 문제(`_____`)를 절대 채워 넣지 마세요.
  2. 사용자가 직접 써 내려갈 수 있는 **완전한 공백 영역(줄글 선, 빈 상자/입력 영역, 격자 패턴, 넉넉한 여백)**으로 디자인해야 합니다.
  3. 사용자가 입력한 내용을 참고하여 **'메인 제목', '주제별 구분 영역 제목(Section Header)', '키워드 단서 영역', '하단 빈 요약 상자'** 등 서식의 틀(Structure)만 세련되게 배치하세요.
- HTML 내부 `<style>` 태그에 CSS를 통합하여 완성된 단일 HTML 문서를 생성하세요.
- 선택된 노트 규격 비율 및 필기 방식의 레이아웃(줄간격, 필기 박스 테두리, 은은한 구분선 색상 등)이 가독성 높게 디자인되어야 합니다.

[응답 형식]
반드시 유효한 JSON 형식으로만 응답하세요. 부연 설명이나 마크다운 코드 블록(```json 등)은 작성하지 마세요.

{{
  "explanation": "디자인된 빈 노트 서식의 레이아웃 구조와 필기 활용 팁에 대한 2-3줄의 간단한 설명글",
  "html_code": "<!DOCTYPE html><html><head><style>...</style></head><body>...</body></html>"
}}
"""

                # Upstage Solar API 호출
                response = client.chat.completions.create(
                    model="solar-pro",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional stationery and notebook layout designer specializing in HTML/CSS printable templates. Always output valid JSON only."
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
                explanation = data.get("explanation", "맞춤형 빈 노트 템플릿이 생성되었습니다.")
                html_code = data.get("html_code", "")

                st.success("✨ 맞춤형 빈 노트 서식 생성이 완료되었습니다!")
                
                st.divider()
                
                # 1. 간단한 설명 글 출력
                st.subheader("📋 노트 레이아웃 및 활용 가이드")
                st.markdown(explanation)
                
                # 2. HTML/CSS 시각적 렌더링 출력
                st.subheader("🎨 생성된 빈 노트 템플릿 미리보기")
                components.html(html_code, height=850, scrolling=True)

                # 3. HTML 소스 코드 및 다운로드 버튼 제공
                with st.expander("📄 HTML / CSS 코드 확인 및 다운로드"):
                    st.code(html_code, language="html")
                    st.download_button(
                        label="💾 빈 노트 양식 다운로드 (인쇄/태블릿 필기용)",
                        data=html_code,
                        file_name="blank_note_template.html",
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"처리 중 오류가 발생했습니다: {e}")
