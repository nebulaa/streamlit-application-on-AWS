import streamlit as st
import components.authenticate as authenticate
from PIL import Image
import json
import requests

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_icon=favicon,
    initial_sidebar_state="expanded"
)

authenticate.set_st_state_vars()

if (st.session_state["authenticated"]) == True:
    st.title(":speech_balloon: Contact Us", anchor=False)
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:
        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        if 'form_submitted' not in st.session_state:
            st.session_state['form_submitted'] = False
        
        if st.session_state['form_submitted']:
            st.success("Thank you for contacting us. We will get back to you soon.")

        if not st.session_state['form_submitted']:
            with st.form(key='contact_form'):
                st.write(":writing_hand: Please fill out the form below to contact us.")
                name = st.text_input("Login ID", username, key="username", disabled=True)
                email = st.text_input("Email", email, key="email", disabled=True)
                subject = st.text_input("Subject", max_chars=100, placeholder= "Enter a subject for your message.", key="subject")
                message = st.text_area("Message", max_chars=1000, placeholder= "Enter your questions or feedback about here.", key="message")
                submitted = st.form_submit_button("Submit Message 🛸")

                if submitted:
                    has_errors = False

                    if not subject:
                        st.error("Subject field is empty. Please enter a subject.")
                        has_errors = True

                    if not message:
                        st.error("Message field is empty. Please enter a message.")
                        has_errors = True

                    message = subject + "\n\n" + message

                    sns_api = "https://ztg8l9wj58.execute-api.us-east-1.amazonaws.com/user_email_contact_form"

                    sns_payload = {
                        "uuid": uuid,
                        "name": name,
                        "email": email,
                        "message": message
                    }

                    headers = {
                        'Content-Type': 'application/json',
                        'Authorization': access_token
                    }

                    if not has_errors:
                        try:
                            sns_response = requests.post(sns_api, data=json.dumps(sns_payload), headers=headers)
                            sns_response.raise_for_status()
                            sns_result = sns_response.json()

                            if 'MessageId' in sns_result:
                                st.success("Thank you for contacting us. We will get back to you soon.")
                                st.session_state['form_submitted'] = True
                            else:
                                st.error("An error occurred while sending your message. Please try again later.")

                        except Exception as err:
                            st.error("An error occurred while sending your message. Please try again later.")

        authenticate.button_logout()

else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()
