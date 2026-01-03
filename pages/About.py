import streamlit as st

st.set_page_config(page_title="About - Conscious Flow", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
.main { font-family: 'Poppins', sans-serif !important; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
.about-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 5rem 2rem; text-align: center; position: relative; }
.about-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px; background: rgba(255,255,255,0.3); }
.logo-about { width: 100px; filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2)); }
.h1-about { font-size: clamp(2.5rem, 7vw, 4rem) !important; font-weight: 800 !important; margin: 1rem 0 !important; }
.content-section { max-width: 1200px; margin: 0 auto; padding: 4rem 2rem; }
.story-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4rem; align-items: center; margin: 4rem 0; }
.story-card { background: rgba(255,255,255,0.9); backdrop-filter: blur(20px); padding: 3rem; border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.3); line-height: 1.8; }
.photo-container { text-align: center; }
.dev-photo { width: 100%; max-width: 350px; border-radius: 24px; box-shadow: 0 25px 50px rgba(0,0,0,0.15); transition: transform 0.3s ease; }
.dev-photo:hover { transform: scale(1.02); }
.tech-stack { display: flex; flex-wrap: wrap; gap: 1rem; margin: 2rem 0; }
.tech-badge { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.75rem 1.5rem; border-radius: 50px; font-weight: 600; font-size: 0.95rem; box-shadow: 0 5px 15px rgba(102,126,234,0.4); transition: all 0.3s ease; }
.tech-badge:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.6); }
.timeline { position: relative; padding: 3rem 0; }
.timeline::before { content: ''; position: absolute; left: 50%; transform: translateX(-50%); width: 4px; height: 100%; background: linear-gradient(180deg, #667eea, #764ba2); border-radius: 2px; }
.timeline-item { display: flex; margin: 3rem 0; position: relative; }
.timeline-item:nth-child(odd) { justify-content: flex-end; padding-right: 3rem; }
.timeline-item:nth-child(even) { justify-content: flex-start; padding-left: 3rem; }
.timeline-content { background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 400px; backdrop-filter: blur(10px); }
@media (max-width: 768px) { .story-grid { grid-template-columns: 1fr !important; gap: 2rem !important; } .timeline::before { left: 20px !important; } .timeline-item:nth-child(odd) { justify-content: flex-start !important; padding-right: 0 !important; padding-left: 4rem !important; } }
</style>
""", unsafe_allow_html=True)

# Hero - FIXED: No deprecated parameters
col1, col2 = st.columns([1, 4])
with col1: 
    st.image("images/image.png", width=100)
with col2:
    st.markdown('<div class="about-hero"><h1 class="h1-about">The Story Behind Conscious Flow</h1><p style="font-size: 1.3rem; opacity: 0.95; max-width: 600px; margin: 0 auto;">Bridging ancient wisdom with cutting-edge AI</p></div>', unsafe_allow_html=True)

# Main Story
st.markdown('<div class="content-section">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
    <div class="story-card">
        <h2 style="color: #4a5568; font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;">🌊 What is Conscious Flow?</h2>
        <p style="color: #666; font-size: 1.1rem; line-height: 1.8;">An innovative platform that enhances yoga practice through artificial intelligence. Advanced AI delivers personalized insights, pose recommendations, and real-time feedback—making yoga accessible and effective for all levels.</p>
        <div class="tech-stack">
            <div class="tech-badge">Streamlit</div><div class="tech-badge">Ollama phi3:mini</div><div class="tech-badge">Python</div><div class="tech-badge">Computer Vision</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="photo-container">', unsafe_allow_html=True)
    # FIXED: Changed use_column_width=True to use_container_width=True
    st.image("images/me.jpg", caption="👨‍💻 Creator & Yoga Enthusiast", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="story-card" style="margin-top: 3rem; text-align: center;">
    <h2 style="color: #4a5568; font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;">🚀 Vision for the Future</h2>
    <p style="color: #666; font-size: 1.1rem; line-height: 1.8; max-width: 700px; margin: 0 auto;">
        Evolving with AI advancements to deliver hyper-personalized yoga experiences, adaptive flows, and integrated nutrition planning.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
