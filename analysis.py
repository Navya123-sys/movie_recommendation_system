import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Comparative Analysis", layout="centered")

# ====== CUSTOM STYLE ======
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">📊 Comparative Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Accuracy Comparison of Recommendation Methods</div>', unsafe_allow_html=True)

# ================= DATA =================
methods = ["Content-Based", "Collaborative", "NLP Model"]
accuracy = [65, 75, 85]

# ================= GRAPH =================
fig, ax = plt.subplots()

bars = ax.bar(methods, accuracy)

ax.set_ylabel("Accuracy (%)")
ax.set_ylim(0, 100)

# Add values on bars
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 1, f"{yval}%", 
            ha='center', fontsize=10)

st.pyplot(fig)