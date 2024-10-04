import streamlit as st
import components.authenticate as authenticate
from PIL import Image
import json
import requests

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_icon=favicon,
    initial_sidebar_state="expanded")

authenticate.set_st_state_vars()

if st.session_state["authenticated"] == True:
    st.title("Account Info :lock:", anchor=False)
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:

        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        get_acc_api = "https://ps9j9p7qh1.execute-api.us-east-1.amazonaws.com/user_get_information"

        get_acc_payload = {
        "uuid": uuid,
        "email": email
        }

        get_acc_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        try:
            get_acc_response = requests.post(get_acc_api, data=json.dumps(get_acc_payload), headers=get_acc_headers)
            get_acc_response.raise_for_status()
            get_acc_result = get_acc_response.json()
            message = get_acc_result.get('message')

            if message is not None:
                if 'Image_1' in message and 'S' in message['Image_1']:
                    image_1_uploaded = "Yes"
                else:
                    image_1_uploaded = "No"
            else:
                image_1_uploaded = "No"

        except requests.exceptions.HTTPError as http_err:
            st.error(f'HTTP error occurred: {http_err}')
            message = None
        except Exception as err:
            st.error(f'An error occurred: {err}')
            message = None

        if message is not None:
            
            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(":id: Personal Details :open_file_folder:", anchor=False)
                st.write(f"**Login ID:** `{username}`")
                st.write(f"**First Name:** `{message['first_name']['S']}`")
                st.write(f"**Last Name:** `{message['last_name']['S']}`")
                st.write(f"**Email:** :email: `{message['email']['S']}`")
                st.write(f"**Phone or Dial Code:** :telephone_receiver: `{message['phone_country_code']['S']}`")
                st.write(f"**Phone Number:** :telephone: `{message['phone_number']['S']}`")
                st.write(f"**Date of Birth:** :birthday: `{message['date_of_birth']['S']}`")
                st.write(f"**Age:** :date: `{message['age']['N']}`")

            with col2:

                st.subheader(":earth_americas: Location Details :house_with_garden:", anchor=False)
                st.write(f"**Country:** :earth_africa: `{message['country']['S']}`")
                st.write(f"**State:** :house: `{message['state_province']['S']}`")
                st.write(f"**City:** :cityscape: `{message['city']['S']}`")
                st.subheader(":information_source: Other Information :mega:", anchor=False)
                st.write(f"**Discord ID:** :microphone: ` {message['discord_id']['S']}`")
                st.write(f"**Prefer to lead and organize meetups in your neighborhood:** :handshake: `{message['leadership_preference']['S']}`")
                st.write(f"**Photo ID Uploaded:** 📤 `{image_1_uploaded}`")

            st.divider()

            if 'verification_status' in message:
                Verified = message['verification_status']['BOOL']
                if Verified == True:
                    st.subheader(f"🍀 Account Status: :green[Verified]", anchor=False)
                elif Verified == False and image_1_uploaded == "No":
                    st.subheader(f":x: Account Status: :red[Not Verified]", anchor=False)
                    st.write(f"📝 Please visit the `📁 Upload ID` page to complete the verification process.")
                    if st.button("📁 Upload ID"):
                        st.switch_page("pages/3_📁_Upload_ID.py")
                else:
                    st.subheader(f":x: Account Status: :red[Not Verified]", anchor=False)
                    st.write(f"📝 Please wait for an admin to review your account.")
                    st.write(f"Referring Admin: 📩 `{message['referring_admin']['S']}`")
            else:
                st.subheader(f":x: Account Status: :red[Not Verified]", anchor=False)
                st.write(f"📝 Please reach out to an admin.")
        else:
            st.write(":x: `No account information found.`")

            st.subheader("🔗Please visit the below pages to get started.", anchor=False)

            if st.button("✅ Membership Form"):
                st.switch_page("pages/2_✅_Membership_Form.py")

            if st.button("📁 Upload ID"):
                st.switch_page("pages/3_📁_Upload_ID.py")
        
        authenticate.button_logout()

else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()