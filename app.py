import json
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ==============================================================================
# 1. API 키 설정 (코드 내부 고정)
# ==============================================================================
UPSTAGE_API_KEY = "up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG"  # 발급받으신 Upstage API Key를 입력하세요.

client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

# ==============================================================================
# 2. Page Config
# ==============================================================================
st.set_page_config(
    page_title="주제 맞춤형 무지 학습 틀 생성기",
    page_icon="📝",
    layout="wide"
)

st.title("📝 주제 맞춤형 무지 학습 템플릿 생성기")

st.divider()

# ==============================================================================
# 3. 입력 및 결과 화면 레이아웃 (2열 구성)
# ==============================================================================
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("⚙️ 템플릿 설정")
    
    template_type = st.selectbox(
        "📌 템플릿 구조 양식",
        [
            "🤖 AI 자동 구조화 (학습 주제에 맞는 최적의 무지 틀 자동 생성)",
            "📊 무지 비교 표 (관점·이론·개념 비교용 공백 표)",
            "🌳 무지 위계/분류 박스 (3역 6계, 분류 체계용 빈 마인드맵/상자)",
            "🔄 무지 과정/흐름도 (순서, 실험 절차용 공백 화살표 상자)",
            "📌 무지 코넬/구획 서식 (주제별 섹션 및 하단 공백 요약란)"
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
        "✍️ 학습할 주제 및 서식 요구사항",
        height=280,
        placeholder="예시 1:\n생명과학 3역 6계 분류 체계 (3역과 6계를 나누어 정리할 수 있는 공백 마인드맵이나 분류 표 틀만 만들어줘.)\n\n예시 2:\n사회문화 사회를 바라보는 관점 (기능론, 갈등론, 상징적 상호작용론을 비교할 수 있는 항목별 완전 공백 비교 표를 만들어줘.)"
    )
    
    submit_btn = st.button("🚀 무지 학습 템플릿 생성하기", use_container_width=True)

with col_output:
    st.subheader("🖼️ 생성된 템플릿 미리보기")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("학습 주제를 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("코드 상단의 UPSTAGE_API_KEY 변수에 실제 Upstage API 키를 입력해 주세요.")
        else:
            with st.spinner("학습 주제에 최적화된 무지 서식 틀을 디자인 중입니다..."):
                try:
                    # 안전한 문자열 템플릿 (.format 활용)
                    prompt_template = """
[사용자 입력 정보]
1. 선호 템플릿 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습 주제 및 요구사항:
{class_notes}

[템플릿 제작 절대 규칙 (100% 무지 서식)]
1. **본문 내부 공간은 100% 완전히 비어있는 무지(공백) 상태여야 합니다.**
2. AI가 임의로 작성한 요약글, 해설, 키워드, 빈칸 문제(`_____`) 등을 본문 상자나 표 셀 안에 절대 집어넣지 마세요.
3. 입력된 주제를 바탕으로 **'틀(Structure)'**만 생성하세요:
   - 비교 주제: 행/열 헤더(예: 구분, 기능론, 갈등론 등)만 작성하고 내용 셀은 깨끗한 빈칸/공백 표로 생성
   - 분류/위계 주제: 상위 구조 타이틀만 표시하고, 세부 분류 공간은 비어있는 테두리 박스/마인드맵 형태로 생성
   - 과정/순서 주제: 단계 제목만 표시하고 세부 필기 공간은 비어있는 연결 상자로 생성
4. 사용자가 직접 손필기하거나 타이핑하며 모든 내용을 처음부터 채울 수 있도록 넉넉한 공백을 확보하세요.

[페이지 레이아웃 및 CSS 규칙]
- 선택된 규격({note_size})의 실제 치수에 정확히 맞춰 작성하세요:
  * A4: width: 210mm; min-height: 297mm;
  * B5: width: 176mm; min-height: 250mm;
  * Letter: width: 215.9mm; min-height: 279.4mm;
  * iPad: width: 100%; aspect-ratio: 16/9; max-width: 1024px;
- 내용이 길어 2장 이상 필요 시, 반드시 개별 <div class="page">...</div> 태그로 분할하세요.
- CSS 가이드:
  body는 flex column, align-items center, background #f0f0f0로 설정하고,
  .page는 background white, box-shadow, padding 15mm, break-after: page로 지정하세요.
  표 셀, 마인드맵 박스, 필기 구역 테두리는 은은한 색상(#cbd5e1 등)으로 깔끔하게 디테일을 더하세요.

[응답 형식]
반드시 유효한 JSON 형식으로만 응답하세요. 마크다운 코드 블록이나 기타 텍스트는 절대 포함하지 마세요.

"html_code": "<!DOCTYPE html><html><head><style>...</style></head><body>...</body></html>"
"""

                    prompt = prompt_template.format(
                        template_type=template_type,
                        note_size=note_size,
                        class_notes=class_notes
                    )

                    # Upstage Solar API 호출
                    response = client.chat.completions.create(
                        model="solar-pro",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an expert educational template designer. You create clean, elegant HTML/CSS blank worksheets (completely empty content boxes/tables) tailored to study topics. Always return valid JSON with only the 'html_code' field."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.2
                    )

                    # JSON 파싱 및 파싱 오류 예외 처리
                    raw_response = response.choices[0].message.content.strip()
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    if raw_response.startswith("```"):
                        raw_response = raw_response[3:]
                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    data = json.loads(raw_response.strip())
                    html_code = data.get("html_code", "")

                    # 1. 시각적 미리보기 (장 단위 구분)
                    components.html(html_code, height=800, scrolling=True)

                    # 2. 다운로드 버튼
                    st.download_button(
                        label="💾 무지 템플릿 다운로드 (HTML)",
                        data=html_code,
                        file_name="blank_study_template.html",
                        mime="text/html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"템플릿 생성 중 오류가 발생했습니다: {e}")
