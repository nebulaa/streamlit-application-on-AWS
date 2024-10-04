import streamlit as st
from PIL import Image
import components.authenticate as authenticate

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_title="ABC Admin App",
    page_icon=favicon,
    initial_sidebar_state="expanded"
)

authenticate.set_st_state_vars()
# Add login/logoubutton_logout_2
if st.session_state["authenticated"]:
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:
        username = cognito_user_info['name']

        st.header(f"Hello `{username}` 👋, Welcome to ABC  Admin Portal 🎉", anchor=False)

        st.image('giphy.gif')


        authenticate.button_logout()
else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()