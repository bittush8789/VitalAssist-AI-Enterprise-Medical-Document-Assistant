import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from auth.login import login_ui
from auth.register import register_ui
from ocr.pdf_parser import extract_text_from_pdf
from ocr.image_ocr import extract_text_from_image
from ocr.preprocess import preprocess_image
from workflows.langgraph_flow import medical_workflow
import plotly.express as px
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="VitalAssist | Enterprise Medical AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Environment Variables
load_dotenv()

# Professional Color Palette
PRIMARY_COLOR = "#0F172A"
ACCENT_COLOR = "#3B82F6"
BG_GRADIENT = "linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%)"

# Premium CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * {{
        font-family: 'Outfit', sans-serif;
    }}
    
    .stApp {{
        background: {BG_GRADIENT};
    }}
    
    /* Custom Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {PRIMARY_COLOR};
    }}
    
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: white !important;
    }}
    
    /* Glassmorphism Cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(15, 23, 42, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
        color: #1E293B !important; /* Ensure text is dark */
    }}
    
    .glass-card p, .glass-card h1, .glass-card h2, .glass-card h3, .glass-card div {{
        color: #1E293B !important;
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        border-color: {ACCENT_COLOR};
    }}
    
    /* Header Styling */
    .main-title {{
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1E293B 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }}
    
    .subtitle {{
        color: #64748B;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 3rem;
    }}
    
    /* Metric Cards */
    .metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {ACCENT_COLOR};
    }}
    
    .metric-label {{
        color: #64748B;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Form Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {{
        background-color: white !important;
        color: #1E293B !important;
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
    }}
    
    /* Input Labels */
    .stMarkdown p, label {{
        color: #1E293B !important;
        font-weight: 500 !important;
    }}
    
    /* Buttons */
    .stButton>button {{
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: {ACCENT_COLOR};
        color: white !important;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        opacity: 0.9;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {{
        color: #64748B !important;
    }}
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {ACCENT_COLOR} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

def main():
    if not st.session_state.authenticated:
        # Center Login/Register
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            if os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", width=150)
            st.markdown('<h2 style="text-align:center;">Welcome to VitalAssist</h2>', unsafe_allow_html=True)
            auth_mode = st.tabs(["Login", "Register"])
            with auth_mode[0]:
                login_ui()
            with auth_mode[1]:
                register_ui()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        dashboard()

def dashboard():
    # Sidebar
    with st.sidebar:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=80)
        st.markdown(f"### VitalAssist AI")
        st.write(f"Logged in as: **{st.session_state.user_role}**")
        st.write("---")
        menu = ["🏠 Dashboard", "📄 Document Processing", "🤖 RAG Chatbot", "📊 Analytics", "🚪 Logout"]
        choice = st.radio("", menu)

    if "🏠 Dashboard" in choice:
        st.markdown('<h1 class="main-title">Medical Intelligence Center</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Real-time clinical insights and document automation</p>', unsafe_allow_html=True)
        
        # Real Metrics from data tracker
        try:
            from dashboard.data_tracker import get_stats
            stats = get_stats()
            total_reports = str(stats["total_reports"])
            unique_diag = str(len(set(stats["all_diagnoses"])))
            unique_meds = str(len(set(stats["all_medications"])))
            this_month = str(list(stats["monthly"].values())[-1]) if stats["monthly"] else "0"
        except Exception:
            total_reports, unique_diag, unique_meds, this_month = "0", "0", "0", "0"

        m1, m2, m3, m4 = st.columns(4)
        metrics = [
            ("Total Reports", total_reports),
            ("Unique Diagnoses", unique_diag),
            ("Medications", unique_meds),
            ("This Month", this_month)
        ]
        for col, (label, val) in zip([m1, m2, m3, m4], metrics):
            with col:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center; padding: 1.5rem;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        # Content Row
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color:#1E293B;">Recent Document Activity</h3>', unsafe_allow_html=True)
            try:
                from dashboard.data_tracker import load_history
                history = load_history()
                if history:
                    rows = []
                    for rec in history[-5:][::-1]:
                        diag_list = rec.get("diagnosis", {}).get("diagnosis", []) if isinstance(rec.get("diagnosis"), dict) else []
                        rows.append({
                            "Time": rec.get("timestamp", "N/A"),
                            "File": rec.get("filename", "N/A"),
                            "Top Diagnosis": diag_list[0] if diag_list else "—",
                            "Status": "✅ Completed"
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
                else:
                    st.info("No documents processed yet. Go to **📄 Document Processing** to get started.")
            except Exception:
                st.info("No documents processed yet.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<h3 style="color:#1E293B;">System Status</h3>', unsafe_allow_html=True)
            st.success("✅ All AI Agents Online")
            st.info("ℹ️ Model: Llama 3.3 70B Versatile")
            st.markdown('</div>', unsafe_allow_html=True)

    elif "📄 Document Processing" in choice:
        st.markdown('<h1 class="main-title">Document Processing</h1>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drop clinical documents here (PDF, PNG, JPG)", type=["pdf", "png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file:
            with st.status("Initializing AI Agents...", expanded=True) as status:
                file_path = os.path.join("uploads", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.write("Extracting clinical text...")
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(file_path)
                else:
                    processed_img = preprocess_image(file_path)
                    text = extract_text_from_image(processed_img or file_path)
                
                # Show extracted text for debugging
                st.subheader("🧾 Extracted Text")
                st.write(text)

                # Ensure a fresh vector store for each new document and robustly handle errors
                try:
                    from rag.vector_store import vector_db_manager
                    vector_db_manager.clear_collection()
                except Exception as e:
                    # Log to terminal, not UI
                    print(f"[VectorStore Init Error] {e}")

                # --- NEW: RAG Indexing ---
                try:
                    st.write("Indexing document for RAG...")
                    from rag.chunking import chunk_text
                    chunks = chunk_text(text)
                    vector_db_manager.add_texts(chunks, metadatas=[{"source": uploaded_file.name}] * len(chunks))
                except Exception as e:
                    print(f"[RAG Indexing Error] {e}")
                # -------------------------

                # Run Multi-Agent Workflow (protected)
                try:
                    st.write("Running Multi-Agent Workflow...")
                    inputs = {"text": text, "summary": "", "diagnosis": {}, "insurance": {}, "codes": {}, "metadata": {}}
                    results = medical_workflow.invoke(inputs)
                except Exception as e:
                    print(f"[Workflow Error] {e}")
                    results = {"summary": "Error processing document.", "diagnosis": {}, "insurance": {}, "codes": {}}

                # Save to analytics tracker
                try:
                    from dashboard.data_tracker import save_record
                    save_record({
                        "filename": uploaded_file.name,
                        "summary": results.get("summary", ""),
                        "diagnosis": results.get("diagnosis", {}),
                        "insurance": results.get("insurance", {}),
                        "codes": results.get("codes", {})
                    })
                except Exception as e:
                    print(f"[Tracker Save Error] {e}")

                status.update(label="Processing Complete!", state="complete", expanded=False)
                
            # Results UI
            t1, t2, t3, t4 = st.tabs(["📋 Executive Summary", "🔍 Clinical Diagnosis", "🛡️ Insurance Verify", "🏷️ Medical Coding"])
            
            with t1:
                st.markdown(f'<div class="glass-card" style="font-size:1.1rem; line-height:1.6;">{results["summary"]}</div>', unsafe_allow_html=True)
            
            with t2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.json(results["diagnosis"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with t3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.json(results["insurance"])
                st.markdown('</div>', unsafe_allow_html=True)
                
            with t4:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.json(results["codes"])
                st.markdown('</div>', unsafe_allow_html=True)

    elif "🤖 RAG Chatbot" in choice:
        st.markdown('<h1 class="main-title">Medical RAG Assistant</h1>', unsafe_allow_html=True)
        from rag.chains import rag_chain
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Clear Chat button
        col_a, col_b = st.columns([6, 1])
        with col_b:
            if st.button("🗑️ Clear Chat"):
                st.session_state.messages = []
                try:
                    from rag.vector_store import vector_db_manager
                    vector_db_manager.clear_collection()
                    print("[Clear Chat] Chat history and vector store cleared.")
                except Exception as e:
                    print(f"[Clear Chat Error] {e}")
                st.rerun()

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Query patient history or clinical guidelines..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analyzing context..."):
                    try:
                        answer, retrieved_docs = rag_chain.answer_question(prompt)
                        st.markdown(answer)
                        with st.expander("Show Retrieved Clinical Chunks"):
                            for doc in retrieved_docs:
                                st.info(doc.page_content if hasattr(doc, 'page_content') else str(doc))
                    except Exception as e:
                        print(f"[RAG Chatbot Error] {e}")
                        answer = "I could not find information in the uploaded medical report. Please upload a document first via Document Processing."
                        st.markdown(answer)
            
            st.session_state.messages.append({"role": "assistant", "content": answer})

    elif "📊 Analytics" in choice:
        from dashboard.analytics import render_analytics
        render_analytics()

    elif "🚪 Logout" in choice:
        st.session_state.authenticated = False
        st.rerun()

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    main()
