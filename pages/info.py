import streamlit as st
import os
from PIL import Image
from utils.ollama_client import get_pose_info

# Page config FIRST (best practice)
st.set_page_config(
    page_title="🧘 Conscious Flow: Yoga Poses",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS Framework
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.main {
    background: linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 50%, #e8f5e8 100%);
    background-size: 300% 300%;
    animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Header */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 3rem 2rem;
    text-align: center;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    position: relative;
    overflow: hidden;
}

.app-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 30% 70%, rgba(255,255,255,0.2) 0%, transparent 50%);
    animation: float 25s infinite linear;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
}

.logo-header { width: clamp(90px, 12vw, 130px); filter: drop-shadow(0 8px 25px rgba(0,0,0,0.2)); }
.h1-header { 
    font-size: clamp(2.5rem, 7vw, 4.5rem) !important; 
    font-weight: 800 !important; 
    margin: 1rem 0 0.5rem 0 !important; 
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle-header { font-size: clamp(1.1rem, 3vw, 1.6rem) !important; opacity: 0.95 !important; }

/* Sidebar */
.sidebar-custom {
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(20px);
    padding: 2.5rem 2rem;
    border-radius: 24px;
    margin: 2rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.4);
}

.sidebar-title {
    color: #1e293b !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin-bottom: 2rem !important;
    text-align: center;
}

/* Pose Gallery */
.pose-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.pose-thumb {
    aspect-ratio: 1;
    border-radius: 20px;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    border: 4px solid transparent;
    position: relative;
}

.pose-thumb:hover {
    transform: translateY(-12px) scale(1.05);
    box-shadow: 0 25px 50px rgba(102, 126, 234, 0.3);
    border-color: #667eea;
}

.pose-thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.pose-thumb:hover img { transform: scale(1.12); }

.pose-name {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    color: white;
    padding: 1rem;
    font-weight: 600;
    font-size: 0.9rem;
}

/* Main Content */
.main-content { padding: 3rem 2rem; max-width: 1400px; margin: 0 auto; }
.pose-viewer { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: start; margin-top: 2rem; }
.pose-title { 
    color: #1e293b !important; 
    font-size: clamp(2.2rem, 6vw, 3.5rem) !important; 
    font-weight: 800 !important; 
    margin-bottom: 2rem !important;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.pose-image-large {
    border-radius: 28px;
    box-shadow: 0 30px 60px rgba(0,0,0,0.15);
    max-height: 550px;
    width: 100%;
    object-fit: cover;
}

.ai-insights {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(25px);
    padding: 3.5rem;
    border-radius: 28px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.1);
    border-left: 8px solid #667eea;
    height: fit-content;
    max-height: 550px;
    overflow-y: auto;
}

.insights-title {
    color: #667eea !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin-bottom: 2rem !important;
}

/* Status Messages */
.image-status { text-align: center; padding: 3rem; color: #64748b; font-size: 1.2rem; }
.no-image { background: rgba(248, 250, 252, 0.8); border-radius: 20px; padding: 3rem; }

/* Responsive */
@media (max-width: 1024px) { .pose-viewer { grid-template-columns: 1fr !important; gap: 2.5rem !important; } }
@media (max-width: 768px) { 
    .sidebar-custom { margin: 1rem !important; padding: 2rem !important; } 
    .main-content { padding: 2rem 1rem !important; }
    .pose-gallery { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); }
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="app-header">
    <h1 class="h1-header">🧘 Conscious Flow</h1>
    <p class="subtitle-header">AI-Powered Yoga Pose Explorer</p>
</div>
""", unsafe_allow_html=True)

# Pose Data
poses = [
    "Downward Dog", "Scorpion Pose", "Headstand", "Child's Pose", 
    "Cobra Pose", "Bridge Pose", "Handstand", "leg Splits", "Mountain Pose"
]

image_map = {
    "Downward Dog": "images/Downward-Dog.jpeg",
    "Scorpion Pose": "images/Scorpion.jpg",
    "Headstand": "images/headstand.png",
    "Child's Pose": "images/Child-Pose.jpg",
    "Cobra Pose": "images/Cobra.jpg",
    "Bridge Pose": "images/bridge.jpeg",
    "Handstand": "images/handstand.jpg",
    "leg Splits": "images/split.jpg",
    "Mountain Pose": "images/mountain.jpg"
}

# Enhanced Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-custom">', unsafe_allow_html=True)
    st.markdown('<h2 class="sidebar-title">🌟 Select Pose</h2>', unsafe_allow_html=True)
    
    # Main selector
    selected_pose = st.selectbox(
        "Choose Asana:", 
        poses, 
        help="Pick any pose for instant AI insights",
        label_visibility="collapsed"
    )
    
    # Debug info (remove after confirming images work)
    st.markdown("---")
    st.markdown("**📁 File Check**")
    images_folder_exists = os.path.exists("images")
    st.markdown(f"**Images folder**: {'✅' if images_folder_exists else '❌'}")
    
    if images_folder_exists:
        working_count = sum(1 for path in image_map.values() if os.path.exists(path))
        st.markdown(f"**Working images**: {working_count}/{len(image_map)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content
if selected_pose:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Pose Title
    st.markdown(f'<h2 class="pose-title">📿 {selected_pose}</h2>', unsafe_allow_html=True)
    
    # Two-column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # BULLETPROOF IMAGE HANDLING
        image_path = image_map.get(selected_pose)
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                st.image(
                    img, 
                    caption=f"🧘 {selected_pose}", 
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Image error: {str(e)}")
                st.info(f"Path: {image_path}")
    
    with col2:
        st.markdown('<div class="ai-insights">', unsafe_allow_html=True)
        st.markdown('<h3 class="insights-title">🤖 AI Pose Insights</h3>', unsafe_allow_html=True)
        
        with st.spinner(f"🔮 Analyzing {selected_pose}..."):
            pose_info = get_pose_info(selected_pose)
        
        st.markdown(pose_info, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    text-align: center; 
    padding: 4rem 2rem; 
    color: #64748b; 
    font-size: 0.95rem;
    background: rgba(255,255,255,0.8);
">
    🧘 Conscious Flow - Powered by Ollama phi3:mini & Streamlit
</div>
""", unsafe_allow_html=True)
