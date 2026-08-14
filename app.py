import json
import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# ==============================================================================
# 1. API 키 설정 (코드 내부 고정)
# ==============================================================================
UPSTAGE_API_KEY = "up_Y7OKHBUB2q7pi7C4E1ILIWItBAUOG"  # 실제 발급받으신 Upstage API Key를 입력하세요.

client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

# ==============================================================================
# 2. Page Config & Custom CSS (UI 디자인)
# ==============================================================================
st.set_page_config(
    page_title="AI 맞춤형 학습 템플릿 생성기",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI Styling
st.markdown("""
<style>
    /* 전체 배경 설정 */
    .main { background-color: #f8fafc; }
    
    /* 히어로 헤더 디자인 */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.15);
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; color: #f8fafc; }
    .hero-subtitle { font-size: 1rem; color: #94a3b8; line-height: 1.5; }
    
    /* 생성 버튼 스타일링 */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# 히어로 헤더 출력
st.markdown("""
<div class="hero-container">
    <div class="hero-title">✨ AI 맞춤형 100% 무지 학습 템플릿 생성기</div>
    <div class="hero-subtitle">
        개념 설명이나 힌트를 모두 배제하고 <b>오직 사용자가 직접 채워 넣을 수 있는 100% 공백 필기 틀</b>을 만듭니다.<br>
        표 문법 자동 검증 및 A4 장 단위 자동 분할 기능이 기본 적용되어 있습니다.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. 입력 및 미리보기 레이아웃
# ==============================================================================
col_config, col_view = st.columns([1, 1.3], gap="large")

with col_config:
    st.subheader("⚙️ 서식 설정")
    
    template_type = st.selectbox(
        "📌 템플릿 구조 유형",
        [
            "🤖 AI 자동 구조화 (주제에 맞는 최적 서식)",
            "📊 무지 비교 표 (개념/이론/관점 비교용)",
            "🌳 무지 위계/분류 상자 (계통도 및 분류용)",
            "🔄 무지 흐름도 (단계/순서/인과관계용)",
            "📌 무지 코넬 서식 (섹션 구분 + 요약란)"
        ]
    )
    
    note_size = st.selectbox(
        "📐 노트 용지 규격",
        [
            "A4 (210mm x 297mm)",
            "B5 (176mm x 250mm)",
            "Letter (215.9mm x 279.4mm)",
            "iPad Screen (16:9)"
        ]
    )
    
    class_notes = st.text_area(
        "✍️ 학습 주제 및 구성 요구사항",
        height=300,
        placeholder="예시:\n인공지능, 머신러닝, 딥러닝 개념 정리 표와 머신러닝 학습 유형(지도/비지도/강화학습) 비교 표를 만들어주고, 과적합 해결 방안과 K-Means 단계별 정리 상자 틀을 만들어줘."
    )
    
    submit_btn = st.button("🚀 100% 무지 템플릿 생성", use_container_width=True)

with col_view:
    st.subheader("🖼️ 템플릿 미리보기 (장 단위)")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("⚠️ 학습 주제를 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("⚠️ 코드 상단의 UPSTAGE_API_KEY 변수에 실제 API 키를 입력해 주세요.")
        else:
            with st.spinner("개념 설명을 모두 지우고 순수 필기용 공백 틀을 제작 중입니다..."):
                try:
                    # 퓨샷(Few-Shot) 예시를 통한 100% 공백 셀 보장 프롬프트
                    prompt_template = """
[사용자 입력 정보]
1. 템플릿 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습 주제:
{class_notes}

[절대 규칙: 본문 설명/해설/특징 100% 제거 및 빈 셀 생성]
1. 당신은 '답안지'가 아닌 '공백 시험지/노트 서식'을 만드는 생성기입니다.
2. 각 행의 구분명(예: 지도학습, 비지도학습)을 제외하고, 특징/설명/사례/원인/해결책 등 내용이 작성되는 모든 셀은 반드시 `<td></td>` 형태로 비워두어야 합니다.

[작성 예시 (FEW-SHOT EXAMPLES)]
❌ 잘못된 작성 방식 (절대 금지!):
<tr>
  <td>지도학습</td>
  <td>레이블(정답) 제공 및 스팸 메일 분류에 활용</td>
</tr>

✅ 올바른 작성 방식 (필수 준수!):
<tr>
  <td>지도학습</td>
  <td></td>
  <td></td>
</tr>

[HTML 표 문법 및 페이지 분할 규칙]
1. 모든 표(table)의 <th> 개수와 각 <tr> 안의 <td> 개수는 완벽히 일치해야 합니다.
2. 한 개 페이지(<div class="page">)에 너무 많은 요소가 들어가 인쇄 시 잘리지 않도록 적절히 2~3개의 <div class="page">로 분할하세요.

[HTML5/JS 템플릿 구조]
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ margin: 0; background-color: #cbd5e1; font-family: 'Noto Sans KR', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }}
  .nav-bar {{ position: sticky; top: 0; z-index: 1000; width: 100%; background: #0f172a; color: white; padding: 12px 0; display: flex; justify-content: center; align-items: center; gap: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
  .nav-btn {{ background: #2563eb; color: white; border: none; padding: 8px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s; }}
  .nav-btn:disabled {{ background: #64748b; cursor: not-allowed; opacity: 0.5; }}
  .page-num {{ font-size: 15px; font-weight: bold; color: #f8fafc; }}
  .page-wrapper {{ padding: 25px 0; display: flex; justify-content: center; width: 100%; }}
  .page {{ display: none; background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.15); box-sizing: border-box; padding: 20mm; border-radius: 4px; width: 210mm; min-height: 297mm; }}
  .page.active {{ display: block; }}
  .section-title {{ font-size: 20px; font-weight: bold; color: #0f172a; border-bottom: 2px solid #2563eb; padding-bottom: 8px; margin: 10px 0 18px 0; }}
  .sub-title {{ font-weight: bold; color: #334155; margin: 14px 0 8px 0; font-size: 15px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }}
  th {{ background-color: #f1f5f9; font-weight: bold; color: #1e293b; text-align: center; border: 1px solid #cbd5e1; padding: 10px; font-size: 14px; }}
  td {{ border: 1px solid #cbd5e1; padding: 10px; height: 50px; vertical-align: top; }}
  .blank-box {{ border: 1px dashed #94a3b8; border-radius: 6px; min-height: 100px; background-color: #fafafa; margin-bottom: 18px; }}
  @media print {{
    .nav-bar {{ display: none; }}
    .page {{ display: block !important; break-after: page; box-shadow: none; padding: 0; }}
    body {{ background: white; }}
  }}
</style>
</head>
<body>
<div class="nav-bar">
  <button class="nav-btn" id="prevBtn" onclick="prevPage()">◀ 이전 페이지</button>
  <span class="page-num" id="pageIndicator">1 / 1</span>
  <button class="nav-btn" id="nextBtn" onclick="nextPage()">다음 페이지 ▶</button>
</div>
<div class="page-wrapper">
  <!-- 페이지 1 -->
  <div class="page active">
     <!-- 1페이지 올바른 HTML 표 (설명 셀은 반드시 <td></td>로만 작성) -->
  </div>
  <!-- 분량이 넘치거나 주제가 바뀌면 페이지 2, 3으로 분할 -->
</div>
<script>
  let currentPage = 0;
  const pages = document.querySelectorAll('.page');
  const pageIndicator = document.getElementById('pageIndicator');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');

  function updatePage() {{
    pages.forEach((p, idx) => {{
      p.classList.toggle('active', idx === currentPage);
    }});
    pageIndicator.textContent = (currentPage + 1) + ' / ' + pages.length;
    prevBtn.disabled = (currentPage === 0);
    nextBtn.disabled = (currentPage === pages.length - 1);
  }}

  function prevPage() {{
    if (currentPage > 0) {{
      currentPage--;
      updatePage();
      window.scrollTo(0, 0);
    }}
  }}

  function nextPage() {{
    if (currentPage < pages.length - 1) {{
      currentPage++;
      updatePage();
      window.scrollTo(0, 0);
    }}
  }}
  updatePage();
</script>
</body>
</html>

[응답 형식]
반드시 부연 설명 없이 유효한 JSON 형식으로만 응답하세요.
"html_code": "<!DOCTYPE html><html>...</html>"
"""

                    prompt = prompt_template.format(
                        template_type=template_type,
                        note_size=note_size,
                        class_notes=class_notes
                    )

                    response = client.chat.completions.create(
                        model="solar-pro",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a worksheet template generator. You NEVER write answers or explanations inside <td> cells. All content/feature cells MUST BE strictly empty `<td></td>`."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.0
                    )

                    raw_response = response.choices[0].message.content.strip()
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    if raw_response.startswith("```"):
                        raw_response = raw_response[3:]
                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    data = json.loads(raw_response.strip())
                    html_code = data.get("html_code", "")

                    # 미리보기 프레임
                    components.html(html_code, height=940, scrolling=False)

                    # 다운로드 버튼
                    st.download_button(
                        label="💾 100% 무지 템플릿 다운로드 (HTML)",
                        data=html_code,
                        file_name="pure_blank_template.html",
                        mime="text/html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
