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
# 2. Page Config & Custom CSS (사이트 디자인 개선)
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
    /* 전체 배경 및 폰트 설정 */
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
    
    /* 카드 컨테이너 */
    .css-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    
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
    <div class="hero-title">✨ AI 맞춤형 학습 템플릿 생성기</div>
    <div class="hero-subtitle">
        학습 주제를 입력하면 설명이나 힌트 없이 <b>오직 필기에만 집중할 수 있는 perfect-fit 공백 서식</b>을 생성합니다.<br>
        표 문법 파손 방지 및 A4 장 단위 자동 분할 엔진이 탑재되어 있습니다.
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
    
    submit_btn = st.button("🚀 장 단위 무지 템플릿 생성", use_container_width=True)

with col_view:
    st.subheader("🖼️ 템플릿 미리보기 (장 단위)")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("⚠️ 학습 주제를 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("⚠️ 코드 상단의 UPSTAGE_API_KEY 변수에 실제 API 키를 입력해 주세요.")
        else:
            with st.spinner("표 문법 검증 및 A4 장 단위 규격에 맞춰 제작 중입니다..."):
                try:
                    # 완벽한 HTML 문법 규격 및 장 잘림 방지 프롬프트
                    prompt_template = """
[사용자 입력 정보]
1. 템플릿 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습 주제:
{class_notes}

[HTML 표 문법 필수 준수 규칙 (오류 엄금)]
1. 모든 표(table) 생성 시 아래의 **표준 HTML 구조**를 완벽하게 지키세요.
   - <th> 태그 수와 각 <tr> 안의 <td> 태그 수는 정확히 일치해야 합니다.
   - 단 하나의 <td>도 닫는 태그(</td>)를 누락하거나 `<td><td>`처럼 중첩해서 쓰지 마세요.
   - 올바른 예시:
     <table>
       <thead><tr><th>구분</th><th>특징</th></tr></thead>
       <tbody>
         <tr><td></td><td></td></tr>
         <tr><td></td><td></td></tr>
       </tbody>
     </table>

[본문 100% 무지(공백) 규칙]
1. <th>, .section-title, .sub-title 외의 본문 공간(<td>, .blank-box) 내부에 문장, 키워드, 예시, 힌트를 절대 넣지 마세요.
2. 필기용 셀은 <td></td>, 박스는 <div class="blank-box"></div> 형태로 완벽한 공백으로 두세요.

[페이지 overflow잘림 방지 규칙]
1. 한 개 페이지(<div class="page">)에 너무 많은 내용을 몰아넣지 마세요. (A4 높이 초과 방지)
2. 한 페이지에는 [제목 1개 + 표 1~2개 + 공백 박스 1~2개] 수준으로 적절히 배치하고, 분량이 넘어가면 반드시 다음 <div class="page">...</div>로 분할하여 작성하세요.

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
  td {{ border: 1px solid #cbd5e1; padding: 10px; height: 48px; vertical-align: top; }}
  .blank-box {{ border: 1px dashed #94a3b8; border-radius: 6px; min-height: 90px; background-color: #fafafa; margin-bottom: 18px; }}
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
     <!-- 1페이지 올바른 HTML 표 및 빈 박스 -->
  </div>
  <!-- 필요시 페이지 2, 3 분할 -->
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
반드시 마크다운이나 다른 설명 없이 유효한 JSON 형식으로만 응답하세요.
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
                                "content": "You are a precise HTML layout compiler. You never write invalid HTML table syntax like <td><td>. You split large documents across multiple clean page divs without exceeding page height limits."
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
                        label="💾 완벽한 무지 템플릿 다운로드 (HTML)",
                        data=html_code,
                        file_name="clean_study_template.html",
                        mime="text/html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
