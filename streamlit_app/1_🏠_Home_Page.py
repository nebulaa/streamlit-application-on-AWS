import streamlit as st
from PIL import Image
import components.authenticate as authenticate

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_title=" App",
    page_icon=favicon,
    initial_sidebar_state="expanded")

authenticate.set_st_state_vars()
if st.session_state["authenticated"] == True:
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:
        username = cognito_user_info['name']

        st.subheader(f"Hello `{username}` 👋, Welcome 🎉", anchor=False)

        st.divider()

        st.audio ("bh.wav")

        st.image('img.jpg', use_column_width=True)

        st.header("Ready to become a member? :fire:", anchor=False)

        st.subheader("Complete the following steps to get your account verified:", anchor=False)
 
        if st.button("✅ Membership Form"):
            st.switch_page("pages/2_✅_Membership_Form.py")

        if st.button("📁 Upload ID"):
            st.switch_page("pages/3_📁_Upload_ID.py")

        st.subheader("Check your membership status:", anchor=False)

        if st.button("⚙️ Account Info"):
            st.switch_page("pages/4_⚙️_Account_Info.py")
        
        st.subheader("Let's create a third place together! 🔥")

        authenticate.button_logout()
else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()