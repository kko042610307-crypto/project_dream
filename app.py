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
    page_title="AI 맞춤형 학습 템플릿",
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
    <div class="hero-title">✨ AI 맞춤형 학습 템플릿</div>
    <div class="hero-subtitle">
        사용자가 필기하고 싶은 내용을 입력하면 그에 맞는 템플릿을 제공해줍니다.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. 용지 규격 데이터 맵 및 페이지 예산
# ==============================================================================
SIZE_MAP = {
    "A4 (210mm x 297mm)": {
        "width": "210mm", 
        "height": "297mm", 
        "max_elem": "A4 크기이므로 한 <div class='page'> 당 [표 2개] 또는 [표 1개 + 상자 2개] 이하로 구성하세요."
    },
    "A5 (148mm x 210mm)": {
        "width": "148mm", 
        "height": "210mm", 
        "max_elem": "A5는 용지가 작으므로 한 <div class='page'> 당 반드시 [표 1개] 또는 [상자 2개] 이하만 배치하세요. 내용이 많다면 <div class='page'>를 3~5개 이상 적극적으로 분할하세요!"
    },
    "B5 (176mm x 250mm)": {
        "width": "176mm", 
        "height": "250mm", 
        "max_elem": "B5 크기이므로 한 <div class='page'> 당 [표 1~2개] 이하로 구성하세요."
    },
    "iPad Screen (4:3)": {
        "width": "240mm", 
        "height": "180mm", 
        "max_elem": "4:3 비율의 아이패드 화면이므로 한 <div class='page'> 당 [표 1개] 또는 [상자 2개] 이하로 깔끔하게 구성하세요."
    }
}

# ==============================================================================
# 4. 입력 및 미리보기 레이아웃
# ==============================================================================
col_config, col_view = st.columns([1, 1.3], gap="large")

with col_config:
    st.subheader("⚙️ 서식 설정")
    
    # 템플릿 구조 고정
    template_type = "🤖 AI 자동 구조화 (학습 주제의 특성에 맞춰 최적의 무지 표/상자/디자인 자동 분할)"
    
    # 노트 용지 규격 선택
    note_size = st.selectbox(
        "📐 노트 용지 규격",
        list(SIZE_MAP.keys())
    )
    
    class_notes = st.text_area(
        "✍️ 학습 주제 및 구성 요구사항",
        height=320,
        placeholder="예시:\n1.인공지능, 머신러닝, 딥러닝 개념 정리 표와 머신러닝 학습 유형(지도/비지도/강화학습) 비교 표를 만들어주고, 과적합 해결 방안과 K-Means 단계별 정리 상자 틀을 만들어줘."\n\n"사회와 문화 시간에 배운 사회를 바라보는 관점을 정리하여 간단하게 한 눈에 알아볼 수 있게 만들어줘".
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
            with st.spinner("템플릿을 생성중입니다..."):
                try:
                    selected_size_info = SIZE_MAP[note_size]
                    page_w = selected_size_info["width"]
                    page_h = selected_size_info["height"]
                    max_elem_rule = selected_size_info["max_elem"]

                    prompt_template = """
[사용자 입력 정보]
1. 템플릿 양식: {template_type}
2. 노트 규격: {note_size} (가로: {page_w}, 세로: {page_h})
3. 학습 주제:
{class_notes}

[절대 규칙 1: 2번째 열부터는 무조건 100% 빈 칸 `<td></td>`]
1. 각 행(`<tr>`)에서 오직 **1번째 `<td>`에만** 구분 명칭(예: 인공지능, 지도학습, 데이터 부족 등)을 작성하십시오.
2. **2번째, 3번째, 4번째 이후의 모든 `<td>`에는 어떤 단어나 키워드도 절대 쓰지 말고 100% `<td></td>`로 비워두어야 합니다.**

[작성 예시 (FEW-SHOT EXAMPLES)]
❌ 잘못된 작성 방식 (절대 금지 - 2번째, 3번째 열에 단어를 채우는 행위):
<tr>
  <td>인공지능</td>
  <td>머신러닝</td> <!-- 금지! -->
  <td>딥러닝</td>   <!-- 금지! -->
</tr>

✅ 올바른 작성 방식 (필수 준수!):
<tr>
  <td>인공지능</td>
  <td></td> <!-- 완벽 -->
  <td></td> <!-- 완벽 -->
</tr>

[절대 규칙 2: 용지 높이 초과 엄금 (페이지 분할 규칙)]
1. 선택된 용지 규격: {note_size} (세로 높이: {page_h})
2. 용지 배치 제한: {max_elem_rule}
3. 한 페이지에 요소를 무리하게 많이 넣어서 아래로 잘리는 것은 심각한 오류입니다. 내용이 많다면 반드시 `<div class="page">...</div>`를 여러 개(3~5개) 사용하여 페이지를 분할하세요.

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
  .page {{ display: none; background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.15); box-sizing: border-box; padding: 15mm; border-radius: 4px; width: {page_w}; height: {page_h}; overflow: hidden; }}
  .page.active {{ display: block; }}
  .section-title {{ font-size: 18px; font-weight: bold; color: #0f172a; border-bottom: 2px solid #2563eb; padding-bottom: 6px; margin: 5px 0 14px 0; }}
  .sub-title {{ font-weight: bold; color: #334155; margin: 12px 0 6px 0; font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; table-layout: fixed; }}
  th {{ background-color: #f1f5f9; font-weight: bold; color: #1e293b; text-align: center; border: 1px solid #cbd5e1; padding: 8px; font-size: 13px; }}
  td {{ border: 1px solid #cbd5e1; padding: 8px; height: 42px; vertical-align: top; }}
  .blank-box {{ border: 1px dashed #94a3b8; border-radius: 6px; min-height: 80px; background-color: #fafafa; margin-bottom: 14px; }}
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
     <!-- 1페이지 표 (규격 제한에 맞춰 표 1~2개 배치) -->
  </div>
  <!-- 높이 초과 방지를 위한 추가 페이지 분할 -->
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
                        page_w=page_w,
                        page_h=page_h,
                        max_elem_rule=max_elem_rule,
                        class_notes=class_notes
                    )

                    response = client.chat.completions.create(
                        model="solar-pro",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a worksheet template generator. NEVER put text in the 2nd, 3rd, or 4th <td> column. STRICTLY limit content per page to fit paper height."
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
                    components.html(html_code, height=1050, scrolling=True)

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
