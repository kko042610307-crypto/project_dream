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
# 2. Page Config
# ==============================================================================
st.set_page_config(
    page_title="주제 맞춤형 순수 무지 템플릿 생성기",
    page_icon="📝",
    layout="wide"
)

st.title("📝 주제 맞춤형 순수 무지 템플릿 생성기")

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
            "🌳 무지 위계/분류 박스 (분류 체계용 빈 마인드맵/상자)",
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
        placeholder="예시:\n생명과학 3역 6계 분류 체계를 정리할 수 있는 분류 표와 박스를 만들어줘.\n또는 사회문화 기능론/갈등론/상징적 상호작용론을 비교 정리할 수 있는 완전 공백 표를 구성해줘."
    )
    
    submit_btn = st.button("🚀 장 단위 무지 템플릿 생성하기", use_container_width=True)

with col_output:
    st.subheader("🖼️ 템플릿 미리보기 (장 단위 넘기기)")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("학습 주제를 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("코드 상단의 UPSTAGE_API_KEY 변수에 실제 Upstage API 키를 입력해 주세요.")
        else:
            with st.spinner("다중 페이지의 완벽한 공백 서식을 디테일하게 생성 중입니다..."):
                try:
                    # 다중 페이지 완성도 및 100% 공백 유지를 위한 엄격한 프롬프트
                    prompt_template = """
[사용자 입력 정보]
1. 템플릿 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습 주제 및 요구사항:
{class_notes}

[원칙 1: 본문 100% 빈칸 보장 - 텍스트 채우기 절대 금지]
- <th>(표 헤더), .section-title(구획 제목), .sub-title(소제목) 외에는 본문 내부(<td>, .blank-box)에 그 어떤 단어, 힌트, 요약, 문장도 작성하지 마세요.
- 필기용 데이터 셀은 반드시 <td></td> 와 같이 완벽히 비워두어야 합니다.
- 필기용 박스는 <div class="blank-box"></div> 와 같이 내부에 어떠한 텍스트도 넣지 마세요.

[원칙 2: 다중 페이지(2장 이상) 작성 시 완벽성 보장]
- 요구사항 분량이 많아 2장 이상의 <div class="page">가 필요한 경우, 2번째, 3번째 페이지도 첫 번째 페이지와 동일한 높은 품질과 완벽한 HTML 구조로 작성하세요.
- 뒷부분 페이지라고 해서 태그를 작성하다 말거나, 구조를 생략하거나, 미완성 상태로 끝내는 것을 절대 금지합니다.
- 모든 <div class="page">는 완벽히 독립된 페이지 구획이어야 하며, 동일한 서식 디테일을 유지해야 합니다.

[원칙 3: 고정 높이 지정으로 빈 박스/셀 형태 유지]
- 글자가 없어도 수직 공간이 무너지지 않도록 CSS의 고정 높이(height, min-height) 스펙을 준수하세요.

[필수 HTML/JS 통합 구조]
아래 자바스크립트 페이지 슬라이더 및 CSS 구조를 사용하여 단일 HTML5 문서를 완성하세요:

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ margin: 0; background-color: #e2e8f0; font-family: 'Noto Sans KR', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }}
  
  .nav-bar {{ position: sticky; top: 0; z-index: 1000; width: 100%; background: #1e293b; color: white; padding: 12px 0; display: flex; justify-content: center; align-items: center; gap: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
  .nav-btn {{ background: #3b82f6; color: white; border: none; padding: 8px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s; }}
  .nav-btn:disabled {{ background: #64748b; cursor: not-allowed; opacity: 0.6; }}
  .page-num {{ font-size: 15px; font-weight: bold; color: #f8fafc; }}
  
  .page-wrapper {{ padding: 20px 0; display: flex; justify-content: center; width: 100%; }}
  
  .page {{ display: none; background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.15); box-sizing: border-box; padding: 18mm; border-radius: 4px; width: 210mm; min-height: 297mm; }}
  .page.active {{ display: block; }}
  
  .section-title {{ font-size: 18px; font-weight: bold; color: #1e293b; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin: 20px 0 12px 0; }}
  .sub-title {{ font-weight: bold; color: #475569; margin: 12px 0 6px 0; font-size: 14px; }}
  
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }}
  th {{ background-color: #f1f5f9; font-weight: bold; color: #334155; text-align: center; border: 1px solid #cbd5e1; padding: 10px; font-size: 14px; }}
  td {{ border: 1px solid #cbd5e1; padding: 10px; height: 45px; vertical-align: top; }} /* 고정 높이 확보 */
  
  .blank-box {{ border: 1px dashed #94a3b8; border-radius: 6px; min-height: 100px; background-color: #fafafa; margin-bottom: 15px; }} /* 공백 박스 고정 높이 */
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
     <!-- 1페이지 구조 (완전 빈 <td></td> 및 <div class="blank-box"></div>만 사용) -->
  </div>
  <!-- 분량이 많을 경우 2페이지, 3페이지도 동일한 고품질로 생성 -->
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
반드시 유효한 JSON 형식으로만 응답하세요. 부연 설명이나 마크다운 코드 블록은 절대 포함하지 마세요.

"html_code": "<!DOCTYPE html><html>...</html>"
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
                                "content": "You are a professional compiler for printable blank worksheets. You NEVER fill content in table data cells or writing boxes. You always generate complete, perfectly formatted HTML multi-page structures without dropping quality on later pages. Return valid JSON only."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.05  # 생성 일관성 극대화 및 내용 일탈 방지
                    )

                    # JSON 파싱
                    raw_response = response.choices[0].message.content.strip()
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    if raw_response.startswith("```"):
                        raw_response = raw_response[3:]
                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    data = json.loads(raw_response.strip())
                    html_code = data.get("html_code", "")

                    # 1. 미리보기 (슬라이드 넘기기)
                    components.html(html_code, height=920, scrolling=False)

                    # 2. 다운로드 버튼
                    st.download_button(
                        label="💾 순수 무지 템플릿 다운로드 (HTML)",
                        data=html_code,
                        file_name="blank_writing_template.html",
                        mime="text/html",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"템플릿 생성 중 오류가 발생했습니다: {e}")
