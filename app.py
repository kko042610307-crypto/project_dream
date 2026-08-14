import json
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ==============================================================================
# 1. API 키 설정 (코드 내부 고정)
# ==============================================================================
UPSTAGE_API_KEY = "up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG"  # 여기에 발급받으신 Upstage API Key를 입력하세요.

client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

# ==============================================================================
# 2. Page Config
# ==============================================================================
st.set_page_config(
    page_title="AI 맞춤형 빈 노트 템플릿 생성기",
    page_icon="📝",
    layout="wide"
)

st.title("📝 AI 맞춤형 빈 노트 템플릿 생성기")

st.divider()

# ==============================================================================
# 3. 입력 및 결과 화면 레이아웃 (2열 구성)
# ==============================================================================
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("⚙️ 노트 설정")
    
    note_style = st.selectbox(
        "📌 필기 양식 스타일",
        [
            "코넬 노트 (Cornell Notes - 키워드 / 필기 / 하단 요약)",
            "줄글 노트 (Lined Notebook - 세련된 줄눈 간격)",
            "모눈/격자 노트 (Grid Paper - 개념 및 도표 정리용)",
            "3분할 노트 (3-Column Layout - 개념 / 상세 / 노트)",
            "Q&A 노트 (Question & Answer Layout - 질문 / 답변 상자)",
            "구조화 섹션 노트 (Sectioned Layout - 주제별 구분 박스)"
        ]
    )
    
    note_size = st.selectbox(
        "📐 노트 규격",
        [
            "A4 (210mm x 297mm)",
            "B5 (176mm x 250mm)",
            "Letter (215.9mm x 279.4mm)",
            "iPad (16:9 가로 스크린)"
        ]
    )
    
    class_notes = st.text_area(
        "✍️ 수업 주제 및 노트 구조 요청",
        height=250,
        placeholder="예시:\n오늘 데이터베이스 수업에서 정규화에 대해 배웠어.\n1정규형, 2정규형, 3정규형을 각각 정리할 수 있는 빈 박스를 만들어주고, 하단에는 핵심 키워드 정리용 노트 칸을 만들어줘."
    )
    
    submit_btn = st.button("🚀 빈 노트 템플릿 생성하기", use_container_width=True)

with col_output:
    st.subheader("🖼️ 노트 미리보기")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("수업 주제 및 구조 요청을 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 Upstage API 키를 입력해 주세요.")
        else:
            with st.spinner("선택한 규격에 맞춰 장 단위 빈 노트 템플릿을 생성 중입니다..."):
                try:
                    # 정확한 규격 및 장 단위 분할을 요구하는 프롬프트
                    prompt = f"""
[사용자 입력 정보]
1. 필기 양식 스타일: {note_style}
2. 노트 규격: {note_size}
3. 수업 주제 및 구조 요구사항:
{class_notes}

[필수 CSS 및 페이지 레이아웃 지시사항]
- 선택된 노트 규격({note_size})의 실제 물리적 크기/비율에 정확히 맞추어 스타일링하세요.
  * A4: width: 210mm; min-height: 297mm;
  * B5: width: 176mm; min-height: 250mm;
  * Letter: width: 215.9mm; min-height: 279.4mm;
  * iPad: width: 100%; aspect-ratio: 16/9; max-width: 1024px;
- **페이지 장 단위 구성 규칙**:
  1. 전체 노트를 여러 장으로 구성할 수 있도록 **각 페이지는 반드시 `<div class="page">...</div>` 태그로 개별 작성**해야 합니다.
  2. 요구사항 양이 많아 2장 이상이 필요한 경우, 반드시 `<div class="page">`를 여러 개 작성하여 장 단위로 나누어지게 만드세요.
  3. CSS에 아래 페이지 스펙을 반드시 적용하세요:
     ```css
     body {{
         background-color: #f0f0f0;
         display: flex;
         flex-direction: column;
         align-items: center;
         gap: 20px;
         padding: 20px;
         margin: 0;
     }}
     .page {{
         background: white;
         box-shadow: 0 4px 10px rgba(0,0,0,0.15);
         box-sizing: border-box;
         padding: 20mm;
         break-after: page;
         page-break-after: always;
     }}
     ```
- **완전 공백 양식 준수**: 본문에는 작성된 해설, 요약 텍스트, 빈칸 문제(`_____`)를 넣지 말고, 직접 손필기할 수 있는 공백, 상자, 줄글 라인, 표 틀만 디자인하세요.

[응답 형식]
반드시 유효한 JSON 형식으로만 응답하세요. 마크다운 코드 블록(```json 등)이나 기타 텍스트는 절대 포함하지 마세요.

{{
  "html_code": "<!DOCTYPE html><html><head><style>...</style></head><body>...</body></html>"
}}
"""

                    # Upstage Solar API 호출
                    response = client.chat.completions.create(
                        model="solar-pro",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a professional printable HTML/CSS notebook layout designer. Always respond with valid JSON containing only the 'html_code' field."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.2
                    )

                    # JSON 파싱 및 예외 처리
                    raw_response = response.choices[0].message.content.strip()
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    if raw_response.startswith("```"):
                        raw_response = raw_response[3:]
                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    data = json.loads(raw_response.strip())
                    html_code = data.get("html_code", "")

                    # 1. 시각적 미리보기 (장 단위로 구분되어 렌더링됨)
                    components.html(html_code, height=800, scrolling=True)

                    # 2. 다운로드 버튼
                    st.download_button(
                        label="💾 HTML 노트 템플릿 다운로드",
                        data=html_code,
                        file_name="note_template.html",
                        mime="text/html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
