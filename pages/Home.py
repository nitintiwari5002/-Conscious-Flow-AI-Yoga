import streamlit as st
from PIL import Image
import os

# Page config first
st.set_page_config(
    page_title="🧘 Conscious Flow: AI Yoga",
    page_icon="🧘",
    layout="wide"
)

# Modern CSS (same as before)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.main { font-family: 'Inter', sans-serif !important; background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%); background-size: 300% 300%; animation: gradientShift 12s ease infinite; }
@keyframes gradientShift { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
/* [Keep all previous CSS exactly the same - just the hero section changes below] */
.hero-section { min-height: 90vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem; position: relative; overflow: hidden; }
.hero-section::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at 20% 80%, rgba(120,119,198,0.3) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(255,119,198,0.3) 0%, transparent 50%); animation: float 20s infinite linear; pointer-events: none; }
@keyframes float { 0%,100%{transform:translateY(0px)rotate(0deg)} 33%{transform:translateY(-20px)rotate(120deg)} 66%{transform:translateY(10px)rotate(240deg)} }
.logo-hero { width: clamp(80px,15vw,140px); margin-bottom: 2rem; filter: drop-shadow(0 10px 30px rgba(255,255,255,0.3)); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.05)} }
.main-title { font-size: clamp(2.5rem,8vw,5.5rem) !important; font-weight: 800 !important; background: linear-gradient(135deg,#ffffff 0%,#e0e7ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 1rem 0 !important; line-height: 1.1; text-shadow: 0 0 40px rgba(255,255,255,0.5); }
.subtitle { font-size: clamp(1.2rem,4vw,2.2rem) !important; color: rgba(255,255,255,0.95) !important; font-weight: 400 !important; margin: 0 0 2.5rem 0 !important; max-width: 700px; }
.hero-text { color: rgba(255,255,255,0.9); font-size: clamp(1rem,2.5vw,1.3rem); line-height: 1.8; max-width: 650px; margin: 0 auto 3rem auto; }
.cta-button { background: linear-gradient(135deg,#ec4899 0%,#f59e0b 50%,#10b981 100%) !important; color: white !important; padding: 1.2rem 3rem !important; font-size: 1.25rem !important; font-weight: 600 !important; border: none !important; border-radius: 50px !important; box-shadow: 0 20px 40px rgba(236,72,153,0.4) !important; transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important; text-decoration: none !important; display: inline-block !important; }
.cta-button:hover { transform: translateY(-4px) !important; box-shadow: 0 25px 50px rgba(236,72,153,0.6) !important; }
</style>
""", unsafe_allow_html=True)

# ✅ FIXED LOGO - Using PIL (bulletproof)
logo_path = "images/image.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, use_container_width=False, width=120)
else:
    st.error("❌ Logo not found! Put 'images/image.png' in your app folder.")

# Hero content
st.markdown("""
<div class="hero-section">
    <h1 class="main-title">Conscious Flow</h1>
    <h2 class="subtitle">Yoga Powered by AI</h2>
    <p class="hero-text">Transform your practice with intelligent pose analysis and real-time feedback.</p>
    <a href="/info" class="cta-button">🌟 Explore Poses</a>
</div>
""", unsafe_allow_html=True)
