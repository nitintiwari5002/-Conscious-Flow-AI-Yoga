import streamlit as st
from utils.ollama_client import get_pose_info
from duckduckgo_search import DDGS


# -------------------------------
# DuckDuckGo video helper
# -------------------------------
@st.cache_data(show_spinner=False, ttl=60 * 60)
def fetch_video_ddg(name: str):
    """
    Fetch a yoga pose video URL for the given asana name using DuckDuckGo.
    Returns a single HTTPS video URL or None.
    """
    query = f"{name} yoga pose"
    try:
        results = list(
            DDGS().videos(
                keywords=query,
                region="in-en",
                safesearch="moderate",
                timelimit=None,
                max_results=5,
            )
        )
    except Exception:
        return None

    if not results:
        return None

    # Prefer the actual video URL from 'content' / 'href', fallback to thumbnail
    for r in results:
        url = r.get("content") or r.get("href") or r.get("thumbnail")
        if not url:
            continue
        if not url.startswith("http"):
            continue
        if "base64," in url:
            continue
        return url

    return None


# -------------------------------
# Fallback pose info (no Ollama)
# -------------------------------
def get_pose_fallback_info(pose_name: str) -> str:
    """
    Fallback pose information when Ollama is unavailable.
    Returns structured HTML content.
    """
    pose_data = {
        "downwarddog": {
            "title": "Adho Mukha Svanasana (Downward Dog)",
            "benefits": "Strengthens arms and legs, stretches hamstrings, calves, and back, and calms the mind.",
            "level": "Beginner–Intermediate",
            "duration": "30–60 seconds",
        },
        "warriori": {
            "title": "Virabhadrasana I (Warrior I)",
            "benefits": "Strengthens legs, opens hips and chest, and improves focus and stamina.",
            "level": "Beginner",
            "duration": "20–40 seconds per side",
        },
        "treepose": {
            "title": "Vrikshasana (Tree Pose)",
            "benefits": "Improves balance and concentration, strengthens ankles and inner thighs.",
            "level": "Beginner",
            "duration": "20–45 seconds per side",
        },
        "childspose": {
            "title": "Balasana (Child's Pose)",
            "benefits": "Relieves back and neck tension and calms the nervous system.",
            "level": "Beginner",
            "duration": "1–3 minutes",
        },
        "tadasana": {
            "title": "Tadasana (Mountain Pose)",
            "benefits": "Improves posture and body awareness and acts as a foundation for standing poses.",
            "level": "Beginner",
            "duration": "30–60 seconds",
        },
        "savasana": {
            "title": "Savasana (Corpse Pose)",
            "benefits": "Provides deep relaxation and stress relief and integrates the practice.",
            "level": "All levels",
            "duration": "5–10 minutes",
        },
    }

    normalized = (
        pose_name.lower()
        .strip()
        .replace("’", "")
        .replace("'", "")
        .replace("-", "")
        .replace(" ", "")
    )

    if normalized in pose_data:
        data = pose_data[normalized]
        return f"""
        <div style="font-size: 1.05rem; line-height: 1.6;">
            <div style="font-weight: 700; color: #1e40af; font-size: 1.15rem; margin-bottom: 0.8rem;">
                {data['title']}
            </div>
            <div style="margin-bottom: 1rem; color: #0f172a;">
                <strong>✨ Key Benefits:</strong> {data['benefits']}
            </div>
            <div style="display: flex; gap: 1.5rem; font-size: 0.95rem; color: #475569;">
                <div><strong>Level:</strong> {data['level']}</div>
                <div><strong>Hold:</strong> {data['duration']}</div>
            </div>
            <div style="margin-top: 1.2rem; padding: 1rem; background: rgba(99, 102, 241, 0.08); border-radius: 12px; font-size: 0.92rem; color: #3730a3;">
                💡 <strong>Tip:</strong> Breathe deeply and focus on alignment for maximum benefits.
            </div>
        </div>
        """

    return f"""
    <div style="text-align: center; padding: 2rem; color: #64748b;">
        <div style="font-size: 1.3rem; margin-bottom: 1rem;">🧘 {pose_name.title()}</div>
        <div style="font-size: 1.05rem; line-height: 1.6; max-width: 280px; margin: 0 auto;">
            A yoga pose that can support strength, flexibility, and mindfulness.
            <br><br>
            <strong>General Benefits:</strong> Improves posture, reduces stress, and enhances body awareness.
        </div>
        <div style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;">
            Detailed insights will appear here when the Ollama backend is available.
        </div>
    </div>
    """


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

    .video-status {
        text-align: center;
        padding: 2.5rem 2rem;
        color: #64748b;
        font-size: 1.05rem;
    }

    .no-video {
        background: rgba(248, 250, 252, 0.92);
        border-radius: 22px;
        padding: 2.5rem 2rem;
        border: 1px dashed rgba(148, 163, 184, 0.7);
    }

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

    .footer-bar {
        text-align: center;
        padding: 3rem 1.5rem 2.5rem 1.5rem;
        color: #64748b;
        font-size: 0.95rem;
        background: rgba(255, 255, 255, 0.85);
        border-top: 1px solid rgba(226, 232, 240, 0.9);
        margin-top: 1.5rem;
    }

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
# Sidebar input
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

    # LEFT: video
    with col1:
        with st.spinner("🎬 Fetching pose video..."):
            video_url = fetch_video_ddg(selected_pose)

        if video_url:
            st.video(video_url)
        else:
            st.markdown(
                """
                <div class="video-status no-video">
                    <strong>Could not load a video for this pose.</strong><br>
                    Try a different spelling, another asana name, or check your internet connection.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # RIGHT: AI insights with Ollama + fallback
    with col2:
        st.markdown('<div class="ai-insights">', unsafe_allow_html=True)
        st.markdown(
            '<h3 class="insights-title">AI Pose Insights</h3>',
            unsafe_allow_html=True,
        )

        try:
            with st.spinner(f"🤖 Analyzing {selected_pose} with Ollama..."):
                pose_info = get_pose_info(selected_pose)
            st.markdown(pose_info, unsafe_allow_html=True)
        except Exception:
            st.warning(
                "Ollama is not reachable right now. Showing basic pose information instead."
            )
            with st.spinner(f"ℹ️ Loading basic info for {selected_pose}..."):
                pose_info = get_pose_fallback_info(selected_pose)
            st.markdown(pose_info, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # pose-viewer
    st.markdown("</div>", unsafe_allow_html=True)  # main-content


# -------------------------------
# Footer
# -------------------------------
st.markdown(
    """
    <div class="footer-bar">
        Conscious Flow - Powered by Ollama phi3-mini & Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
