# pyrefly: ignore [missing-import]
import streamlit as st 

# configure page settings
st.set_page_config(page_title="My Portfolio", page_icon="")

# Center content on page using columns
col1, col2, col3  = st.columns([1,2,1])

with col2:
    st.title("Welcome Back") 
    st.write("Please log in to your accout to view the portfolio")

    # Create the form

    with st.form("Login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")

        # everyform must have a submit button
        submitted = st.form_submit_button("Login")

        if submitted:
            # Basic validation logic
            if email and password:
                st.success(f"Authentication successful! Welcome, {email}.")
                st.balloons()
            else:
                st.error("Please provide both email and password.")