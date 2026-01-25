import streamlit as st
from utils.ollama_client import get_pose_info
from duckduckgo_search import DDGS


# -------------------------------
# DuckDuckGo image helper
# -------------------------------
@st.cache_data(show_spinner=False, ttl=60 * 60)
def fetch_image_ddg(name: str):
    """
    Fetch a yoga pose image URL for the given asana name using DuckDuckGo.
    Returns a single HTTPS image URL or None.
    """
    query = f"{name} yoga pose"
    try:
        results = list(
            DDGS().images(
                keywords=query,
                region="in-en",
                safesearch="moderate",
                max_results=5,
            )
        )
    except Exception:
        return None

    if not results:
        return None

    for r in results:
        url = r.get("image") or r.get("thumbnail")
        if not url:
            continue
        if not url.startswith("http"):
            continue
        if "base64," in url:
            continue
        return url

    return None


# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Conscious Flow Yoga Poses",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------------------------
# Global CSS
# -------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== Base ===== */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #0f172a;
    }

    .main {
        background: radial-gradient(circle at top left, #e0f2fe 0, transparent 40%),
                    radial-gradient(circle at bottom right, #dcfce7 0, transparent 40%),
                    #f1f5f9;
        background-attachment: fixed;
    }

    /* ===== Header ===== */
    .app-header {
        max-width: 1100px;
        margin: 2.5rem auto 1.5rem auto;
        padding: 2.5rem 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        color: #f9fafb;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.35);
    }

    .app-header::before,
    .app-header::after {
        content: "";
        position: absolute;
        border-radius: 999px;
        filter: blur(30px);
        opacity: 0.6;
    }

    .app-header::before {
        width: 220px;
        height: 220px;
        background: rgba(248, 250, 252, 0.18);
        top: -80px;
        left: -40px;
    }

    .app-header::after {
        width: 260px;
        height: 260px;
        background: rgba(15, 23, 42, 0.18);
        bottom: -100px;
        right: -60px;
    }

    .h1-header {
        position: relative;
        font-size: clamp(2.4rem, 4vw, 3.3rem) !important;
        font-weight: 800 !important;
        letter-spacing: 0.03em;
        margin: 0 0 0.75rem 0 !important;
    }

    .subtitle-header {
        position: relative;
        font-size: clamp(1.05rem, 2vw, 1.35rem) !important;
        opacity: 0.95 !important;
    }

    /* ===== Sidebar ===== */
    .sidebar-custom {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(22px);
        padding: 2.25rem 2rem 2.5rem 2rem;
        border-radius: 22px;
        margin: 1.75rem 1.25rem;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.10);
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    .sidebar-title {
        color: white !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.3rem !important;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .sidebar-title::before {
        content: "🧘";
        font-size: 1.4rem;
    }

    .sidebar-custom label {
        font-weight: 500;
        color: yellow !important;
    }

    .sidebar-custom input {
        border-radius: 999px !important;
    }

    /* ===== Main layout ===== */
    .main-content {
        padding: 1.5rem 1.5rem 3.5rem 1.5rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .pose-title {
        color: white !important;
        font-size: clamp(2rem, 3vw, 2.6rem) !important;
        font-weight: 800 !important;
        margin: 0 0 2rem 0 !important;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .pose-title::before {
        content: "📿";
        font-size: 1.6rem;
    }

    .pose-viewer {
        display: grid;
        grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
        gap: 2.5rem;
        align-items: flex-start;
        margin-top: 1.25rem;
    }

    /* ===== Image panel ===== */
    .pose-image-large, .stImage > img {
        border-radius: 26px !important;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.35);
        object-fit: cover;
    }

    .image-status {
        text-align: center;
        padding: 2.5rem 2rem;
        color: #64748b;
        font-size: 1.05rem;
    }

    .no-image {
        background: rgba(248, 250, 252, 0.92);
        border-radius: 22px;
        padding: 2.5rem 2rem;
        border: 1px dashed rgba(148, 163, 184, 0.7);
    }

    /* ===== AI panel ===== */
    .ai-insights {
        background: linear-gradient(135deg, #ffffff 0%, #f9fafb 50%, #eff6ff 100%);
        backdrop-filter: blur(28px);
        padding: 2.5rem 2.3rem;
        border-radius: 26px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.18);
        border: 1px solid rgba(129, 140, 248, 0.35);
        position: relative;
        overflow: hidden;
    }

    .ai-insights::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at top right, rgba(129, 140, 248, 0.18) 0, transparent 55%);
        opacity: 0.8;
        pointer-events: none;
    }

    .ai-insights > * {
        position: relative;
        z-index: 1;
    }

    .insights-title {
        color: #4338ca !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.3rem !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .insights-title::before {
        content: "✨";
        font-size: 1.3rem;
    }

    /* ===== Footer ===== */
    .footer-bar {
        text-align: center;
        padding: 3rem 1.5rem 2.5rem 1.5rem;
        color: #64748b;
        font-size: 0.95rem;
        background: rgba(255, 255, 255, 0.85);
        border-top: 1px solid rgba(226, 232, 240, 0.9);
        margin-top: 1.5rem;
    }

    /* ===== Streamlit tweaks ===== */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }

    .stButton>button, .stTextInput>div>div>input {
        transition: box-shadow 0.18s ease, transform 0.12s ease, border-color 0.18s ease;
    }

    .stTextInput>div>div>input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.35);
    }

    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(15, 23, 42, 0.16);
    }

    /* ===== Responsive ===== */
    @media (max-width: 1024px) {
        .pose-viewer {
            grid-template-columns: minmax(0, 1fr);
            gap: 2rem;
        }

        .main-content {
            padding: 1.5rem 1.1rem 3rem 1.1rem;
        }

        .app-header {
            margin: 1.75rem 1rem 1.25rem 1rem;
            padding: 2.2rem 1.6rem;
        }
    }

    @media (max-width: 768px) {
        .sidebar-custom {
            margin: 1.25rem 0.9rem;
            padding: 2rem 1.6rem;
        }

        .pose-title {
            justify-content: center;
            text-align: center;
        }

        .main-content {
            padding: 1.25rem 0.9rem 2.5rem 0.9rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------------
# Header
# -------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1 class="h1-header">Conscious Flow</h1>
        <p class="subtitle-header">AI-Powered Yoga Pose Explorer</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------------------------------
# Sidebar: user inputs asana name
# -------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-custom">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">Enter Asana</h2>', unsafe_allow_html=True)

    asana_name = st.text_input(
        "Asana name",
        value="Downward Dog",
        help="Type any yoga pose name, e.g. Tadasana, Savasana, etc.",
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

selected_pose = asana_name.strip()

# -------------------------------
# Main content
# -------------------------------
if selected_pose:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown(
        f'<h2 class="pose-title">{selected_pose}</h2>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="pose-viewer">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.05, 0.95])

    # LEFT: image from DuckDuckGo
    with col1:
        with st.spinner("Fetching pose image..."):
            img_url = fetch_image_ddg(selected_pose)

        if img_url:
            st.image(
                img_url,
                caption=f"🧘 {selected_pose}",
                use_container_width=True,
            )
        else:
            st.markdown(
                """
                <div class="image-status no-image">
                    <strong>Could not load an image for this pose.</strong><br>
                    Try a different spelling, another asana name, or check your internet connection.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # RIGHT: AI insights
    with col2:
        st.markdown('<div class="ai-insights">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="insights-title">AI Pose Insights</h3>',
            unsafe_allow_html=True,
        )
        with st.spinner(f"Analyzing {selected_pose}..."):
            pose_info = get_pose_info(selected_pose)
        st.markdown(pose_info, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close pose-viewer
    st.markdown("</div>", unsafe_allow_html=True)  # close main-content


# -------------------------------
# Footer
# -------------------------------
st.markdown(
    """
    <div class="footer-bar">
        Conscious Flow – Powered by Ollama phi3-mini & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
