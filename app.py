# app.py  –  AI-Assisted Requirement Tool  v2
# Run: streamlit run app.py

import streamlit as st
import time as _time

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Assisted Requirement Tool",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0b0d12; color: #ddd9d0; }
.block-container { max-width: 960px; padding-top: 2rem; padding-bottom: 4rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0e1017;
    border-right: 1px solid #1a1d28;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* Header */
.hero { text-align:center; margin-bottom:2rem; }
.hero h1 {
    font-family:'DM Serif Display',serif; font-size:2.6rem;
    color:#ede9df; margin:0; letter-spacing:-0.5px;
}
.hero p { color:#6a6d7a; font-size:.95rem; margin:.4rem 0 0; }
.accent { width:50px; height:3px;
    background:linear-gradient(90deg,#e07845,#c94f6e);
    border-radius:2px; margin:.9rem auto 0; }

/* Cards */
.card {
    background:#10121a; border:1px solid #1c1f2e;
    border-radius:12px; padding:1.5rem 1.7rem; margin-bottom:1.2rem;
}
.card h3 {
    font-family:'DM Serif Display',serif; font-size:1.1rem;
    color:#ede9df; margin:0 0 1rem;
}

/* Score ring */
.score-wrap { text-align:center; }
.score-num {
    font-family:'DM Serif Display',serif; font-size:3.5rem;
    line-height:1; color:#ede9df;
}
.score-grade { font-size:.9rem; font-weight:600; letter-spacing:1px; }
.grade-A { color:#5ecb82; }
.grade-B { color:#70b8e0; }
.grade-C { color:#e0c050; }
.grade-D { color:#e08040; }
.grade-F { color:#e06070; }

/* Checklist items */
.chk { display:flex; align-items:center; gap:8px;
    padding:.4rem .6rem; border-radius:6px; font-size:.86rem;
    margin-bottom:4px; }
.chk-ok  { background:#0d2018; color:#5ecb82; border:1px solid #1e4030; }
.chk-off { background:#1a0e12; color:#c06070; border:1px solid #3a1828; }

/* Alerts */
.alert { padding:.8rem 1.1rem; border-radius:8px;
    font-size:.88rem; margin-bottom:.8rem; line-height:1.5; }
.alert-ok   { background:#0c2018; border:1px solid #1e4030; color:#5ecb82; }
.alert-err  { background:#1e0c10; border:1px solid #581820; color:#e07080; }
.alert-warn { background:#1c1408; border:1px solid #4a3010; color:#e0a050; }
.alert-info { background:#0c1620; border:1px solid #1e3050; color:#60a0e0; }

/* Issue / suggestion */
.issue { display:flex; align-items:flex-start; gap:8px;
    padding:.55rem .8rem; margin-bottom:5px;
    background:#1a0c10; border:1px solid #3a1820;
    border-radius:6px; color:#e07080; font-size:.86rem; }
.suggestion { display:flex; align-items:flex-start; gap:8px;
    padding:.55rem .8rem; margin-bottom:5px;
    background:#0d1a10; border:1px solid #1e4028;
    border-radius:6px; color:#70c890; font-size:.86rem; }

/* TC card */
.tc { background:#0c0e15; border:1px solid #1c1f2e;
    border-radius:10px; padding:1rem 1.2rem; margin-bottom:8px; position:relative; }
.tc:hover { border-color:#2c3048; }
.tc-badge { display:inline-block; font-size:.7rem; font-weight:700;
    letter-spacing:.8px; padding:2px 9px; border-radius:12px;
    text-transform:uppercase; margin-bottom:5px; }
.pos { background:#1c3828; color:#5ecb82; }
.neg { background:#381820; color:#e07080; }
.tc-id { position:absolute; top:.9rem; right:1.1rem;
    font-family:'JetBrains Mono',monospace; font-size:.72rem; color:#353848; }
.tc-desc { font-size:.9rem; font-weight:500; color:#d0cdc7; margin-bottom:.5rem; }
.lbl { font-size:.7rem; font-weight:600; text-transform:uppercase;
    letter-spacing:.8px; color:#555868; margin-bottom:2px; }
.val { font-size:.83rem; color:#888a98; white-space:pre-line; margin-bottom:.5rem; }
.prio-H { color:#e07080; } .prio-M { color:#e0a050; } .prio-L { color:#6088b8; }

/* History pill */
.hist-pill { display:inline-flex; align-items:center; gap:6px;
    background:#13151e; border:1px solid #1e2130; border-radius:8px;
    padding:.5rem .9rem; margin-bottom:6px; font-size:.84rem;
    width:100%; }
.req-status-valid   { color:#5ecb82; font-weight:600; }
.req-status-invalid { color:#e07080; font-weight:600; }
.req-status-pending { color:#e0a050; font-weight:600; }

/* Traceability table */
.trace-table { width:100%; border-collapse:collapse; font-size:.84rem; }
.trace-table th {
    background:#13151e; color:#888a98; font-weight:600;
    padding:.6rem .9rem; text-align:left; border-bottom:1px solid #1e2130;
    text-transform:uppercase; font-size:.72rem; letter-spacing:.5px;
}
.trace-table td { padding:.55rem .9rem; border-bottom:1px solid #161820; color:#c0bdb8; }
.trace-table tr:last-child td { border-bottom:none; }
.trace-table tr:hover td { background:#11131b; }

/* Buttons */
.stButton>button {
    background:linear-gradient(135deg,#e07845,#c94f6e) !important;
    color:#fff !important; border:none !important;
    border-radius:8px !important; font-family:'DM Sans',sans-serif !important;
    font-weight:600 !important; font-size:.88rem !important;
    transition:opacity .2s,transform .1s !important;
}
.stButton>button:hover { opacity:.85 !important; transform:translateY(-1px); }

.stDownloadButton>button {
    background:#141720 !important; color:#b8b5ae !important;
    border:1px solid #2a2e42 !important; border-radius:8px !important;
    font-family:'DM Sans',sans-serif !important; font-weight:500 !important;
}
.stDownloadButton>button:hover { background:#1c2030 !important; }

/* Text area */
.stTextArea textarea {
    background:#0b0d12 !important; border:1px solid #252838 !important;
    border-radius:8px !important; color:#ddd9d0 !important;
    font-family:'DM Sans',sans-serif !important;
}
.stTextArea textarea:focus { border-color:#e07845 !important; box-shadow:0 0 0 2px rgba(224,120,69,.15) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background:#10121a; border-radius:10px; padding:4px; }
.stTabs [data-baseweb="tab"] { color:#666a80 !important; border-radius:7px; }
.stTabs [aria-selected="true"] { background:#1c1f2e !important; color:#ddd9d0 !important; }

/* File uploader */
[data-testid="stFileUploader"] { background:#10121a; border:1px dashed #252838; border-radius:10px; padding:.5rem; }

/* Progress bar */
.stProgress > div > div { background:linear-gradient(90deg,#e07845,#c94f6e) !important; }

/* Metric */
[data-testid="stMetricValue"] { color:#ede9df !important; font-family:'DM Serif Display',serif !important; }

/* Sidebar text */
.sidebar-section { margin-bottom:1.4rem; }
.sidebar-section h4 { color:#ede9df; font-size:.9rem; font-weight:600;
    margin-bottom:.6rem; border-bottom:1px solid #1e2130; padding-bottom:.4rem; }

.footer { text-align:center; margin-top:3rem; color:#353848; font-size:.76rem; }
</style>
""", unsafe_allow_html=True)


# ── Imports (after page config) ────────────────────────────────────────────────
from requirement import Requirement
from repository import RequirementRepository, TestCaseRepository
from controllers import RequirementController, TestCaseController, ExportController


# ══════════════════════════════════════════════════════════════════════════════
# Session state
# ══════════════════════════════════════════════════════════════════════════════

def _init():
    if "req_repo" not in st.session_state:
        st.session_state.req_repo  = RequirementRepository()
        st.session_state.tc_repo   = TestCaseRepository()
        Requirement.reset_counter()

    defaults = {
        # Current single-req workflow
        "current_req":      None,
        "val_result":       None,
        "current_tcs":      [],
        # Batch / doc workflow
        "batch_reqs":       [],      # list of Requirement objects from upload
        "batch_results":    [],      # list of {req, val_result, tcs}
        # UI state
        "active_tab":       0,
        "req_input_text":   "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

req_ctrl = RequirementController(st.session_state.req_repo)
tc_ctrl  = TestCaseController(st.session_state.tc_repo)
exp_ctrl = ExportController(st.session_state.req_repo, st.session_state.tc_repo)


# ══════════════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _score_bar(score: int):
    st.progress(score / 100)

def _grade_html(grade: str) -> str:
    return '<span class="score-grade grade-' + grade + '">' + grade + '</span>'

def _prio_class(p: str) -> str:
    return {"High": "prio-H", "Medium": "prio-M", "Low": "prio-L"}.get(p, "")

def _render_tc(tc: dict):
    badge = "pos" if tc["type"] == "Positive" else "neg"
    steps_html = (tc.get("steps") or "").replace("\n", "<br>")
    prio = tc.get("priority", "Medium")
    prio_cls = _prio_class(prio)
    st.markdown(
        '<div class="tc">'
        '<span class="tc-badge ' + badge + '">' + tc["type"] + '</span>'
        ' &nbsp;<span class="' + prio_cls + '" style="font-size:.72rem;font-weight:600;">' + prio + ' Priority</span>'
        '<span class="tc-id">' + tc.get("id","") + '</span>'
        '<div class="tc-desc">' + tc.get("description","") + '</div>'
        '<div class="lbl">Preconditions</div>'
        '<div class="val">' + (tc.get("preconditions","") or "—") + '</div>'
        '<div class="lbl">Steps</div>'
        '<div class="val">' + steps_html + '</div>'
        '<div class="lbl">Expected Result</div>'
        '<div class="val">' + tc.get("expected_result","") + '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

def _render_val_result(vr: dict, compact: bool = False):
    score = vr["score"]
    grade = vr["grade"]

    if not compact:
        c1, c2 = st.columns([1, 3])
        with c1:
            st.markdown(
                '<div class="score-wrap">'
                '<div class="score-num">' + str(score) + '</div>'
                '<div style="color:#555868;font-size:.78rem;margin:.2rem 0">/100</div>'
                + _grade_html(grade) +
                '</div>', unsafe_allow_html=True
            )
            _score_bar(score)
        with c2:
            _render_checklist(vr)
    else:
        col_s, col_d = st.columns([1,4])
        with col_s:
            st.markdown('<div class="score-num" style="font-size:2rem">' + str(score) + '</div>' + _grade_html(grade), unsafe_allow_html=True)
        with col_d:
            _render_checklist(vr)

    if vr["issues"]:
        st.markdown("**Issues**")
        for iss in vr["issues"]:
            st.markdown('<div class="issue">⚠️ ' + iss + '</div>', unsafe_allow_html=True)
    if vr["suggestions"]:
        st.markdown("**Suggestions**")
        for sug in vr["suggestions"]:
            st.markdown('<div class="suggestion">💡 ' + sug + '</div>', unsafe_allow_html=True)

def _render_checklist(vr: dict):
    d = vr.get("details", {})
    items = [
        (d.get("obligation_present", False), "Obligation keyword (must/shall/should…)"),
        (d.get("actor_present",     False), "Actor/subject identified"),
        (d.get("measurable",        False), "Measurable criteria present"),
        (d.get("adequate_length",   False), "Sufficient length (≥15 words)"),
        (d.get("condition_present", False), "Conditional clause present"),
        (d.get("error_handling",    False), "Error/exception handling mentioned"),
        (not bool(d.get("ambiguous_words", [])), "No ambiguous language"),
    ]
    for ok, label in items:
        cls = "chk-ok" if ok else "chk-off"
        icon = "✓" if ok else "✗"
        st.markdown('<div class="chk ' + cls + '">' + icon + ' ' + label + '</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Sidebar — Requirement History
# ══════════════════════════════════════════════════════════════════════════════

def _render_sidebar():
    with st.sidebar:
        st.markdown("## Session History")

        all_reqs = st.session_state.req_repo.all()
        if not all_reqs:
            st.markdown('<p style="color:#455;font-size:.85rem;">No requirements yet.</p>', unsafe_allow_html=True)
        else:
            st.markdown(
                str(len(all_reqs)) + " requirement(s) &nbsp;·&nbsp; " +
                str(len(st.session_state.tc_repo.all())) + " test case(s)",
                unsafe_allow_html=True,
            )
            st.markdown("---")
            for req in reversed(all_reqs):
                tcs   = st.session_state.tc_repo.get_for_req(req.req_id)
                sc    = ("Score: " + str(req.score)) if req.score is not None else "Not validated"
                s_cls = "req-status-" + req.status
                st.markdown(
                    '<div class="hist-pill">'
                    '<span style="color:#404358;font-family:\'JetBrains Mono\',monospace;font-size:.75rem;">REQ-' + str(req.req_id).zfill(3) + '</span>'
                    '&nbsp;<span class="' + s_cls + '">' + req.status.upper() + '</span>'
                    '&nbsp;<span style="color:#555868;font-size:.78rem;">' + sc + '</span>'
                    '&nbsp;<span style="color:#404358;font-size:.75rem;">·</span>'
                    '&nbsp;<span style="color:#60a0e0;font-size:.78rem;">' + str(len(tcs)) + ' TCs</span>'
                    '</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<p style="color:#666a80;font-size:.78rem;margin:-4px 0 8px 4px;">'
                    + req.description[:70] + ("…" if len(req.description) > 70 else "") +
                    '</p>',
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        if st.button("🗑  Clear Session", use_container_width=True):
            st.session_state.req_repo.clear()
            st.session_state.tc_repo.clear()
            st.session_state.current_req    = None
            st.session_state.val_result     = None
            st.session_state.current_tcs   = []
            st.session_state.batch_reqs    = []
            st.session_state.batch_results = []
            Requirement.reset_counter()
            st.rerun()

_render_sidebar()


# ══════════════════════════════════════════════════════════════════════════════
# Header
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
  <h1>AI-Assisted Requirement Validation and Test Case Generation Tool</h1>
  <p>Validate · Score · Generate Test Cases · Trace</p>
  <div class="accent"></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Tabs
# ══════════════════════════════════════════════════════════════════════════════

tab_single, tab_doc, tab_trace = st.tabs([
    "✏️  Single Requirement",
    "📄  Upload Document",
    "🔗  Traceability Matrix",
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — SINGLE REQUIREMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_single:

    SAMPLES = [
        "The system must allow registered users to reset their password within 60 seconds via a link sent to their registered email address.",
        "The admin must be able to generate monthly usage reports and export them as CSV files within 30 seconds.",
        "Users should be able to upload files of at most 10 MB in PDF or DOCX format, and the system must reject files that exceed this limit.",
        "The system must lock a user account after 5 consecutive failed login attempts and notify the admin via email.",
        "The application must allow customers to search and filter products by category, price range, and rating, and results must load within 2 seconds.",
    ]

    st.markdown('<div class="card"><h3>📝 Enter Requirement</h3>', unsafe_allow_html=True)

    with st.expander("💡 Load a sample requirement"):
        for i, s in enumerate(SAMPLES):
            if st.button("Sample " + str(i+1) + " — " + s[:60] + "…", key="s" + str(i)):
                st.session_state.req_input_text = s
                st.session_state.current_req    = None
                st.session_state.val_result     = None
                st.session_state.current_tcs   = []
                st.rerun()

    req_text = st.text_area(
        "Requirement:",
        value=st.session_state.req_input_text,
        height=100,
        placeholder="e.g. The system must allow registered users to reset their password within 60 seconds via email.",
        label_visibility="collapsed",
    )

    c1, c2 = st.columns([3,1])
    with c1:
        validate_btn = st.button("🔍  Validate Requirement", use_container_width=True)
    with c2:
        if st.button("↺  Reset", use_container_width=True):
            st.session_state.req_input_text = ""
            st.session_state.current_req    = None
            st.session_state.val_result     = None
            st.session_state.current_tcs   = []
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Handle validate ───────────────────────────────────────────────────────
    if validate_btn:
        if not req_text.strip():
            st.markdown('<div class="alert alert-warn">⚠️ Please enter a requirement.</div>', unsafe_allow_html=True)
        else:
            req = req_ctrl.submit(req_text.strip())
            vr  = req_ctrl.validate(req)
            st.session_state.current_req   = req
            st.session_state.val_result    = vr
            st.session_state.current_tcs  = []
            st.session_state.req_input_text = req_text
            st.rerun()

    # ── Validation result ─────────────────────────────────────────────────────
    if st.session_state.val_result:
        vr  = st.session_state.val_result
        req = st.session_state.current_req

        st.markdown('<div class="card"><h3>🧪 Validation & Quality Score</h3>', unsafe_allow_html=True)

        if vr["valid"]:
            st.markdown('<div class="alert alert-ok">✅ Requirement is <strong>valid</strong>. Ready to generate test cases.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert alert-err">❌ Requirement is <strong>invalid</strong> — fix the issues below before generating test cases.</div>', unsafe_allow_html=True)

        _render_val_result(vr)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Generate button ───────────────────────────────────────────────────
        if vr["valid"]:
            if st.button("⚡  Generate Test Cases for REQ-" + str(req.req_id).zfill(3), use_container_width=False):
                with st.spinner("Analysing requirement and generating test cases…"):
                    tcs = tc_ctrl.generate(req)
                    st.session_state.current_tcs = tcs
                st.rerun()

    # ── Test cases ────────────────────────────────────────────────────────────
    if st.session_state.current_tcs:
        tcs = st.session_state.current_tcs
        req = st.session_state.current_req
        pos = [t for t in tcs if t["type"] == "Positive"]
        neg = [t for t in tcs if t["type"] == "Negative"]

        st.markdown('<div class="card"><h3>🗂️ Generated Test Cases — REQ-' + str(req.req_id).zfill(3) + '</h3>', unsafe_allow_html=True)

        ma, mb, mc = st.columns(3)
        ma.metric("Total", len(tcs))
        mb.metric("✅ Positive", len(pos))
        mc.metric("❌ Negative", len(neg))

        st.markdown("---")

        show_pos = st.checkbox("Show Positive Tests", value=True)
        show_neg = st.checkbox("Show Negative Tests", value=True)

        if show_pos:
            st.markdown("#### ✅ Positive Test Cases")
            for tc in pos:
                _render_tc(tc)

        if show_neg:
            st.markdown("#### ❌ Negative Test Cases")
            for tc in neg:
                _render_tc(tc)

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Export ─────────────────────────────────────────────────────────────
        st.markdown('<div class="card"><h3>📥 Export</h3>', unsafe_allow_html=True)
        try:
            csv_bytes = exp_ctrl.export_csv(req_id=req.req_id)
            st.download_button(
                "⬇️  Download Test Cases (CSV)",
                data=csv_bytes,
                file_name="REQ_" + str(req.req_id).zfill(3) + "_test_cases.csv",
                mime="text/csv",
            )
        except ValueError as e:
            st.error(str(e))
        st.markdown("</div>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — DOCUMENT UPLOAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_doc:

    st.markdown('<div class="card"><h3>📄 Upload Requirements Document</h3>', unsafe_allow_html=True)
    st.markdown(
        '<div class="alert alert-info">Upload a <strong>PDF</strong> or <strong>DOCX</strong> file containing software requirements. '
        'The system will extract individual requirements, validate each one, and generate test cases automatically.</div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded is not None:
        if st.button("🚀  Analyse Document", use_container_width=False):
            try:
                from doc_parser import extract_requirements_from_file
            except ImportError:
                st.error("doc_parser module not found.")
                st.stop()

            file_bytes = uploaded.read()
            filename   = uploaded.name

            with st.spinner("Extracting requirements from " + filename + "…"):
                try:
                    raw_reqs = extract_requirements_from_file(filename, file_bytes)
                except Exception as ex:
                    st.markdown('<div class="alert alert-err">❌ ' + str(ex) + '</div>', unsafe_allow_html=True)
                    st.stop()

            if not raw_reqs:
                st.markdown(
                    '<div class="alert alert-warn">⚠️ No requirements were detected in the document. '
                    'Make sure your document uses obligation keywords like "must", "shall", or "should".</div>',
                    unsafe_allow_html=True,
                )
                st.stop()

            st.markdown(
                '<div class="alert alert-ok">✅ Extracted <strong>' + str(len(raw_reqs)) + '</strong> requirement(s) from ' + filename + '.</div>',
                unsafe_allow_html=True,
            )

            batch_results = []
            progress_bar  = st.progress(0)

            for i, raw in enumerate(raw_reqs):
                req = req_ctrl.submit(raw, source=filename)
                vr  = req_ctrl.validate(req)
                tcs = []
                if vr["valid"]:
                    try:
                        tcs = tc_ctrl.generate(req)
                    except Exception:
                        pass
                batch_results.append({"req": req, "val": vr, "tcs": tcs})
                progress_bar.progress((i + 1) / len(raw_reqs))

            st.session_state.batch_results = batch_results
            st.rerun()

    # ── Display batch results ─────────────────────────────────────────────────
    if st.session_state.batch_results:
        results = st.session_state.batch_results
        valid_count   = sum(1 for r in results if r["val"]["valid"])
        invalid_count = len(results) - valid_count
        total_tcs     = sum(len(r["tcs"]) for r in results)

        st.markdown("---")
        ma, mb, mc, md = st.columns(4)
        ma.metric("Requirements Found", len(results))
        mb.metric("✅ Valid",            valid_count)
        mc.metric("❌ Invalid",          invalid_count)
        md.metric("🧪 Test Cases Generated", total_tcs)

        st.markdown("---")

        for r in results:
            req = r["req"]
            vr  = r["val"]
            tcs = r["tcs"]
            status_icon = "✅" if vr["valid"] else "❌"
            with st.expander(
                status_icon + " REQ-" + str(req.req_id).zfill(3) +
                "  |  Score: " + str(vr["score"]) + "/100  |  " +
                req.description[:80] + ("…" if len(req.description) > 80 else ""),
                expanded=False,
            ):
                _render_val_result(vr, compact=True)
                if tcs:
                    st.markdown("**" + str(len(tcs)) + " test case(s) generated:**")
                    pos = [t for t in tcs if t["type"] == "Positive"]
                    neg = [t for t in tcs if t["type"] == "Negative"]
                    st.markdown("✅ " + str(len(pos)) + " Positive · ❌ " + str(len(neg)) + " Negative")
                    for tc in tcs:
                        _render_tc(tc)
                else:
                    st.markdown('<div class="alert alert-warn">⚠️ No test cases generated (requirement was invalid).</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📥 Export All")
        col_a, col_b = st.columns(2)
        with col_a:
            try:
                all_csv = exp_ctrl.export_csv()
                st.download_button("⬇️  All Test Cases (CSV)", data=all_csv,
                                   file_name="all_test_cases.csv", mime="text/csv")
            except ValueError:
                st.info("No valid test cases to export yet.")
        with col_b:
            trace_csv = exp_ctrl.export_traceability_csv()
            st.download_button("⬇️  Traceability Matrix (CSV)", data=trace_csv,
                               file_name="traceability_matrix.csv", mime="text/csv")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — TRACEABILITY MATRIX
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_trace:
    st.markdown('<div class="card"><h3>🔗 Requirement ↔ Test Case Traceability Matrix</h3>', unsafe_allow_html=True)

    all_reqs = st.session_state.req_repo.all()
    tc_by_req = st.session_state.tc_repo.all_by_req()

    if not all_reqs:
        st.markdown(
            '<div class="alert alert-info">No requirements yet. Validate at least one requirement in the other tabs to populate this matrix.</div>',
            unsafe_allow_html=True,
        )
    else:
        rows_html = ""
        for req in all_reqs:
            tcs  = tc_by_req.get(req.req_id, [])
            pos  = len([t for t in tcs if t["type"] == "Positive"])
            neg  = len([t for t in tcs if t["type"] == "Negative"])
            ids  = ", ".join(t.get("id","") for t in tcs[:5])
            if len(tcs) > 5:
                ids += "…"
            status_badge = (
                '<span style="color:#5ecb82;font-weight:600;">VALID</span>'
                if req.status == "valid" else
                '<span style="color:#e07080;font-weight:600;">INVALID</span>'
                if req.status == "invalid" else
                '<span style="color:#e0a050;font-weight:600;">PENDING</span>'
            )
            score_html = str(req.score) + "/100" if req.score is not None else "—"
            rows_html += (
                "<tr>"
                "<td><span style='font-family:JetBrains Mono,monospace;font-size:.8rem;color:#555868;'>REQ-" + str(req.req_id).zfill(3) + "</span></td>"
                "<td>" + req.description[:70] + ("…" if len(req.description) > 70 else "") + "</td>"
                "<td>" + status_badge + "</td>"
                "<td>" + score_html + "</td>"
                "<td>" + str(len(tcs)) + "</td>"
                "<td style='color:#5ecb82'>" + str(pos) + "</td>"
                "<td style='color:#e07080'>" + str(neg) + "</td>"
                "<td style='font-family:JetBrains Mono,monospace;font-size:.76rem;color:#404358'>" + (ids or "—") + "</td>"
                "</tr>"
            )

        st.markdown(
            "<table class='trace-table'>"
            "<thead><tr>"
            "<th>REQ ID</th><th>Requirement (truncated)</th><th>Status</th>"
            "<th>Score</th><th>Total TCs</th><th>Positive</th><th>Negative</th><th>TC IDs</th>"
            "</tr></thead>"
            "<tbody>" + rows_html + "</tbody>"
            "</table>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            trace_csv = exp_ctrl.export_traceability_csv()
            st.download_button("⬇️  Export Traceability Matrix (CSV)",
                               data=trace_csv, file_name="traceability_matrix.csv", mime="text/csv")
        with col_b:
            try:
                all_tc_csv = exp_ctrl.export_csv()
                st.download_button("⬇️  Export All Test Cases (CSV)",
                                   data=all_tc_csv, file_name="all_test_cases.csv", mime="text/csv")
            except ValueError:
                pass

    if all_reqs:
        st.markdown("---")
        st.markdown("### 📊 Session Summary")
        valid_reqs  = [r for r in all_reqs if r.status == "valid"]
        all_tcs     = st.session_state.tc_repo.all()
        avg_score   = (sum(r.score for r in all_reqs if r.score is not None) // max(1, len(all_reqs)))
        sa, sb, sc, sd = st.columns(4)
        sa.metric("Requirements",  len(all_reqs))
        sb.metric("Valid / Invalid", str(len(valid_reqs)) + " / " + str(len(all_reqs) - len(valid_reqs)))
        sc.metric("Total Test Cases", len(all_tcs))
        sd.metric("Avg Quality Score", str(avg_score) + "/100")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  AI-Assisted Requirement Tool v2 &nbsp;·&nbsp;
  Built with Python + Streamlit
</div>
""", unsafe_allow_html=True)
