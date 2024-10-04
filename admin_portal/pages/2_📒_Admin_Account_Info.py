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

if st.session_state["authenticated"]:
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
        
    else:
        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        get_code_api = "https://46xpdayzpe.execute-api.us-east-1.amazonaws.com/admin_create_view_invite_code"

        get_code_payload = {
            "uuid": uuid
        }

        get_code_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        try:
            get_code_response = requests.post(get_code_api, data=json.dumps(get_code_payload), headers=get_code_headers)
            response_uuid = get_code_response.json()['response_uuid']
            response_code = get_code_response.json()['response_code']
            response_name = get_code_response.json()['response_name']
        except Exception as err:
            st.error(f'An error occurred: {err}')
        
        if response_uuid == "No UUID found":
            st.subheader("⛔ Create a referral code below.", anchor=False)

        st.header(f"Admin Account Info 📣", anchor=False)
        
        st.subheader(f"⛵ Your Referral Code: `{response_code}`", anchor=False)

        st.write("Share this code with your friends and help them register. 🎉")
        st.write("You can update this code in the `🪐 Update Referral Code` section below.")

        st.divider()

        st.header("🪐 Update Referral code:", anchor=False)
        st.write("*Removes the old referral code and adds the new one.* 🔐")
        with st.form(key='update_referral_code', clear_on_submit = True):
            code = st.text_input("Enter the new referral code below:", max_chars=15)
            update_referral_code = st.form_submit_button("Update Referral Code 🍄")
        
            if update_referral_code:
                create_referral_code_api = "https://g3wdc082k0.execute-api.us-east-1.amazonaws.com/admin_update_invite_code"

                create_referral_code_payload = {
                "uuid": uuid,
                "name": username,
                "code": code
                }

                create_referral_code_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }

                try:
                    create_referral_code_response = requests.post(create_referral_code_api, data=json.dumps(create_referral_code_payload), headers=create_referral_code_headers)
                    create_referral_code_response.raise_for_status()
                    create_referral_code_result = create_referral_code_response.json()
                    if create_referral_code_result['message'] == "Duplicate code found.":
                        st.error("Duplicate code found. Please enter another code. ⛔")
                    elif create_referral_code_result['message'] == "Code updated.":
                        st.success(f"✅ Referral code updated to `{code}` ")
                        st.write("Please click on `📒 Admin Account Info` on the left sidebar to see the updated invite code. ⚠️")
                    else:
                        st.error("Something went wrong. Please try again. ⛔")
                except Exception as err:
                    st.error(f'An error occurred: {err}')

        authenticate.button_logout()
    
else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()