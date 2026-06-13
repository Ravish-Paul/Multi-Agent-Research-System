import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

import streamlit as st
import os
from graph import graph

# Set page configuration for a wider layout and custom tab icon/title
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

/* Main font styling */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Inter', sans-serif;
}

/* Custom Header styling */
.main-header {
    background: linear-gradient(135deg, rgba(31, 41, 55, 0.9) 0%, rgba(17, 24, 39, 0.95) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.header-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(to right, #60a5fa, #3b82f6, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.header-desc {
    color: #9ca3af;
    margin-top: 0.5rem;
    font-size: 1.1rem;
}

/* Cards style */
.card-container {
    background-color: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    height: 100%;
}

.agent-badge {
    background: rgba(96, 165, 250, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(96, 165, 250, 0.3);
    padding: 0.2rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.report-container {
    background-color: rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar - Settings & Inputs
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/artificial-intelligence.png", width=80)
    st.title("Configuration")
    st.write("Set up your research parameters below.")
    
    st.divider()
    
    topic = st.text_area(
        "🔍 Research Topic / Query", 
        placeholder="Enter a topic (e.g., Quantum Computing breakthroughs in 2025)",
        height=100
    )
    
    uploaded_file = st.file_uploader(
        "📁 Upload Context PDF (Optional)", 
        type="pdf",
        help="Upload a PDF document to prioritize it as context for your research."
    )
    
    st.divider()
    
    # Run button with visual prominence
    run_btn = st.button("🚀 Launch Swarm Research", use_container_width=True, type="primary")

# Main Header
st.markdown("""
<div class="main-header">
    <h1 class="header-title">Multi-Agent Research Swarm</h1>
    <div class="header-desc">An intelligent system orchestrating research, fact-checking, synthesis, and report writing.</div>
</div>
""", unsafe_allow_html=True)

pdf_path = None
if uploaded_file is not None:
    pdf_path = "temp.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.subheader("⚙️ Swarm Execution Progress")
        
        # Display progress status
        with st.status("🤖 Orchestrating Multi-Agent Swarm...", expanded=True) as status:
            result = {}
            try:
                # Use stream to show real-time agent updates
                for event in graph.stream({"topic": topic, "pdf_path": pdf_path}):
                    for node_name, node_output in event.items():
                        if node_name == "research":
                            status.write("🔍 **Researcher Agent** finished searching and compiling data.")
                            result["research"] = node_output.get("research")
                            result["search_result"] = node_output.get("search_result")
                        elif node_name == "fact_checker":
                            status.write("🛡️ **Fact Checker Agent** verified research findings.")
                            result["verified_research"] = node_output.get("verified_research")
                        elif node_name == "summary":
                            status.write("📝 **Summarizer Agent** generated summary of facts.")
                            result["summary"] = node_output.get("summary")
                        elif node_name == "writer":
                            status.write("✍️ **Writer Agent** completed the final report.")
                            result["report"] = node_output.get("report")
                
                status.update(label="✨ Swarm Research Complete!", state="complete", expanded=False)
                
            except Exception as e:
                status.update(label="❌ Swarm Execution Failed", state="error", expanded=True)
                st.error(f"Error executing research graph: {str(e)}")
                result = None

        if result:
            # Check report format
            report = result.get("report")
            if report:
                if isinstance(report, list):
                    report = report[0]["text"]
            else:
                report = "No report could be generated."

            # Organize the outputs in tabs
            tab1, tab2, tab3 = st.tabs([
                "📄 Executive Report", 
                "🧠 Swarm Intelligence Trace", 
                "📁 Source Documents"
            ])
            
            with tab1:
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.markdown(report)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.divider()
                st.download_button(
                    label="📥 Download Report (.txt)",
                    data=report,
                    file_name=f"research_report_{topic.replace(' ', '_')[:30]}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            with tab2:
                st.write("Explore the individual outputs from each specialized AI agent:")
                
                # Researcher Agent Expander
                with st.expander("🔍 Researcher Agent Output", expanded=False):
                    research_out = result.get("research")
                    if research_out:
                        st.markdown(research_out)
                    else:
                        st.info("No research output generated.")
                
                # Fact Checker Agent Expander
                with st.expander("🛡️ Fact Checker Verification Log", expanded=False):
                    fact_out = result.get("verified_research")
                    if fact_out:
                        st.markdown(fact_out)
                    else:
                        st.info("Fact Checker was skipped for this query type (Simple Query).")
                
                # Summarizer Agent Expander
                with st.expander("📝 Summarizer Agent Synthesis", expanded=False):
                    sum_out = result.get("summary")
                    if sum_out:
                        st.markdown(sum_out)
                    else:
                        st.info("Summarizer was skipped for this query type (Simple Query).")
                        
            with tab3:
                if pdf_path:
                    st.write("Extracts retrieved from the uploaded PDF document context:")
                    search_res = result.get("search_result")
                    if search_res:
                        st.subheader("Vector DB Search Match Hits")
                        st.text(search_res)
                    else:
                        st.info("No context could be loaded from the PDF.")
                else:
                    st.info("No PDF was uploaded for this run. The researcher relied on public web sources.")

else:
    # Beautiful landing/intro layout when not running
    st.subheader("About the Swarm")
    st.write("This application leverages a collaborative multi-agent architecture powered by LangGraph to research, verify, and write reports.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="card-container">
            <span class="agent-badge">Agent 1</span>
            <h4>🔍 Researcher</h4>
            <p style="font-size:0.85rem; color:#9ca3af;">Gathers facts from uploaded PDFs and web searches using FAISS vector storage & duckduckgo.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card-container">
            <span class="agent-badge">Agent 2</span>
            <h4>🛡️ Fact Checker</h4>
            <p style="font-size:0.85rem; color:#9ca3af;">Reviews the gathered research to flag any inconsistencies, unsupported claims, or inaccuracies.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="card-container">
            <span class="agent-badge">Agent 3</span>
            <h4>📝 Summarizer</h4>
            <p style="font-size:0.85rem; color:#9ca3af;">Synthesizes the validated research into structured summaries to eliminate redundancy.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="card-container">
            <span class="agent-badge">Agent 4</span>
            <h4>✍️ Writer</h4>
            <p style="font-size:0.85rem; color:#9ca3af;">Drafts the final technical report, laying out title, introduction, key findings, and conclusions.</p>
        </div>
        """, unsafe_allow_html=True)