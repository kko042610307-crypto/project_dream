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
    page_title="주제 맞춤형 학습 템플릿 생성기",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 주제 맞춤형 학습 템플릿 생성기")
st.write("학습할 내용을 입력하면, AI가 내용의 구조(비교·분류·과정 등)를 분석하여 **직접 채워 넣으며 공부할 수 있는 맞춤형 복습 템플릿**을 만들어 드립니다.")

st.divider()

# ==============================================================================
# 3. 입력 및 결과 화면 레이아웃
# ==============================================================================
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("⚙️ 학습 템플릿 설정")
    
    template_type = st.selectbox(
        "📌 템플릿 표현 양식",
        [
            "🤖 AI 자동 추천 (학습 내용 구조에 맞는 최적의 레이아웃 자동 생성)",
            "📊 비교/대조 표 양식 (관점, 이론, 개념 간 차이점 한눈에 비교)",
            "🌳 위계/분류 구조 양식 (3역 6계, 분류 체계, 마인드맵형 다이어그램)",
            "🔄 과정/순서 흐름도 양식 (시대순, 실험 절차, 인과관계 단계별 정리)",
            "📌 코넬 & 개념 인출 양식 (핵심 용어 정의 및 빈칸 채우기 중심)"
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
        "✍️ 학습할 내용 / 수업 요약",
        height=280,
        placeholder="예시 1:\n생명과학 시간 생물 분류 체계 (3역 6계: 세균역, 고세균역, 진핵생물역과 6개 계의 특징을 분류하여 정리할 수 있는 표나 마인드맵 서식을 만들어줘.)\n\n예시 2:\n사회문화 - 사회를 바라보는 관점 (기능론, 갈등론, 상징적 상호작용론의 핵심 개념, 사회관, 한계점을 한눈에 비교해서 적을 수 있는 표 양식을 만들어줘.)"
    )
    
    submit_btn = st.button("🚀 맞춤형 학습 템플릿 생성하기", use_container_width=True)

with col_output:
    st.subheader("🖼️ 생성된 학습 템플릿 미리보기")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("학습할 내용을 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 Upstage API 키를 입력해 주세요.")
        else:
            with st.spinner("AI가 학습 내용의 구조를 분석하여 최적의 복습 서식을 디자인 중입니다..."):
                try:
                    # 핵심 프롬프트: '완성된 요약본'이 아닌 '구조화된 채우기용 학습 양식' 생성
                    prompt = f"""
[사용자 입력 정보]
1. 선호 템플릿 표현 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습할 수업 내용:
{class_notes}

[템플릿 제작 핵심 규칙 (필수 준수)]
1. **완성된 정답 요약본을 작성하지 마세요.**
2. 입력된 학습 내용의 **구조적 특성**을 분석하여 맞춤형 서식을 만드세요:
   - **비교/대조 개념인 경우**: 비교 기준(개념, 특징, 장단점 등)이 들어간 '비교 표(Table)' 형태로 틀을 만들고, 내부 셀은 작성할 수 있도록 비워두거나 힌트/빈칸 `[       ]`을 배치하세요.
   - **분류/위계 체계인 경우 (예: 3역 6계 등)**: 마인드맵 스타일의 계통도, 트리 구조 Box, 혹은 단계별 분류 표로 틀을 만드세요.
   - **과정/순서인 경우**: Flowchart 형태의 연결된 박스를 배치하세요.
3. 학습자가 직접 손필기하거나 타이핑하며 채워갈 수 있도록 **충분한 작성 공간(빈 셀, 빈 상자, 밑줄, 점선)**을 마련하세요.

[페이지 레이아웃 및 CSS 규칙]
- 선택된 규격({note_size})에 완벽히 맞추어 디자인하세요:
  * A4: width: 210mm; min-height: 297mm;
  * B5: width: 176mm; min-height: 250mm;
  * Letter: width: 215.9mm; min-height: 279.4mm;
  * iPad: width: 100%; aspect-ratio: 16/9; max-width: 1024px;
- 내용이 길어 2장 이상 필요 시, 반드시 개별 `<div class="page">...</div>` 태그로 구분하세요.
- CSS 스타일 적용 예시:
  ```css
  body {{
      background-color: #f0f0f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
      padding: 20px;
      margin: 0;
      font-family: 'Noto Sans KR', sans-serif;
  }}
  .page {{
      background: white;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
      box-sizing: border-box;
      padding: 15mm;
      break-after: page;
      page-break-after: always;
  }}
  table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
  }}
  th, td {{
      border: 1px solid #cbd5e1;
      padding: 12px;
      text-align: center;
  }}
  th {{
      background-color: #f1f5f9;
      font-weight: bold;
  }}
  .diagram-box {{
      border: 2px dashed #94a3b8;
      border-radius: 8px;
      padding: 15px;
      background-color: #fafafa;
  }}
