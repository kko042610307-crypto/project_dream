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
# 2. Page Config & Custom CSS (유저 친화적 디자인 시스템)
# ==============================================================================
st.set_page_config(
    page_title="AI 맞춤형 빈 노트 디자인 스튜디오",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS를 통한 UX/UI 디테일 강화
st.markdown("""
<style>
    /* 메인 배경 및 폰트 설정 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 헤더 히어로 섹션 */
    .hero-header {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        padding: 2.2rem 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.25);
    }
    .hero-header h1 {
        color: white !important;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    .hero-header p {
        color: #E0E7FF;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    /* 카드 컨테이너 스타일링 */
    .ui-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.2rem;
    }

    /* Step 인디케이터 */
    .step-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4F46E5;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin-bottom: 0.8rem;
    }

    /* 메인 버튼 커스텀 */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45) !important;
    }

    /* 하이라이트 박스 */
    .info-callout {
        background-color: #F0F9FF;
        border-left: 4px solid #0EA5E9;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.95rem;
        color: #0369A1;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. 사이드바 (도움말 및 안내)
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/notebook.png", width=70)
    st.title("노트 스튜디오 가이드")
    st.write("나만의 맞춤형 손필기 노트 양식을 AI로 순식간에 제작하세요!")
    
    st.divider()
    
    st.markdown("""
    ### 💡 사용 팁
    1. **스타일 선택**: 필기 목적에 최적화된 양식을 고르세요.
    2. **구조 입력**: 어떤 주제의 수업인지, 필요한 섹션(예: 핵심 키워드, 하단 요약, 질문란 등)을 적어주세요.
    3. **저장 & 출력**: 생성된 HTML을 다운로드하여 **굿노트/노타빌리티**에 불러오거나 **프린터로 인쇄**해 사용하세요.
    """)
    
    st.divider()
    st.caption("Powered by **Upstage Solar AI**")

# ==============================================================================
# 4. 메인 화면 - 히어로 헤더
# ==============================================================================
st.markdown("""
<div class="hero-header">
    <h1>🎨 AI 맞춤형 빈 노트 디자인 스튜디오</h1>
    <p>수업 주제와 구성 요구사항을 입력하면 직접 손필기할 수 있는 완벽한 <b>맞춤형 빈 노트 양식(Blank Template)</b>을 만들어 드립니다.</p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 5. 입력 및 출력 영역 분할 레이아웃
# ==============================================================================
col_left, col_right = st.columns([1.1, 1.3], gap="large")

with col_left:
    st.markdown('<div class="step-badge">STEP 1</div><h3 style="margin-top:-10px;">노트 서식 및 규격</h3>', unsafe_allow_html=True)
    
    with st.container():
        note_style = st.selectbox(
            "📌 필기 양식 스타일 선택",
            [
                "📐 코넬 노트 (Cornell Notes - 핵심키워드 / 넓은 필기란 / 하단 요약)",
                "📝 줄글 노트 (Ruled Notebook - 깔끔한 줄눈 간격 및 섹션 구분)",
                "▦ 모눈/격자 노트 (Grid Paper - 개념 정리 및 도표 작성용)",
                "📊 3분할 구조 노트 (3-Column - 개념 / 상세 정리 / 아이디어 영역)",
                "❓ Q&A 셀프 노트 (Question & Answer - 질문 박스 및 답변 필기 공간)",
                "📦 카드형 섹션 노트 (Sectioned Layout - 주제별 구분 박스 구조)"
            ],
            help="작성하고자 하는 수업의 성격에 어울리는 서식을 골라주세요."
        )
        
        note_size = st.selectbox(
            "📐 노트 용지 / 화면 규격",
            [
                "📄 A4 (210 x 297 mm - 표준 인쇄용)",
                "📘 B5 (176 x 250 mm - 일반 서적/단권화용)",
                "📋 Letter (215.9 x 279.4 mm)",
                "📱 iPad / 태블릿 뷰 (16:9 가로 스크린 맞춤)"
            ],
            help="출력용 용지 규격이나 사용할 디지털 기기 비율을 선택하세요."
        )

    st.markdown('<div class="step-badge" style="margin-top:15px;">STEP 2</div><h3 style="margin-top:-10px;">수업 주제 및 구성 요청</h3>', unsafe_allow_html=True)
    
    class_notes = st.text_area(
        "✍️ 노트에 반영할 수업 주제 및 구획 요청",
        height=220,
        placeholder="예시:\n컴퓨터 네트워크 수업 중 'OSI 7계층' 개념을 정리할 거야.\n상단에는 계층별 이름과 특징을 적을 수 있는 7개의 빈 칸 박스를 만들어주고, 하단에는 핵심 프로토콜 키워드를 직접 쓸 수 있는 노트 공간을 넓게 배치해줘."
    )
    
    submit_btn = st.button("✨ 맞춤형 빈 노트 생성하기", use_container_width=True)

# Right Column - 결과 및 미리보기
with col_right:
    st.markdown('<h3>🎨 생성된 맞춤형 노트</h3>', unsafe_allow_html=True)
    
    if not submit_btn:
        # 생성 전 안내 대기 화면
        st.markdown("""
        <div style="background-color: white; padding: 3rem 2rem; border-radius: 16px; border: 2px dashed #E2E8F0; text-align: center; color: #94A3B8;">
            <img src="https://img.icons8.com/isometric/100/edit-property.png" width="80" style="opacity: 0.7; margin-bottom: 1rem;"><br>
            <h4 style="color: #64748B; margin-bottom: 0.5rem;">아직 생성된 노트가 없습니다.</h4>
            <p style="font-size: 0.95rem;">왼쪽에서 원하는 노트 옵션과 주제를 입력한 후<br><b>[맞춤형 빈 노트 생성하기]</b> 버튼을 눌러주세요!</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # 입력값 검증
        if not class_notes.strip():
            st.warning("⚠️ 노트에 반영할 수업 주제나 구조 요구사항을 입력해 주세요!")
        elif UPSTAGE_API_KEY == "YOUR_UPSTAGE_API_KEY_HERE":
            st.error("🔑 코드 상단의 `UPSTAGE_API_KEY` 변수에 실제 Upstage API 키를 넣어주세요!")
        else:
            with st.spinner("🚀 Upstage Solar AI가 나만의 맞춤형 빈 노트 레이아웃을 디자인하고 있습니다..."):
                try:
                    # 프롬프트 설계 (완전한 공백 틀 생성 강제)
                    prompt = f"""
[사용자 입력 정보]
1. 필기 양식 스타일: {note_style}
2. 노트 규격: {note_size}
3. 수업 주제 및 구조 요구사항:
{class_notes}

[지시 사항]
- 사용자가 입력한 수업 주제 및 구성 요청에 맞추어, 처음부터 끝까지 **직접 손필기하거나 작성할 수 있는 '완전한 빈 노트 양식(Blank Note Template)'**을 생성하세요.
- **필수 준수 규칙**:
  1. 본문 영역에는 완성된 글, 요약 내용, 해설, 빈칸 문제(`_____`) 등을 작성하지 마세요.
  2. 사용자가 손으로 필기할 수 있는 **완전한 공백/라인 영역(줄글 선, 빈 상자, 격자, 점선, 넓은 필기 박스)**으로 레이아웃을 디자인해야 합니다.
  3. 메인 타이틀, 섹션 구분 헤더, 키워드 입력 칸, 하단 요약 상자 등 서식의 구조(Frame)만 미학적으로 배치하세요.
- HTML 내부 `<style>` 태그에 CSS를 포함하여 단일 HTML 문서를 생성하세요.
- 은은한 구분선, 눈이 편안한 색상 팔레트, 세련된 여백을 적용하여 가독성을 극대화하세요.

[응답 형식]
반드시 유효한 JSON 형식으로만 응답하세요. 마크다운 코드 블록(```json 등)이나 부연 설명은 절대 포함하지 마세요.

{{
  "explanation": "디자인된 노트 레이아웃의 구조적 특징과 필기 활용 팁에 대한 2-3줄의 간단하고 친절한 설명",
  "html_code": "<!DOCTYPE html><html><head><style>...</style></head><body>...</body></html>"
}}
"""

                    # Upstage Solar API 호출
                    response = client.chat.completions.create(
                        model="solar-pro",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a world-class stationery and printable worksheet UX designer. You create clean, beautiful HTML/CSS blank templates based on user requirements. Always reply in valid JSON only."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.3
                    )

                    # 응답 파싱 및 파싱 에러 방지 처리
                    raw_response = response.choices[0].message.content.strip()
                    if raw_response.startswith("```json"):
                        raw_response = raw_response[7:]
                    if raw_response.startswith("```"):
                        raw_response = raw_response[3:]
                    if raw_response.endswith("```"):
                        raw_response = raw_response[:-3]

                    data = json.loads(raw_response.strip())
                    explanation = data.get("explanation", "맞춤형 빈 노트 양식이 완성되었습니다.")
                    html_code = data.get("html_code", "")

                    st.success("🎉 나만의 맞춤형 노트 서식이 완성되었습니다!")

                    # 설명글 렌더링
                    st.markdown(f"""
                    <div class="info-callout">
                        💡 <b>노트 구조 가이드:</b> {explanation}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")

                    # 결과 탭(Tabs) 구성
                    tab_preview, tab_code, tab_download = st.tabs(["👁️ 노트 미리보기", "💻 HTML/CSS 소스", "💾 저장 및 출력 가이드"])

                    with tab_preview:
                        components.html(html_code, height=750, scrolling=True)

                    with tab_code:
                        st.caption("생성된 HTML 문서를 직접 수정하거나 웹에 적용할 수 있습니다.")
                        st.code(html_code, language="html")

                    with tab_download:
                        st.markdown("""
                        #### 📥 다운로드 및 활용하는 방법
                        1. 아래 **[HTML 양식 다운로드]** 버튼을 클릭하여 파일(`blank_note_template.html`)을 저장하세요.
                        2. 저장된 파일은 **크롬/웨일 등 웹 브라우저**에서 열어 **`Ctrl + P` (인쇄)**를 누르면 PDF로 저장하거나 종이로 출력할 수 있습니다.
                        3. PDF로 변환한 문서를 **굿노트(Goodnotes), 노타빌리티(Notability)**에 불러오면 디바이스에서 직접 손필기할 수 있습니다.
                        """)
                        
                        st.download_button(
                            label="💾 HTML 양식 다운로드",
                            data=html_code,
                            file_name="blank_note_template.html",
                            mime="text/html",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"❌ 서식 생성 중 오류가 발생했습니다: {e}")
