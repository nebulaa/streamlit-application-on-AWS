import streamlit as st
import components.authenticate as authenticate
from PIL import Image
import json
import requests
import pandas as pd
import io
import base64

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
        st.header(f"Verification 📖", anchor=False)
        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        get_user_info_api = "https://j4vaqo3y89.execute-api.us-east-1.amazonaws.com/admin_get_members"

        get_user_info_payload = {
        "uuid": uuid
        }

        get_user_info_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }

        try:
            get_user_info_response = requests.post(get_user_info_api, data=json.dumps(get_user_info_payload), headers=get_user_info_headers)
            get_user_info_response.raise_for_status()
            get_user_info_result = get_user_info_response.json()

            df = pd.DataFrame(get_user_info_result)

            if df.empty:
                st.error("There are no members to display. ⚠️")
                authenticate.button_logout()
                st.stop()
            
            if 'image_upload_timestamp' not in df.columns:
                
                columns_shown_no_image = st.multiselect("Select the columns: ", ['UUID', 'first_name', 'last_name', 'email', 'phone_country_code','phone_number', 'date_of_birth', 'country', 'state_province', 'city', 'age', 'invite_code', 'username', 'discord_id'], default=['UUID', 'first_name', 'last_name', 'email', 'age', 'country'])

                st.dataframe(df, column_order=columns_shown_no_image, hide_index=True)

                st.write("Members yet to upload IDs. Unable to verify. ⚠️")

                authenticate.button_logout()
                st.stop()


            df = df.drop(columns=['referring_admin_uuid', 'verification_status','leadership_preference', 'time_of_submission', 'image_upload_timestamp', 'consent', 'image_consent', 'referring_admin'])

            columns_shown = st.multiselect("Select the columns: ", ['UUID', 'first_name', 'last_name', 'email', 'phone_country_code','phone_number', 'date_of_birth', 'country', 'state_province', 'city', 'age', 'invite_code', 'Image_1', 'Image_2', 'Image_3', 'username', 'discord_id'], default=['UUID', 'first_name', 'last_name', 'email', 'age', 'country', 'Image_1', 'Image_2', 'Image_3'])

            st.dataframe(df, column_order=columns_shown, hide_index=True)

            df = df[df['Image_1'].notna()]

            uuid_list = df["UUID"].tolist()
            email_list = df["email"].tolist()

            all_Image1 = df["Image_1"].tolist()
            all_Image2 = df["Image_2"].tolist()
            all_Image3 = df["Image_3"].tolist()

        except Exception as err:
            st.error(f'An error occurred: {err}')

        st.divider()

        st.subheader("Get Member Info 📒", anchor=False)

        
        with st.form(key='get_member_info'):
            member_uuid = st.selectbox("Select the member's UUID: ", uuid_list)
            get_member_info = st.form_submit_button("Get Member Info 🔍")

        if get_member_info:
            selected_row = df[df["UUID"] == member_uuid]
            transposed_row = selected_row.transpose()
            new_order = ['UUID', 'first_name', 'last_name', 'email', 'phone_country_code','phone_number', 'date_of_birth', 'age', 'country', 'state_province', 'city', 'invite_code', 'Image_1', 'Image_2', 'Image_3', 'username', 'discord_id']
            transposed_row = transposed_row.reindex(new_order)
            transposed_row = transposed_row.astype(str)
            st.table(transposed_row)

        st.divider()

        st.subheader("Retrieve Photo ID :camera:", anchor=False)

        tab1, tab2, tab3 = st.tabs(["Image ID: 1", "Image ID: 2", "Image ID: 3"])
        with tab1:
            with st.form(key='retrieve_photo_id_1'):
                selected_Image1 = st.selectbox("Select the member's S3Key: ", all_Image1)
                retrieve_photo_id_1 = st.form_submit_button("Retrieve Photo ID 🔎")

            if retrieve_photo_id_1:
                retrieve_photo_id_1_api = "https://j4vaqo3y89.execute-api.us-east-1.amazonaws.com/admin_get_members"

                retrieve_photo_id_1_payload = {
                    "Image_1": selected_Image1
                }

                retrieve_photo_id_1_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }

                try:
                    retrieve_photo_id_1_response = requests.post(retrieve_photo_id_1_api, data=json.dumps(retrieve_photo_id_1_payload), headers=retrieve_photo_id_1_headers)
                    retrieve_photo_id_1_response.raise_for_status()
                    retrieve_photo_id_1_result = retrieve_photo_id_1_response.json()
                    decoded_message_1 = base64.b64decode(retrieve_photo_id_1_result['response'])
                    received_image_1 = Image.open(io.BytesIO(decoded_message_1))
                    st.image(received_image_1)
                    
                except Exception as err:
                    st.error(f'An error occurred: {err}')
            
        with tab2:
            with st.form(key='retrieve_photo_id_2'):
                selected_Image2 = st.selectbox("Select the member's S3Key: ", all_Image2)
                retrieve_photo_id_2 = st.form_submit_button("Retrieve Photo ID 🔎")

            if retrieve_photo_id_2:
                retrieve_photo_id_2_api = "https://j4vaqo3y89.execute-api.us-east-1.amazonaws.com/admin_get_members"

                retrieve_photo_id_2_payload = {
                    "Image_2": selected_Image2
                }

                retrieve_photo_id_2_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }

                try:
                    retrieve_photo_id_2_response = requests.post(retrieve_photo_id_2_api, data=json.dumps(retrieve_photo_id_2_payload), headers=retrieve_photo_id_2_headers)
                    retrieve_photo_id_2_response.raise_for_status()
                    retrieve_photo_id_2_result = retrieve_photo_id_2_response.json()
                    decoded_message_2 = base64.b64decode(retrieve_photo_id_2_result['response'])
                    received_image_2 = Image.open(io.BytesIO(decoded_message_2))
                    st.image(received_image_2)
                    
                except Exception as err:
                    st.error(f'An error occurred: {err}')

        with tab3:
            with st.form(key='retrieve_photo_id_3'):
                selected_Image3 = st.selectbox("Select the member's S3Key: ", all_Image3)
                retrieve_photo_id_3 = st.form_submit_button("Retrieve Photo ID 🔎")

            if retrieve_photo_id_3:
                retrieve_photo_id_3_api = "https://j4vaqo3y89.execute-api.us-east-1.amazonaws.com/admin_get_members"

                retrieve_photo_id_3_payload = {
                    "Image_3": selected_Image3
                }

                retrieve_photo_id_3_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }

                try:
                    retrieve_photo_id_3_response = requests.post(retrieve_photo_id_3_api, data=json.dumps(retrieve_photo_id_3_payload), headers=retrieve_photo_id_3_headers)
                    retrieve_photo_id_3_response.raise_for_status()
                    retrieve_photo_id_3_result = retrieve_photo_id_3_response.json()
                    decoded_message_3 = base64.b64decode(retrieve_photo_id_3_result['response'])
                    received_image_3 = Image.open(io.BytesIO(decoded_message_3))
                    st.image(received_image_3)
                    
                except Exception as err:
                    st.error(f'An error occurred: {err}')
                    
        st.divider()

        st.subheader(":id: Verify a member:", anchor=False)

        with st.form(key='verify_member'):
            member_uuid = st.selectbox("Select the member's UUID: ", uuid_list)
            member_email = st.selectbox("Select the member's email: ", email_list)
            verify_member = st.form_submit_button("Verify Member 🔆")

        if verify_member:
            
            verify_member_api = "https://j4vaqo3y89.execute-api.us-east-1.amazonaws.com/admin_get_members"

            verify_member_payload = {
                "member_uuid": member_uuid,
                "email": member_email
            }

            verify_member_headers = {
                'Content-Type': 'application/json',
                'Authorization': access_token
            }

            try:
                if df.loc[(df['UUID'] == member_uuid) & (df['email'] == member_email)].empty:
                    st.error("UUID and email are not of the same user. Refer to the table above and try again. ⚠️")
                else:
                    verify_member_response = requests.post(verify_member_api, data=json.dumps(verify_member_payload), headers=verify_member_headers)
                    verify_member_response.raise_for_status()
                    verify_member_result = verify_member_response.json()

                    if verify_member_result['response']['ResponseMetadata']['HTTPStatusCode'] == 200:
                        st.success("✨Member verified successfully.✨")
                    else:
                        st.error("Member verification failed. Please try again. ⚠️")
            except requests.exceptions.HTTPError as http_err:
                st.error(f'HTTP error occurred: {http_err}')
            except Exception as err:
                st.error(f'An error occurred: {err}')

        authenticate.button_logout()
                
else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()