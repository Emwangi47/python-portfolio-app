# pyrefly: ignore [missing-import]
import streamlit as st

# Configure the page
st.set_page_config(page_title="About Me", page_icon="👋")

# 1. HIDE STREAMLIT BRANDING (CSS Injection)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. HERO SECTION
col1, col2 = st.columns([1, 2.5], vertical_alignment="center") # Make the text column wider than the image column

with col1:
    # Profile Picture
    st.image("profile.jpeg", width=250)

with col2:
    st.title("Hi, I'm Emmanuel")
    st.subheader("Software Engineer | Python Developer | Cloud Architect")
    st.write("I am a junior software engineer based in Elk Grove Village, Illinois focused on practical application development. I have a strong foundation in Python & AWS and a commitment to building reliable, well-tested systems.")

# 3. INTERACTIVE TABS
# This groups your information neatly instead of stacking it vertically
tab1, tab2, tab3 = st.tabs(["🛠️ Technical Skills", "🎓 Certifications", "🚀 Current Focus"])

with tab1:
    st.write("### Core Competencies")
    st.write("- **Languages:** Python")
    st.write("- **Cloud Compute:** AWS Console & Architecture")
    st.write("- **Frameworks & Tools:** Streamlit, APIs, Git/GitHub")
    st.write("- **Concepts:** Data Structures & Algorithms, Quality Assurance, Data Virtualization, Machine Learning & Artificial Intelligence")

with tab2:
    st.write("### Professional Credentials")
    st.write("✔️ **AWS Solutions Architect – Associate**")
    st.write("✔️ **Certified Python Programmer**")
    st.write("✔️ **Python Data Structures and Algorithms**")
    st.write("✔️ **Introduction to Artificial Intelligence**")
    st.write("✔️ **Foundations of Machine Learning**")
    st.write("✔️ **Introduction to Quality Assurance (On going)**")
    st.write("✔️ **System Design and Architecture (On going)**")


with tab3:
    st.write("### Studies & Trajectory")
    st.write("- Currently expanding my expertise in **System Design and Architecture** and **Software Testing & Quality Assurance** while continuing to build on my Foundations of Machine Learning.")
    st.write("- Actively preparing to transition into a software engineering role or apprenticeship.")
    st.write("- Passionate about leveraging technology to solve real-world problems and eager to contribute to impactful projects.")
    st.write("- Continuing to build hands-on Python and AWS projects to strengthen my cloud computing and software development skills.")


st.divider()

# CONTACT SECTION
st.header("📫 Let's Connect!")
st.write("I am always open to discussing technology, apprenticeships, and software engineering opportunities.")

if st.button("Contact Me"):
    st.success("Please reach out at: manumwangi47@gmail.com, connect with me on [GitHub](https://github.com/Emwangi47) or [LinkedIn](https://www.linkedin.com/in/emanmwangi)!")