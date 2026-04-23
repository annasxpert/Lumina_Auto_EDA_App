# =============================================================================
#  LUMINA — Luminous Data Intelligence Studio
#  Automated Exploratory Data Analysis · Streamlit
# =============================================================================
#  Run locally:
#    pip install streamlit pandas numpy matplotlib seaborn plotly scipy openpyxl
#    streamlit run app.py
# =============================================================================

import io
import warnings

import matplotlib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import seaborn as sns
import streamlit as st

warnings.filterwarnings("ignore")
matplotlib.use("Agg")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LUMINA · Data Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL THEME & CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

:root {
    --bg-base:      #07090f;
    --bg-surface:   #0e1118;
    --bg-elevated:  #141824;
    --bg-card:      #1a1f2e;
    --border:       #252d42;
    --border-soft:  #1e2538;
    --accent:       #5b8dee;
    --accent-2:     #7c3aed;
    --accent-glow:  rgba(91,141,238,0.18);
    --success:      #10d48e;
    --warning:      #f59e0b;
    --danger:       #f43f5e;
    --text-primary: #e8edf8;
    --text-muted:   #6b7a9f;
    --text-dim:     #3d4b6e;
    --mono:         'JetBrains Mono', monospace;
}

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
}
.stApp {
    background: var(--bg-base);
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(91,141,238,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 80%, rgba(124,58,237,0.05) 0%, transparent 50%);
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
div[data-testid="metric-container"]:hover { border-color: var(--accent); }
div[data-testid="metric-container"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2));
}
div[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}
div[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] [data-testid="metric-delta"] {
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
    color: white !important; border: none;
    border-radius: 8px; padding: 0.5rem 1.5rem;
    font-weight: 600; font-size: 0.9rem;
    letter-spacing: 0.02em;
    box-shadow: 0 4px 15px rgba(91,141,238,0.3);
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(91,141,238,0.45);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-elevated);
    border-radius: 10px; padding: 4px;
    border: 1px solid var(--border-soft);
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px; padding: 0.5rem 1rem;
    color: var(--text-muted) !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
}

/* ── DataFrames ── */
.stDataFrame, .stDataFrame > div { border-radius: 10px; overflow: hidden; }

/* ── Inputs ── */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--bg-elevated) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
}
.stSlider > div > div > div { background: var(--accent) !important; }
.stRadio > div { gap: 0.5rem; }
.stRadio > div > label {
    background: var(--bg-elevated);
    border: 1px solid var(--border-soft);
    border-radius: 8px; padding: 0.35rem 0.9rem;
    font-size: 0.85rem; cursor: pointer;
    transition: all 0.15s;
}
.stRadio > div > label:hover { border-color: var(--accent); }
[data-testid="stMarkdownContainer"] { color: var(--text-primary); }
hr { border-color: var(--border-soft) !important; }

/* ── Custom classes ── */
.lumina-section {
    display: flex; align-items: center; gap: 0.6rem;
    font-size: 1.15rem; font-weight: 700;
    color: var(--text-primary);
    border-left: 3px solid var(--accent);
    padding: 0.6rem 0 0.6rem 1rem;
    margin: 0.5rem 0 1.2rem;
    background: linear-gradient(90deg, var(--accent-glow), transparent);
    border-radius: 0 8px 8px 0;
}

.info-chip {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--accent);
    margin: 0.2rem;
}

.stat-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-ok      { background: rgba(16,212,142,0.12); color: var(--success); border: 1px solid rgba(16,212,142,0.25); }
.badge-warn    { background: rgba(245,158,11,0.12); color: var(--warning); border: 1px solid rgba(245,158,11,0.25); }
.badge-danger  { background: rgba(244,63,94,0.12);  color: var(--danger);  border: 1px solid rgba(244,63,94,0.25); }

.sidebar-section-title {
    font-size: 0.68rem; font-weight: 700;
    color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 0.12em;
    padding: 0.8rem 0 0.4rem;
}

