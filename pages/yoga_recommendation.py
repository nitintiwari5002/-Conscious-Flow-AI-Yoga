import streamlit as st
from utils.ollama_client import pose_predictor  # Your existing function
from duckduckgo_search import DDGS

@st.cache_data(show_spinner=False, ttl=60*60)
def fetch_gif_ddg(name: str):
    """Fetch yoga pose GIF using DuckDuckGo."""
    query = f"{name} yoga pose gif animation"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=3))
            for r in results:
                url = r.get("image")
                if url and url.startswith("https") and (".gif" in url.lower() or "gif" in r.get("title", "").lower()):
                    return url
    except:
        pass
    return None

st.title("🧘 Conscious Flow AI Yoga Predictor")
st.markdown("Describe your issues (e.g., back pain, stress, neck stiffness) for personalized pose recommendations.")

problem = st.text_input("Enter your problems...", placeholder="e.g., lower back pain and anxiety")

if problem:
    with st.spinner("AI is recommending poses..."):
        # Call your pose_predictor - enhance it with this prompt if needed
        response = pose_predictor(f"""
        User problems: {problem}
        Recommend 2-3 beginner-friendly yoga poses. For each:
        - English & Sanskrit name
        - Key benefits for these issues
        - Step-by-step instructions (3-5 steps)
        - Duration: 30-60 seconds
        Format as bullet list: **Pose Name**: \n
        Benefits. \n
        Steps: 1....
        """)
    
    st.markdown("### Recommended Poses")
    st.markdown(response)  # Ollama output renders as Markdown
    
    # Parse common poses from response (simple keyword extract; improve with regex if needed)
    poses = ["Child's Pose", "Cat-Cow Pose", "Downward Dog", "Cobra Pose", "Tree Pose", "Legs Up the Wall"]
    for pose in poses:
        if pose.lower() in response.lower():
            gif_url = fetch_gif_ddg(pose)
            if gif_url:
                st.markdown(f"**{pose} Demo:**")
                st.image(gif_url, use_container_width=True)
                break  # Show first matching GIF
