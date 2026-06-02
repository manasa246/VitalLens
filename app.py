import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="VitalLens",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding-top: 1rem;
}

.header-container {
    background: #2563eb;
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
}

.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2563eb;
    margin-bottom: 0.5rem;
}

.diet-section {
    background: #f0fdf4;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1rem;
    border-left: 4px solid #10b981;
}

.warning-section {
    background: #fef2f2;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1rem;
    border-left: 4px solid #ef4444;
}

.stButton > button[kind="primary"] {
    background-color: #2563eb !important;
    border-color: #2563eb !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# Session State
if "llm" not in st.session_state:
    st.session_state.llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash"
    )

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "diet_results" not in st.session_state:
    st.session_state.diet_results = None

# Header
st.markdown("""
<div class="header-container">
    <h1>VitalLens: Health Insights Made Simple</h1>
    <p>
        Upload your blood work report to get personalized health insights
        and dietary recommendations
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📋 About This App")

    st.info("""
This application uses AI to:

- Extract blood test values from reports
- Classify results as HIGH, LOW, or NORMAL
- Provide health summaries
- Suggest Indian diet recommendations
""")

    st.divider()

    st.subheader("📝 How to Use")

    st.markdown("""
1. Upload a blood report (.txt or .pdf)
2. Or paste the report directly
3. Click Analyze Blood Report
4. Review results and recommendations
""")

# Main Content (Full Width)
st.subheader("📤 Upload Your Blood Report")

uploaded_file = st.file_uploader(
    "Choose a blood work report",
    type=["txt", "pdf"],
    help="Upload a TXT or PDF blood report"
)

st.divider()

st.subheader("📝 Or Paste Your Report")

pasted_text = st.text_area(
    "Paste your blood work report here",
    height=400,
    placeholder="Paste the blood report text here or upload a file above..."
)

# Analyze Button
if st.button(
    "🔍 Analyze Blood Report",
    type="primary",
    use_container_width=True
):
    blood_report = None

    # File Upload Handling
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".txt"):
                blood_report = uploaded_file.read().decode("utf-8")

            elif uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)

                pages = []

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)

                blood_report = "\n".join(pages)

        except Exception as e:
            st.error(f"Error reading file: {e}")

    elif pasted_text.strip():
        blood_report = pasted_text

    if not blood_report:
        st.warning(
            "Please upload a report or paste report content."
        )

    else:
        with st.spinner("🤔 Analyzing your blood report..."):

            # Stage 1: Blood Analysis
            extraction_prompt = f"""
You are a medical data extraction assistant.

From the blood report below, extract all test values and classify each one as
HIGH, LOW, or NORMAL based on the reference ranges provided.

Format your response as:

- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""

            extraction_response = (
                st.session_state.llm.invoke(extraction_prompt)
            )

            st.session_state.analysis_results = (
                extraction_response.content
            )

            # Stage 2: Diet Recommendations
            diet_prompt = f"""
You are a clinical nutritionist specializing in Indian dietary habits.

Based on the blood work analysis below, provide two clearly separated sections.

SECTION 1 - HEALTH SUMMARY:
Write 4-5 lines explaining the patient's condition
in simple, non-technical language.

SECTION 2 - INDIAN DIET PLAN:
List foods to eat more of and foods to avoid.

Use commonly available Indian foods such as:
- dal
- sabzi
- roti
- rice
- fruits
- nuts

Keep recommendations practical and concise.

Blood Work Analysis:
{st.session_state.analysis_results}
"""

            diet_response = (
                st.session_state.llm.invoke(diet_prompt)
            )

            st.session_state.diet_results = (
                diet_response.content
            )

# Results Section
if (
    st.session_state.analysis_results
    and st.session_state.diet_results
):
    st.divider()

    st.success("✅ Analysis Complete!")

    tab1, tab2 = st.tabs(
        ["📊 Test Results", "🍽️ Diet Recommendations"]
    )

    # Test Results Tab
    with tab1:
        st.subheader("Blood Test Analysis")

        results_lines = (
            st.session_state.analysis_results.split("\n")
        )

        for line in results_lines:
            if line.strip() and "|" in line:
                st.markdown(
                    f"""
                    <div class="metric-card">
                    {line}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with st.expander("📋 Full Analysis"):
            st.text(st.session_state.analysis_results)

    # Diet Recommendations Tab
    with tab2:
        diet_text = st.session_state.diet_results

        if "SECTION 1" in diet_text:
            sections = diet_text.split("SECTION")

            # Health Summary
            if len(sections) > 1:
                summary_text = (
                    sections[1]
                    .replace("1 - HEALTH SUMMARY:", "")
                    .strip()
                )

                summary_parts = summary_text.split("SECTION")

                summary = (
                    summary_parts[0].strip()
                    if summary_parts
                    else summary_text
                )

                st.markdown("""
                <div class="warning-section">
                    <h4>💊 Your Health Summary</h4>
                </div>
                """, unsafe_allow_html=True)

                st.write(summary)

            # Diet Plan
            if len(sections) > 2:
                diet_plan = (
                    sections[2]
                    .replace("2 - INDIAN DIET PLAN:", "")
                    .strip()
                )

                st.markdown("""
                <div class="diet-section">
                    <h4>🥗 Personalized Indian Diet Plan</h4>
                </div>
                """, unsafe_allow_html=True)

                st.write(diet_plan)

        else:
            st.markdown("""
            <div class="diet-section">
                <h4>🥗 Dietary Recommendations & Health Summary</h4>
            </div>
            """, unsafe_allow_html=True)

            st.write(diet_text)

    # Action Buttons
    col1, col2 = st.columns(2)

    with col1:
        results_text = f"""
HEALTH ANALYSIS REPORT
==================================================

TEST RESULTS:

{st.session_state.analysis_results}

==================================================

RECOMMENDATIONS:

{st.session_state.diet_results}
"""

        st.download_button(
            label="📥 Download Results",
            data=results_text,
            file_name="health_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        if st.button(
            "🔄 Analyze Another Report",
            use_container_width=True
        ):
            st.session_state.analysis_results = None
            st.session_state.diet_results = None
            st.rerun()