.tag-num { background: rgba(91,141,238,0.12); color: #79a8ff; border: 1px solid rgba(91,141,238,0.2); border-radius:5px; padding:1px 7px; font-size:0.78rem; }
.tag-cat { background: rgba(124,58,237,0.12); color: #c4a1ff; border: 1px solid rgba(124,58,237,0.2); border-radius:5px; padding:1px 7px; font-size:0.78rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PLOTLY DARK TEMPLATE OVERRIDE
# ─────────────────────────────────────────────────────────────────────────────
CHART_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(14,17,24,0.6)",
    font=dict(family="Outfit", color="#c8d4f0"),
    margin=dict(t=50, b=30, l=20, r=20),
    xaxis=dict(gridcolor="#1e2538", linecolor="#252d42"),
    yaxis=dict(gridcolor="#1e2538", linecolor="#252d42"),
)
ACCENT_SEQ  = ["#5b8dee","#7c3aed","#10d48e","#f59e0b","#f43f5e","#06b6d4","#ec4899","#84cc16"]
ACCENT_CONT = [[0,"#1a0533"],[0.25,"#4a1d96"],[0.5,"#5b8dee"],[0.75,"#10d48e"],[1,"#ecfdf5"]]

# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def sec(emoji_title: str):
    st.markdown(f'<div class="lumina-section">{emoji_title}</div>', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_csv(b: bytes, sep: str, enc: str) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(b), sep=sep, encoding=enc)

def num_cols(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=np.number).columns.tolist()

def cat_cols(df: pd.DataFrame) -> list[str]:
    return df.select_dtypes(include=["object","category","bool"]).columns.tolist()

def to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

def apply_layout(fig, height=380, **kw):
    fig.update_layout(height=height, **CHART_LAYOUT, **kw)
    return fig

def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5):
    """Return boolean mask — True means outlier (IQR method)."""
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - multiplier * iqr) | (series > q3 + multiplier * iqr)

def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0):
    """Return boolean mask — True means outlier (Z-score method)."""
    z = np.abs(stats.zscore(series.dropna()))
    mask = pd.Series(False, index=series.index)
    mask.iloc[series.dropna().index] = z > threshold
    return mask

