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
    
    submit_btn = st.button("🚀 순수 무지 템플릿 생성하기", use_container_width=True)

with col_output:
    st.subheader("🖼️ 템플릿 미리보기 (장 단위 넘기기)")
    
    if submit_btn:
        if not class_notes.strip():
            st.warning("학습 주제를 입력해 주세요.")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("코드 상단의 UPSTAGE_API_KEY 변수에 실제 Upstage API 키를 입력해 주세요.")
        else:
            with st.spinner("학습 내용을 모두 제거하고 100% 필기용 공백 틀을 생성 중입니다..."):
                try:
                    # 학습적 내용 배제 및 순수 무지 틀 생성을 위한 엄격한 프롬프트
                    prompt_template = """
[사용자 입력 정보]
1. 템플릿 양식: {template_type}
2. 노트 규격: {note_size}
3. 학습 주제 및 요구사항:
{class_notes}

[학습적 내용 전면 삭제 및 100% 공백 틀 절대 규칙]
1. **학습 관련 설명, 요약, 문장, 예시, 힌트를 본문에 절대로 작성하지 마세요.**
2. 본문의 모든 표 셀(`<td>`), 구획 박스(`<div>`), 항목 공간은 **사용자가 처음부터 끝까지 손필기/타이핑할 수 있는 완전한 공백(빈 칸)**이어야 합니다.
3. 오직 **구조적 틀(제목, 표의 행/열 헤더 `<th>`, 구분 레이블)**만 작성하고, 나머지 필기 영역은 너비와 높이가 확보된 비어있는 상자/셀로 구성하세요.

[HTML 문법 및 품질 준수 절대 규칙]
1. 문법적으로 100% 유효한 W3C 표준 HTML5 문서를 생성하세요.
2. 태그 훼손 (예: `<div> class=...`, `<th> style=...`, `<tr><tr>`, `<td>>내용`)을 절대 일으키지 마세요.
3. 모든 HTML 태그는 정확히 열리고 닫혀야 합니다.

[장 단위 넘기기(Page Pagination) 필수 구조]
아래 자바스크립트 슬라이드 넘기기 레이아웃 구조와 CSS를 그대로 사용하여 완성하세요:

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ margin: 0; background-color: #e2e8f0; font-family: 'Noto Sans KR', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }}
  
  /* 상단 페이지 이동 네비게이션 바 */
  .nav-bar {{ position: sticky; top: 0; z-index: 1000; width: 100%; background: #1e293b; color: white; padding: 12px 0; display: flex; justify-content: center; align-items: center; gap: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }}
  .nav-btn {{ background: #3b82f6; color: white; border: none; padding: 8px 18px; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px; transition: 0.2s; }}
  .nav-btn:disabled {{ background: #64748b; cursor: not-allowed; opacity: 0.6; }}
  .page-num {{ font-size: 15px; font-weight: bold; color: #f8fafc; }}
  
  .page-wrapper {{ padding: 20px 0; display: flex; justify-content: center; width: 100%; }}
  
  /* 장 단위 페이지 */
  .page {{ display: none; background: white; box-shadow: 0 10px 25px rgba(0,0,0,0.15); box-sizing: border-box; padding: 18mm; border-radius: 4px; }}
  .page.active {{ display: block; }}
  
  /* 요소 스타일 (순수 필기용 공간) */
  .section-title {{ font-size: 18px; font-weight: bold; color: #1e293b; border-bottom: 2px solid #3b82f6; padding-bottom: 6px; margin: 20px 0 12px 0; }}
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; }}
  th {{ background-color: #f1f5f9; font-weight: bold; color: #334155; text-align: center; border: 1px solid #cbd5e1; padding: 10px; }}
  td {{ border: 1px solid #cbd5e1; padding: 12px; height: 40px; vertical-align: top; }}
  .blank-box {{ border: 1px dashed #94a3b8; border-radius: 6px; min-height: 80px; background-color: #fafafa; margin-bottom: 15px; }}
  .sub-title {{ font-weight: bold; color: #475569; margin: 12px 0 6px 0; }}
</style>
</head>
<body>

<div class="nav-bar">
  <button class="nav-btn" id="prevBtn" onclick="prevPage()">◀ 이전 페이지</button>
  <span class="page-num" id="pageIndicator">1 / 1</span>
  <button class="nav-btn" id="nextBtn" onclick="nextPage()">다음 페이지 ▶</button>
</div>

<div class="page-wrapper">
  <!-- 내용이 넘치거나 주제 구획이 바뀌면 <div class="page">를 나누어 생성하세요 -->
  <div class="page active">
     <!-- 1페이지 (오직 빈 표, 빈 상자, 목차/헤더 텍스트만 포함) -->
  </div>
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
반드시 유효한 JSON 형식으로만 응답하세요. 마크다운 코드 블록이나 부연 설명은 절대 포함하지 마세요.

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
                                "content": "You are a specialized layout designer. Your task is to generate ONLY empty blank tables, boxes, and structural framework HTML without any explanatory or educational body text. Output valid JSON only."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.1
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
