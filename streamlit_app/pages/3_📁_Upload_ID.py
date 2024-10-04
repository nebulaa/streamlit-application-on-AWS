import streamlit as st
import components.authenticate as authenticate
from PIL import Image
import json
import requests
import base64
import datetime

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_icon=favicon,
    initial_sidebar_state="expanded",
    layout="wide"
)

authenticate.set_st_state_vars()

if st.session_state["authenticated"]:
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)
    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:
        st.title("ID Check 📝", anchor=False)
        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        get_item_api = "https://il09wp8sn8.execute-api.us-east-1.amazonaws.com/user_get_uuid_s3_key"

        get_item_payload = {
            "uuid": uuid,
            "email": email
        }

        get_item_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        try:
            get_item_response = requests.post(get_item_api, data=json.dumps(get_item_payload), headers=get_item_headers)
            get_item_response.raise_for_status()
            get_item_result = get_item_response.json()
            db_uuid = get_item_result['db_uuid']
            s3_key = get_item_result['db_s3_key']
            
        except Exception as err:
            st.error(f'An error occurred: {err}')
            db_uuid = None

        if db_uuid is None or db_uuid != uuid:
            st.write(":red[Please complete the membership form before accessing this page.]")
            if st.button("✅ Membership Form"):
                st.switch_page("pages/2_✅_Membership_Form.py")
        
        elif s3_key is not None:
            st.subheader("IDs uploaded successfully. 👍", anchor=False)
            st.subheader("Please visit `⚙️ Account Info` to track your account verification status.", anchor=False)
            if st.button("⚙️ Account Info"):
                st.switch_page("pages/4_⚙️_Account_Info.py")
        
        elif s3_key is None and db_uuid == uuid:
            st.write("Upload a document that contains your :green[name], :green[date of birth] and your :green[current location].")
            st.write("We recommend providing the :green[Indian Voter ID] or :green[Aadhaar card] for the fastest verification process.")
            # st.write("To confirm your current location, you can upload a recent :green[utility bill] or a :green[transport card] that contains your name and current address.")
            st.write(":blue[Accepted file formats: jpg, jpeg or png. File size limit: 5MB.]")
            
            id_form = st.form(key='id_upload_form')

            photo_1 = id_form.file_uploader("Choose a valid ID that shows your name and date of birth, for example, an Indian voter ID.", type=['jpg', 'jpeg', 'png'], key='photo_1')
            photo_2 = id_form.file_uploader("Please upload a proof of (current) address.", type=['jpg', 'jpeg', 'png'], key='photo_2')
            photo_3 = id_form.camera_input("Take a photo with your face clearly visible.")

            image_consent = id_form.checkbox(":red[*] I consent to the use of the uploaded images for the purpose of verifying my account information.")
            submitted = id_form.form_submit_button("Upload ID(s) 📤")

            if submitted:

                has_errors = False

                if image_consent is None or image_consent is False:
                    has_errors = True
                    st.error("Please consent to the use of the uploaded images for the purpose of verifying your account.")
            
                if photo_1 is None:
                    st.error("Please upload your ID.")
                    has_errors = True

                if photo_2 is None:
                    st.error("Please upload your address proof.")
                    has_errors = True
                
                if photo_3 is None:
                    st.error("Please take a picture.")
                    has_errors = True

                if photo_1 is not None:               
                    encoded_image_1 = base64.b64encode(photo_1.read()).decode('utf-8')
                
                if photo_2 is not None:
                    encoded_image_2 = base64.b64encode(photo_2.read()).decode('utf-8')
                
                if photo_3 is not None:
                    encoded_image_3 = base64.b64encode(photo_3.read()).decode('utf-8')
                
                image_upload_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if has_errors is False:

                    photo_api_url = "https://rjz341e0mj.execute-api.us-east-1.amazonaws.com/user_id_photo_uploader"
                    photo_payload = {
                        "UUID": uuid,
                        "image_1": encoded_image_1,
                        "image_2": encoded_image_2,
                        "image_3": encoded_image_3,
                        "email": email,
                        "image_upload_timestamp": image_upload_timestamp,
                        "image_consent": image_consent
                    }
                    photo_headers = {
                        'Content-Type': 'application/json',
                        'Authorization': access_token
                    }
                    
                    try:
                        photo_response = requests.post(photo_api_url, data=json.dumps(photo_payload), headers=photo_headers)
                        photo_response.raise_for_status()
                        photo_upload_result = photo_response.json()
                        st.subheader("IDs uploaded successfully. 👍", anchor=False)
                        st.subheader("Please check `⚙️ Account Info` to track your account verification status.", anchor=False)
                        if st.button("⚙️ Account Info"):
                            st.switch_page("pages/4_⚙️_Account_Info.py")

                    except Exception as err:
                        st.error(f'An error occurred: {err}')
        else:
            st.write("Something went wrong. Please try again. If the problem persists, please contact the administrator.")

    authenticate.button_logout()

else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()