def outlier_summary(df: pd.DataFrame, method: str, param: float) -> pd.DataFrame:
    rows = []
    for c in num_cols(df):
        s = df[c].dropna()
        if method == "IQR":
            mask = detect_outliers_iqr(s, param)
        else:
            mask = detect_outliers_zscore(s, param)
        n_out = mask.sum()
        pct   = n_out / len(s) * 100
        q1,q3 = s.quantile(0.25), s.quantile(0.75)
        iqr   = q3 - q1
        rows.append({
            "Column": c,
            "Total": len(s),
            "Outliers": n_out,
            "% Outliers": round(pct, 2),
            "Min": round(s.min(), 3),
            "Max": round(s.max(), 3),
            "IQR": round(iqr, 3),
            "Lower Fence": round(q1 - 1.5*iqr, 3),
            "Upper Fence": round(q3 + 1.5*iqr, 3),
            "Severity": "🔴 High" if pct > 10 else ("🟡 Medium" if pct > 3 else "🟢 Low"),
        })
    return pd.DataFrame(rows).sort_values("% Outliers", ascending=False)

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0 1rem;">
        <div style="font-size:1.8rem;font-weight:800;letter-spacing:-1px;
             background:linear-gradient(135deg,#5b8dee,#10d48e);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            ✦ LUMINA
        </div>
        <div style="font-size:0.72rem;color:#6b7a9f;letter-spacing:0.18em;text-transform:uppercase;margin-top:2px;">
            Data Intelligence Studio
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<p class="sidebar-section-title">📁 Dataset</p>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    st.divider()
    st.markdown('<p class="sidebar-section-title">⚙️ Parse Options</p>', unsafe_allow_html=True)
    sep = st.selectbox("Delimiter", [",", ";", "|", "\\t"], label_visibility="collapsed")
    sep = "\t" if sep == "\\t" else sep
    enc = st.selectbox("Encoding", ["utf-8","latin-1","iso-8859-1"], label_visibility="collapsed")

    st.divider()
    st.markdown('<p class="sidebar-section-title">🔍 Sections</p>', unsafe_allow_html=True)
    s_overview = st.checkbox("📋 Data Overview",         value=True)
    s_missing  = st.checkbox("❓ Missing Values",         value=True)
    s_stats    = st.checkbox("📊 Statistical Summary",   value=True)
    s_outlier  = st.checkbox("🎯 Outlier Detection",     value=True)
    s_numviz   = st.checkbox("📈 Numerical Plots",       value=True)
    s_catviz   = st.checkbox("🗂️  Categorical Plots",    value=True)
    s_corr     = st.checkbox("🔗 Correlation Analysis",  value=True)
    s_custom   = st.checkbox("🎛️  Custom Visualizer",    value=True)
    s_extra    = st.checkbox("🧹 Cleanup & Export",      value=True)

    st.divider()
    st.markdown('<p style="font-size:0.7rem;color:#3d4b6e;text-align:center;">Built with Streamlit · Plotly · SciPy</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  HERO BANNER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #0e1a3a 0%, #111827 50%, #0f1928 100%);
    border: 1px solid #1e2d52;
    border-radius: 18px;
    padding: 2.8rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), inset 0 1px 0 rgba(91,141,238,0.2);
">
    <div style="
        position:absolute;top:0;left:0;right:0;height:3px;
        background:linear-gradient(90deg,#5b8dee,#7c3aed,#10d48e,#5b8dee);
        background-size:200% 100%;
    "></div>
    <div style="
        position:absolute;top:-60px;right:-60px;width:220px;height:220px;
        background:radial-gradient(circle,rgba(91,141,238,0.12) 0%,transparent 70%);
        border-radius:50%;
    "></div>
    <div style="position:relative;">
        <div style="
            font-size:0.72rem;font-weight:700;letter-spacing:0.22em;
            color:#5b8dee;text-transform:uppercase;margin-bottom:0.6rem;
        ">✦ Exploratory Data Analysis Studio</div>
        <div style="
            font-size:3rem;font-weight:800;letter-spacing:-2px;line-height:1;
            background:linear-gradient(135deg,#e8edf8 0%,#a8c0f0 50%,#10d48e 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            margin-bottom:0.8rem;
        ">LUMINA</div>
        <div style="font-size:1rem;color:#6b7a9f;max-width:540px;line-height:1.6;">
            Upload any CSV dataset and get instant, deeply interactive analysis —
            statistics, outliers, correlations, and custom visualizations. No code required.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  LANDING (no file)
# ─────────────────────────────────────────────────────────────────────────────
if uploaded is None:
    st.markdown("""
    <div style="
        background:linear-gradient(135deg,rgba(91,141,238,0.06),rgba(124,58,237,0.04));
        border:1px dashed #252d42;border-radius:14px;
        padding:2.5rem;text-align:center;margin:1rem 0;
    ">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">📂</div>
        <div style="font-size:1.1rem;font-weight:600;color:#a8c0f0;margin-bottom:0.4rem;">
            Upload a CSV to get started
        </div>
        <div style="font-size:0.85rem;color:#6b7a9f;">
            Use the file uploader in the left sidebar to load your dataset
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    features = [
        ("📋", "Data Overview", "Shape, dtypes, head/tail preview, unique counts"),
        ("❓", "Missing Values", "Per-column counts with bar & pie visualisations"),
        ("📊", "Statistics", "Mean, median, std, skewness, kurtosis per column"),
        ("🎯", "Outlier Detection", "IQR & Z-score methods with visual flagging"),
        ("📈", "Numerical Plots", "Histogram / Box / Violin auto-grid layout"),
        ("🗂️", "Categorical Plots", "Bar / Pie / Treemap with frequency counts"),
        ("🔗", "Correlation", "Heatmap, pair plot, high-correlation alerts"),
        ("🎛️", "Custom Charts", "Pick any X, Y, colour + 8 chart types"),
        ("🧹", "Clean & Export", "Drop dupes/nulls, impute, download cleaned CSV"),
    ]
    for i, (emoji, title, desc) in enumerate(features):
        col = [col1, col2, col3][i % 3]
        col.markdown(f"""
        <div style="
            background:#0e1118;border:1px solid #1e2538;border-radius:12px;
            padding:1.2rem;margin-bottom:0.8rem;
        ">
            <div style="font-size:1.4rem;margin-bottom:0.4rem;">{emoji}</div>
            <div style="font-weight:600;font-size:0.95rem;color:#a8c0f0;margin-bottom:0.3rem;">{title}</div>
            <div style="font-size:0.8rem;color:#6b7a9f;line-height:1.5;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner("✦  Parsing dataset …"):
    try:
        df = load_csv(uploaded.getvalue(), sep, enc)
    except Exception as e:
        st.error(f"❌  Could not parse file — {e}")
        st.stop()

NC = num_cols(df)
CC = cat_cols(df)

# ─────────────────────────────────────────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    background:#0e1118;border:1px solid #1e2538;border-radius:12px;
    padding:0.9rem 1.5rem;margin-bottom:1.2rem;
    display:flex;align-items:center;gap:0.6rem;flex-wrap:wrap;
">
    <span style="font-size:0.7rem;color:#3d4b6e;text-transform:uppercase;letter-spacing:.12em;font-weight:700;margin-right:.4rem;">
        {uploaded.name}
    </span>
    <span class="info-chip">⬛ {df.shape[0]:,} rows</span>
    <span class="info-chip">⬛ {df.shape[1]:,} cols</span>
    <span class="info-chip">🔵 {len(NC)} numerical</span>
    <span class="info-chip">🟣 {len(CC)} categorical</span>
    <span class="info-chip">⚠ {df.isnull().mean().mean()*100:.1f}% missing</span>
    <span class="info-chip">🔁 {df.duplicated().sum():,} duplicates</span>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Rows",         f"{df.shape[0]:,}")
k2.metric("Columns",      f"{df.shape[1]:,}")
k3.metric("Numerical",    len(NC))
k4.metric("Categorical",  len(CC))
k5.metric("Missing %",    f"{df.isnull().mean().mean()*100:.1f}%")
k6.metric("Duplicates",   f"{df.duplicated().sum():,}")
st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  1. DATA OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if s_overview:
    sec("📋  Data Overview")
    n = st.slider("Rows to preview", 5, min(100, len(df)), 10, key="prev")
    t1, t2, t3 = st.tabs(["🔼 Head", "🔽 Tail", "🧬 Schema"])

    with t1:
        st.dataframe(df.head(n), use_container_width=True, height=300)
    with t2:
        st.dataframe(df.tail(n), use_container_width=True, height=300)
    with t3:
        schema = pd.DataFrame({
            "Column":        df.columns,
            "Dtype":         df.dtypes.astype(str).values,
            "Non-Null":      df.notnull().sum().values,
            "Null":          df.isnull().sum().values,
            "% Null":        (df.isnull().mean()*100).round(1).values,
            "Unique":        df.nunique().values,
            "% Unique":      (df.nunique()/len(df)*100).round(1).values,
            "Sample":        [str(df[c].dropna().iloc[0]) if df[c].notnull().any() else "—" for c in df.columns],
        })
        st.dataframe(schema, use_container_width=True, height=350)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Numerical columns**")
        st.markdown(" ".join(f'<span class="tag-num">{c}</span>' for c in NC) if NC else "_none_", unsafe_allow_html=True)
    with c2:
        st.markdown("**Categorical columns**")
        st.markdown(" ".join(f'<span class="tag-cat">{c}</span>' for c in CC) if CC else "_none_", unsafe_allow_html=True)
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  2. MISSING VALUES
# ─────────────────────────────────────────────────────────────────────────────
if s_missing:
    sec("❓  Missing Values Analysis")
    mv = pd.DataFrame({
        "Column":    df.columns,
        "Missing":   df.isnull().sum().values,
        "% Missing": (df.isnull().mean()*100).round(2).values,
        "Present":   df.notnull().sum().values,
    }).sort_values("Missing", ascending=False)

    cols_mv = mv[mv["Missing"] > 0]

    if cols_mv.empty:
        st.success("✅  Dataset is complete — no missing values detected.")
    else:
        st.markdown(f"**{len(cols_mv)}** column(s) contain missing values &nbsp;·&nbsp; **{df.isnull().sum().sum():,}** cells total")
        st.dataframe(
            mv.style.background_gradient(subset=["% Missing"], cmap="Reds").format({"% Missing": "{:.2f}%"}),
            use_container_width=True, height=300,
        )
        m1, m2 = st.columns(2)
        with m1:
            fig = go.Figure(go.Bar(
                x=cols_mv["Column"], y=cols_mv["% Missing"],
                marker=dict(
                    color=cols_mv["% Missing"],
                    colorscale=[[0,"#1e3a5f"],[0.5,"#5b8dee"],[1,"#f43f5e"]],
                    showscale=False,
                    line=dict(width=0),
                ),
                text=cols_mv["% Missing"].apply(lambda v: f"{v:.1f}%"),
                textposition="outside",
            ))
            fig.update_layout(title="Missing % per Column", **CHART_LAYOUT, height=360)
            st.plotly_chart(fig, use_container_width=True)
        with m2:
            total = df.shape[0]*df.shape[1]
            total_mv = df.isnull().sum().sum()
            fig = go.Figure(go.Pie(
                labels=["Missing","Present"],
                values=[total_mv, total-total_mv],
                hole=0.55,
                marker_colors=["#f43f5e","#10d48e"],
                textfont=dict(family="Outfit"),
            ))
            fig.update_layout(title="Data Completeness", **CHART_LAYOUT, height=360)
            st.plotly_chart(fig, use_container_width=True)
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  3. STATISTICAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
if s_stats and NC:
    sec("📊  Statistical Summary")
    desc = df[NC].describe().T
    desc["median"]   = df[NC].median()
    desc["skewness"] = df[NC].skew()
    desc["kurtosis"] = df[NC].kurtosis()
    desc["IQR"]      = df[NC].quantile(0.75) - df[NC].quantile(0.25)
    desc = desc[["count","mean","median","std","IQR","min","25%","75%","max","skewness","kurtosis"]]
    desc.columns = ["Count","Mean","Median","Std","IQR","Min","Q1","Q3","Max","Skewness","Kurtosis"]

    st.dataframe(
        desc.style
            .background_gradient(subset=["Mean","Std"], cmap="Blues")
            .format("{:.3f}"),
        use_container_width=True, height=350,
    )

    sk_col, kurt_col = st.columns(2)
    with sk_col:
        st.markdown("**Skewness**")
        sk_df = desc[["Skewness"]].copy()
        sk_df["Label"] = sk_df["Skewness"].apply(
            lambda x: "✅ Symmetric" if abs(x)<0.5 else ("⚠️ Moderate" if abs(x)<1 else "🔴 High Skew"))
        st.dataframe(sk_df, use_container_width=True)
    with kurt_col:
        st.markdown("**Kurtosis** (>3 = heavy tails)")
        ku_df = desc[["Kurtosis"]].copy()
        ku_df["Label"] = ku_df["Kurtosis"].apply(
            lambda x: "✅ Normal" if abs(x-3)<1 else ("⚠️ Moderate" if abs(x-3)<3 else "🔴 Heavy Tails"))
        st.dataframe(ku_df, use_container_width=True)
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  4. OUTLIER DETECTION  ★ NEW SECTION ★
# ─────────────────────────────────────────────────────────────────────────────
if s_outlier and NC:
    sec("🎯  Outlier Detection")

    # ── Config ────────────────────────────────────────────────────────────────
    oc1, oc2, oc3 = st.columns([1.2, 1.2, 2])
    with oc1:
        method = st.radio("Detection method", ["IQR", "Z-Score"], horizontal=True, key="out_method")
    with oc2:
        if method == "IQR":
            param = st.slider("IQR multiplier", 1.0, 3.0, 1.5, 0.1, key="iqr_k",
                              help="Lower = more aggressive. Standard = 1.5")
        else:
            param = st.slider("Z-Score threshold", 1.5, 4.0, 3.0, 0.1, key="zscore_k",
                              help="Lower = more aggressive. Standard = 3.0")
    with oc3:
        out_cols = st.multiselect("Columns to analyse", NC, default=NC[:min(8,len(NC))], key="out_cols")

    if not out_cols:
        st.info("Select at least one numerical column above.")
    else:
        df_out = df[out_cols]

        # ── Summary table ─────────────────────────────────────────────────────
        summary = outlier_summary(df_out, method, param)
        total_out = summary["Outliers"].sum()
        pct_out   = total_out / (len(df) * len(out_cols)) * 100

        ks1, ks2, ks3, ks4 = st.columns(4)
        ks1.metric("Columns Checked",  len(out_cols))
        ks2.metric("Total Outliers",   f"{total_out:,}")
        ks3.metric("Outlier Rate",     f"{pct_out:.2f}%")
        ks4.metric("Most Affected",    summary.iloc[0]["Column"] if not summary.empty else "—")

        st.markdown("**Outlier Summary Table**")
        def color_severity(val):
            if "High"   in str(val): return "color:#f43f5e;font-weight:600"
            if "Medium" in str(val): return "color:#f59e0b;font-weight:600"
            if "Low"    in str(val): return "color:#10d48e;font-weight:600"
            return ""
        st.dataframe(
            summary.style
                .background_gradient(subset=["% Outliers"], cmap="Reds")
                .applymap(color_severity, subset=["Severity"])
                .format({"% Outliers":"{:.2f}%","Min":"{:.3f}","Max":"{:.3f}",
                         "IQR":"{:.3f}","Lower Fence":"{:.3f}","Upper Fence":"{:.3f}"}),
            use_container_width=True, height=300,
        )

        # ── Outlier bar chart ─────────────────────────────────────────────────
        fig_bar = go.Figure(go.Bar(
            x=summary["Column"], y=summary["% Outliers"],
            marker=dict(
                color=summary["% Outliers"],
                colorscale=[[0,"#1e3a5f"],[0.4,"#f59e0b"],[1,"#f43f5e"]],
                showscale=True,
                colorbar=dict(title="% Out", tickfont=dict(family="Outfit")),
                line=dict(width=0),
            ),
            text=summary["% Outliers"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside",
        ))
        apply_layout(fig_bar, height=340, title=f"Outlier % per Column ({method} method)")
        st.plotly_chart(fig_bar, use_container_width=True)

        # ── Per-column deep dive ──────────────────────────────────────────────
        st.markdown("**Per-Column Outlier Visualisation**")
        viz_type = st.radio("Plot style", ["Box Plot","Strip + Outliers","Distribution Overlay"],
                            horizontal=True, key="out_viz")

        n_cols_grid = 3
        for i in range(0, len(out_cols), n_cols_grid):
            chunk = out_cols[i:i+n_cols_grid]
            grid  = st.columns(len(chunk))
            for col, gcol in zip(chunk, grid):
                with gcol:
                    s = df[col].dropna()
                    if method == "IQR":
                        mask = detect_outliers_iqr(s, param)
                    else:
                        mask = detect_outliers_zscore(s, param)

                    inliers  = s[~mask]
                    outliers = s[mask]
                    n_out    = mask.sum()

                    if viz_type == "Box Plot":
                        fig = go.Figure()
                        fig.add_trace(go.Box(
                            y=s, name=col, boxpoints="suspectedoutliers",
                            marker_color="#5b8dee",
                            marker=dict(outliercolor="#f43f5e", size=5),
                            line=dict(color="#5b8dee"),
                        ))
                        apply_layout(fig, height=300, title=f"{col}<br><sup>{n_out} outliers</sup>",
                                     showlegend=False)

                    elif viz_type == "Strip + Outliers":
                        fig = go.Figure()
                        fig.add_trace(go.Box(y=s, name="", boxpoints=False,
                                             marker_color="#5b8dee", line=dict(color="#3d5fa0"),
                                             fillcolor="rgba(91,141,238,0.08)", showlegend=False))
                        fig.add_trace(go.Scatter(
                            x=["inlier"]*len(inliers), y=inliers,
                            mode="markers", name="Inlier",
                            marker=dict(color="#10d48e", size=4, opacity=0.5),
                        ))
                        if len(outliers):
                            fig.add_trace(go.Scatter(
                                x=["outlier"]*len(outliers), y=outliers,
                                mode="markers", name="Outlier",
                                marker=dict(color="#f43f5e", size=7, symbol="x",
                                            line=dict(width=1, color="#ff6b6b")),
                            ))
                        apply_layout(fig, height=300, title=f"{col}<br><sup>{n_out} outliers</sup>")

                    else:  # Distribution Overlay
                        fig = go.Figure()
                        fig.add_trace(go.Histogram(
                            x=inliers, name="Inliers", nbinsx=35,
                            marker_color="#5b8dee", opacity=0.75,
                        ))
                        if len(outliers):
                            fig.add_trace(go.Histogram(
                                x=outliers, name="Outliers", nbinsx=10,
                                marker_color="#f43f5e", opacity=0.85,
                            ))
                        q1,q3 = s.quantile(0.25), s.quantile(0.75)
                        iqr   = q3-q1
                        for fence, label in [(q1-1.5*iqr,"Lower"),(q3+1.5*iqr,"Upper")]:
                            fig.add_vline(x=fence, line_dash="dash", line_color="#f59e0b",
                                          annotation_text=label, annotation_font_size=10)
                        apply_layout(fig, height=300,
                                     title=f"{col}<br><sup>{n_out} outliers ({mask.mean()*100:.1f}%)</sup>",
                                     barmode="overlay")

                    st.plotly_chart(fig, use_container_width=True)

        # ── Scatter: outlier vs inlier if 2 cols chosen ───────────────────────
        if len(out_cols) >= 2:
            st.markdown("**Outlier Scatter — compare two columns**")
            sc1, sc2 = st.columns(2)
            x_sc = sc1.selectbox("X axis", out_cols, key="osc_x")
            y_sc = sc2.selectbox("Y axis", [c for c in out_cols if c != x_sc], key="osc_y") if len(out_cols)>1 else x_sc
            if x_sc != y_sc:
                mask_x = detect_outliers_iqr(df[x_sc].dropna(), param) if method=="IQR" else detect_outliers_zscore(df[x_sc].dropna(), param)
                mask_y = detect_outliers_iqr(df[y_sc].dropna(), param) if method=="IQR" else detect_outliers_zscore(df[y_sc].dropna(), param)
                # align on common index
                combined = pd.DataFrame({"x": df[x_sc], "y": df[y_sc]}).dropna()
                combined["outlier"] = (
                    mask_x.reindex(combined.index, fill_value=False) |
                    mask_y.reindex(combined.index, fill_value=False)
                )
                combined["label"] = combined["outlier"].map({True:"Outlier", False:"Inlier"})
                fig_sc = px.scatter(
                    combined, x="x", y="y", color="label",
                    color_discrete_map={"Inlier":"#5b8dee","Outlier":"#f43f5e"},
                    labels={"x":x_sc,"y":y_sc},
                    opacity=0.7,
                    symbol="label", symbol_map={"Inlier":"circle","Outlier":"x"},
                )
                apply_layout(fig_sc, height=420, title=f"Outlier Scatter: {x_sc} vs {y_sc}")
                st.plotly_chart(fig_sc, use_container_width=True)

        # ── Option to remove outliers ─────────────────────────────────────────
        st.markdown("**🗑️  Remove Outliers from Working Dataset**")
        ro1, ro2 = st.columns([2,3])
        remove_out = ro1.checkbox(f"Remove outlier rows detected by {method} method")
        if remove_out:
            combined_mask = pd.Series(False, index=df.index)
            for c in out_cols:
                s = df[c].dropna()
                m = detect_outliers_iqr(s,param) if method=="IQR" else detect_outliers_zscore(s,param)
                combined_mask = combined_mask | m.reindex(df.index, fill_value=False)
            df = df[~combined_mask].reset_index(drop=True)
            NC = num_cols(df); CC = cat_cols(df)
            ro2.success(f"✅  Removed {combined_mask.sum():,} rows. Working dataset now has {len(df):,} rows.")

    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  5. NUMERICAL PLOTS
# ─────────────────────────────────────────────────────────────────────────────
if s_numviz and NC:
    sec("📈  Numerical Distributions")
    plot_type = st.radio("Style", ["Histogram","Box Plot","Violin Plot"],
                         horizontal=True, key="npt")
    sel = st.multiselect("Columns", NC, default=NC[:min(6,len(NC))], key="nsel")

    if sel:
        n_grid = 3
        for i in range(0, len(sel), n_grid):
            chunk = sel[i:i+n_grid]
            gcols = st.columns(len(chunk))
            for col, gcol in zip(chunk, gcols):
                with gcol:
                    if plot_type == "Histogram":
                        fig = px.histogram(df, x=col, nbins=40, title=col,
                                           color_discrete_sequence=["#5b8dee"], marginal="rug")
                    elif plot_type == "Box Plot":
                        fig = px.box(df, y=col, title=col,
                                     color_discrete_sequence=["#10d48e"], points="outliers")
                    else:
                        fig = px.violin(df, y=col, title=col,
                                        color_discrete_sequence=["#7c3aed"], box=True, points="outliers")
                    apply_layout(fig, height=300)
                    fig.update_layout(margin=dict(t=40,b=10,l=10,r=10))
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one column.")
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  6. CATEGORICAL PLOTS
# ─────────────────────────────────────────────────────────────────────────────
if s_catviz and CC:
    sec("🗂️  Categorical Distributions")
    cpt = st.radio("Style", ["Bar Chart","Pie Chart","Treemap"], horizontal=True, key="cpt")
    sel = st.multiselect("Columns", CC, default=CC[:min(4,len(CC))], key="csel")
    mx  = st.slider("Max categories per column", 5, 40, 15, key="mxc")

    if sel:
        for col in sel:
            vc = df[col].value_counts().head(mx).reset_index()
            vc.columns = ["Category","Count"]
            if cpt == "Bar Chart":
                fig = px.bar(vc, x="Category", y="Count", color="Count",
                             color_continuous_scale=ACCENT_CONT,
                             title=f"{col} — Top {mx}", text="Count")
                fig.update_traces(textposition="outside")
                fig.update_layout(coloraxis_showscale=False)
            elif cpt == "Pie Chart":
                fig = px.pie(vc, names="Category", values="Count",
                             title=f"{col}", color_discrete_sequence=ACCENT_SEQ, hole=0.38)
            else:
                fig = px.treemap(vc, path=["Category"], values="Count",
                                 title=f"{col}", color="Count",
                                 color_continuous_scale=ACCENT_CONT)
            apply_layout(fig, height=420)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select at least one column.")
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  7. CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
if s_corr and len(NC) >= 2:
    sec("🔗  Correlation Analysis")
    cm_method = st.selectbox("Method", ["pearson","spearman","kendall"], key="cmet")
    corr = df[NC].corr(method=cm_method)

    fig_heat = px.imshow(
        corr, text_auto=".2f",
        color_continuous_scale=[[0,"#f43f5e"],[0.5,"#141824"],[1,"#5b8dee"]],
        zmin=-1, zmax=1,
        title=f"{cm_method.capitalize()} Correlation Matrix",
        aspect="auto",
    )
    apply_layout(fig_heat, height=max(420, len(NC)*45+80))
    fig_heat.update_traces(textfont=dict(family="JetBrains Mono", size=10))
    st.plotly_chart(fig_heat, use_container_width=True)

    thr = st.slider("Show pairs with |r| ≥", 0.4, 1.0, 0.75, 0.05, key="cthr")
    pairs = []
    for i in range(len(corr.columns)):
        for j in range(i+1, len(corr.columns)):
            v = corr.iloc[i,j]
            if abs(v) >= thr:
                pairs.append({
                    "Column A": corr.columns[i],
                    "Column B": corr.columns[j],
                    "Correlation r": round(v,4),
                    "Strength": "🔴 Very High" if abs(v)>=0.9 else "🟠 High",
                    "Direction": "⬆️ Positive" if v>0 else "⬇️ Negative",
                })
    if pairs:
        pf = pd.DataFrame(pairs).sort_values("Correlation r", key=abs, ascending=False)
        st.markdown(f"**{len(pairs)} pair(s)** with |r| ≥ {thr}")
        st.dataframe(pf, use_container_width=True)
    else:
        st.success(f"✅  No pairs exceed the |{thr}| threshold.")

    if len(NC) <= 7 and len(df) <= 3000:
        with st.expander("🔍 Scatter Matrix (Pair Plot)"):
            fig_pair = px.scatter_matrix(
                df[NC].dropna(), dimensions=NC,
                color_discrete_sequence=["#5b8dee"],
                title="Scatter Matrix",
            )
            apply_layout(fig_pair, height=750)
            st.plotly_chart(fig_pair, use_container_width=True)
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  8. CUSTOM VISUALIZER
# ─────────────────────────────────────────────────────────────────────────────
if s_custom:
    sec("🎛️  Custom Visualizer")
    ac = df.columns.tolist()
    v1,v2,v3 = st.columns(3)
    xc = v1.selectbox("X-Axis", ac, key="vx")
    yc = v2.selectbox("Y-Axis", [None]+ac, index=0, key="vy")
    co = v3.selectbox("Colour by", [None]+ac, index=0, key="vco")
    ct = st.selectbox("Chart Type", ["Scatter","Line","Bar","Box","Violin","Histogram","Strip","Area","Bubble"], key="vct")
    ca = co or None

    try:
        if   ct=="Scatter"   and yc: fig=px.scatter(df,x=xc,y=yc,color=ca,opacity=.7,hover_data=df.columns[:5])
        elif ct=="Line"      and yc: fig=px.line(df,x=xc,y=yc,color=ca)
        elif ct=="Bar"             : fig=px.bar(df,x=xc,y=yc,color=ca)
        elif ct=="Box"             : fig=px.box(df,x=ca,y=xc,points="outliers")
        elif ct=="Violin"          : fig=px.violin(df,x=ca,y=xc,box=True,points="outliers")
        elif ct=="Histogram"       : fig=px.histogram(df,x=xc,color=ca,nbins=40,marginal="rug",barmode="overlay")
        elif ct=="Strip"     and yc: fig=px.strip(df,x=xc,y=yc,color=ca)
        elif ct=="Area"      and yc: fig=px.area(df,x=xc,y=yc,color=ca)
        elif ct=="Bubble"    and yc:
            sz_col = st.selectbox("Bubble size column", [None]+NC, key="bsz")
            fig = px.scatter(df,x=xc,y=yc,color=ca,size=sz_col if sz_col else None,opacity=.7)
        else: fig=px.histogram(df,x=xc,nbins=40)

        apply_layout(fig, height=500,
                     title=f"{ct}: {xc}" + (f" vs {yc}" if yc else ""),
                     colorway=ACCENT_SEQ)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️  Cannot render: {e}")
    st.divider()

# ─────────────────────────────────────────────────────────────────────────────
#  9. CLEANUP & EXPORT
# ─────────────────────────────────────────────────────────────────────────────
if s_extra:
    sec("🧹  Cleanup & Export")

    # Duplicate info
    n_dup = df.duplicated().sum()
    d1, d2 = st.columns([1,2])
    d1.metric("Duplicate Rows", f"{n_dup:,}", delta=f"{n_dup/len(df)*100:.2f}% of rows" if n_dup else None)
    with d2:
        if n_dup > 0:
            st.dataframe(df[df.duplicated()].head(8), use_container_width=True, height=220)
        else:
            st.success("✅  No duplicate rows found.")

    # Memory
    with st.expander("💾  Memory Usage per Column"):
        mem = pd.DataFrame({
            "Column": df.columns,
            "KB":     (df.memory_usage(deep=True)[1:]/1024).round(2).values,
            "Dtype":  df.dtypes.astype(str).values,
        }).sort_values("KB", ascending=False)
        fig_mem = px.bar(mem, x="Column", y="KB", color="KB",
                         color_continuous_scale=[[0,"#1e2538"],[1,"#7c3aed"]],
                         title="Memory Usage (KB)")
        apply_layout(fig_mem, height=300)
        fig_mem.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_mem, use_container_width=True)
        st.dataframe(mem, use_container_width=True)
    st.markdown(f"**Total Memory:** `{df.memory_usage(deep=True).sum()/1024:.1f} KB`")

    st.divider()
    st.markdown("#### 🔧 Clean & Download")
    cl1,cl2,cl3 = st.columns(3)
    dd = cl1.checkbox("Drop duplicate rows")
    dm = cl2.checkbox("Drop rows with any missing")
    fm = cl3.checkbox("Fill numeric NaN with median")

    dfc = df.copy()
    if dd:
        b=len(dfc); dfc=dfc.drop_duplicates()
        st.success(f"✅  Removed {b-len(dfc):,} duplicate rows")
    if dm:
        b=len(dfc); dfc=dfc.dropna()
        st.success(f"✅  Removed {b-len(dfc):,} rows with missing values")
    if fm:
        for c in num_cols(dfc): dfc[c]=dfc[c].fillna(dfc[c].median())
        st.success("✅  Filled numeric NaN values with column medians")

    if dd or dm or fm:
        st.markdown(f"Cleaned shape: **{dfc.shape[0]:,} rows × {dfc.shape[1]:,} cols**")
        st.dataframe(dfc.head(5), use_container_width=True)

    st.download_button(
        "⬇️  Download Cleaned Dataset",
        to_csv(dfc), "lumina_cleaned.csv", "text/csv",
        use_container_width=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;padding:2rem;
    border-top:1px solid #1e2538;margin-top:1rem;
">
    <div style="
        font-size:1.1rem;font-weight:800;letter-spacing:-0.5px;
        background:linear-gradient(135deg,#5b8dee,#10d48e);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        margin-bottom:0.3rem;
    ">✦ LUMINA</div>
    <div style="font-size:0.75rem;color:#3d4b6e;letter-spacing:0.06em;">
        Data Intelligence Studio &nbsp;·&nbsp; Streamlit · Plotly · Pandas · SciPy
    </div>
</div>
""", unsafe_allow_html=True)