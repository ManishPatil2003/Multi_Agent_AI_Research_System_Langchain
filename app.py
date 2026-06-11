import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The AI Research Loop · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* =========================
   GLOBAL
========================= */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 20%,
        rgba(77,163,255,0.15),
        transparent 30%),

        radial-gradient(circle at 85% 80%,
        rgba(124,92,255,0.15),
        transparent 30%),

        radial-gradient(circle at 50% 100%,
        rgba(0,255,180,0.08),
        transparent 40%),

        #05070d;

    color: #f8fafc;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* =========================
   HERO
========================= */

.hero {
    text-align: center;
    padding: 4rem 0;
}

.hero-eyebrow {
    color: #60a5fa;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1rem;
    font-weight: 600;
}

.hero h1 {
    font-size: clamp(3rem, 7vw, 6rem);
    font-weight: 800;
    line-height: 1;
    margin-bottom: 1rem;
    color: white;
}

.hero h1 span {
    background: linear-gradient(
        135deg,
        #4da3ff,
        #7c5cff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    max-width: 650px;
    margin: auto;
    color: #94a3b8;
    font-size: 1.1rem;
    line-height: 1.8;
}

/* =========================
   DIVIDER
========================= */

.divider {
    height: 1px;

    background:
    linear-gradient(
        90deg,
        transparent,
        rgba(77,163,255,.5),
        transparent
    );

    margin: 2rem 0;
}

/* =========================
   GLASS PANELS
========================= */

.input-card,
.step-card,
.result-panel,
.report-panel,
.feedback-panel {

    background: rgba(255,255,255,0.04);

    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 20px;

    box-shadow:
        0 10px 40px rgba(0,0,0,.25);

    transition: all .3s ease;
}

.input-card {
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.report-panel,
.feedback-panel {
    padding: 2rem;
}

/* =========================
   INPUT
========================= */

.stTextInput label {
    color: #60a5fa !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
}

.stTextInput input {

    background: rgba(255,255,255,0.05) !important;

    border: 1px solid rgba(255,255,255,.1) !important;

    color: white !important;

    border-radius: 12px !important;

    padding: .85rem 1rem !important;
}

.stTextInput input:focus {

    border-color: #4da3ff !important;

    box-shadow:
        0 0 0 3px rgba(77,163,255,.15) !important;
}

/* =========================
   BUTTON
========================= */

.stButton > button {

    width: 100%;

    border: none !important;

    border-radius: 12px !important;

    padding: .85rem 1.5rem !important;

    background:
    linear-gradient(
        135deg,
        #4da3ff,
        #7c5cff
    ) !important;

    color: white !important;

    font-weight: 700 !important;

    transition: all .25s ease !important;

    box-shadow:
        0 10px 30px rgba(77,163,255,.35) !important;
}

.stButton > button:hover {

    transform: translateY(-3px);

    box-shadow:
        0 15px 40px rgba(77,163,255,.5) !important;
}

/* =========================
   PIPELINE
========================= */

.step-card {
    padding: 1.3rem;
    margin-bottom: 1rem;
}

.step-card.active {

    border-color:
    rgba(77,163,255,.45);

    background:
    rgba(77,163,255,.08);
}

.step-card.done {

    border-color:
    rgba(34,197,94,.4);

    background:
    rgba(34,197,94,.08);
}

.step-header {
    display: flex;
    align-items: center;
}

.step-num {
    color: #60a5fa;
    font-size: .75rem;
    margin-right: .75rem;
}

.step-title {
    color: white;
    font-weight: 700;
}

.status-running {
    color: #60a5fa;
}

.status-done {
    color: #22c55e;
}

.status-waiting {
    color: #64748b;
}

/* =========================
   SECTION TITLES
========================= */

.section-heading {

    color: white;

    font-size: 1.5rem;

    font-weight: 700;

    margin-bottom: 1rem;
}

/* =========================
   PANELS
========================= */

.panel-label {

    text-transform: uppercase;

    letter-spacing: 2px;

    font-size: .75rem;

    margin-bottom: 1rem;

    padding-bottom: .75rem;
}

.panel-label.orange {
    color: #60a5fa;
    border-bottom: 1px solid rgba(77,163,255,.2);
}

.panel-label.green {
    color: #22c55e;
    border-bottom: 1px solid rgba(34,197,94,.2);
}

/* =========================
   RESULTS
========================= */

.result-content {
    color: #cbd5e1;
    line-height: 1.8;
}

/* =========================
   EXPANDER
========================= */

details {

    background:
    rgba(255,255,255,.03);

    border-radius: 12px;

    padding: .75rem;
}

details summary {
    color: #94a3b8;
}

/* =========================
   NOTICE
========================= */

.notice {
    text-align: center;
    margin-top: 3rem;
    color: #64748b;
    font-size: .8rem;
}

/* =========================
   SCROLLBAR
========================= */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #334155;
    border-radius: 20px;
}

::-webkit-scrollbar-thumb:hover {
    background: #4da3ff;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>The AI Research<span>Loop</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    done = st.session_state.done

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        idx = steps.index(step)
        completed = list(r.keys())
        # figure out which steps are done
        if step in r:
            return "done"
        # which step is running now (first not in r)
        if st.session_state.running:
            for i, k in enumerate(steps):
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information")
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content")
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None   # keep inline for now

    # ── Step 2: Reader ──
    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    # Raw outputs in expanders
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])   # render markdown natively
        st.markdown("</div>", unsafe_allow_html=True)

        # Download
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)