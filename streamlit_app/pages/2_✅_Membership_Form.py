import streamlit as st
import components.authenticate as authenticate
from PIL import Image
import datetime
import requests
import json

favicon = Image.open('favicon.ico')

st.set_page_config(
    page_icon=favicon,
    initial_sidebar_state="expanded"
)

authenticate.set_st_state_vars()

if st.session_state["authenticated"] == True:
    st.title("✅ Get Verified", anchor=False)
    access_token = st.session_state["access_token"]
    cognito_user_info = authenticate.get_user_info(access_token)

    if 'error' in cognito_user_info:
        st.error("Invalid Login. Please try again. Contact the administrator if unsuccessful.")
        authenticate.button_login()
    else:
        uuid = cognito_user_info['sub']
        email = cognito_user_info['email']
        username = cognito_user_info['name']

        initial_get_item_api = "https://il09wp8sn8.execute-api.us-east-1.amazonaws.com/user_get_uuid_s3_key"

        initial_get_item_payload = {
        "uuid": uuid,
        "email": email
        }

        initial_get_item_headers = {
            'Content-Type': 'application/json',
            'Authorization': access_token
        }
        try:
            initial_get_item_response = requests.post(initial_get_item_api, data=json.dumps(initial_get_item_payload), headers=initial_get_item_headers)
            initial_get_item_response.raise_for_status()
            initial_get_item_result = initial_get_item_response.json()
            initial_db_uuid = initial_get_item_result['db_uuid']
            initial_db_uuid = str(initial_db_uuid)
            
        except Exception as err:
            st.error(f'An error occurred: {err}')
            initial_db_uuid = None
        
        if initial_db_uuid is not None and initial_db_uuid == uuid:
            st.subheader("Membership form submitted successfully. 🎉", anchor=False)
            st.subheader("Please check `📁 Upload ID` or `⚙️ Account Info` next.", anchor=False)
            
            if st.button("📁 Upload ID"):
                st.switch_page("pages/3_📁_Upload_ID.py")

            if st.button("⚙️ Account Info"):
                st.switch_page("pages/4_⚙️_Account_Info.py")
        
        else:

            if 'count' not in st.session_state:
                st.session_state.count = 0

            def increment_counter():
                st.session_state.count += 1
            st.write("**Please enter the invite code provided by the referring 's  Admin.**")
            if st.session_state.count <= 5:
                ref_code = st.text_input("Enter the referral code", on_change=increment_counter, key="ref_code", help="You have 5 retries to enter the correct referral code.")
            else:
                st.error("You have exceeded the maximum number of retries. Try again later.")
                ref_code = None
                disable_user_api = "https://u4zy4448m4.execute-api.us-east-1.amazonaws.com/user_disable_invite_code_dos"

                disable_user_payload = {
                "uuid": uuid
                }

                disable_user_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }

                try:
                    disable_user_response = requests.post(disable_user_api, data=json.dumps(disable_user_payload), headers=disable_user_headers)
                    disable_user_response.raise_for_status()
                    st.success("Your account has been disabled. Please contact the administrator.")
                    
                except Exception as disable_user_err:
                    st.error(f'An error occurred: {disable_user_err}')

            if ref_code:
                check_code_api = "https://kedtu5hqm2.execute-api.us-east-1.amazonaws.com/user_check_invite_code"

                check_code_payload = {
                    "code": ref_code
                }

                check_code_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': access_token
                }
                
                try:
                    check_code_response = requests.post(check_code_api, data=json.dumps(check_code_payload), headers=check_code_headers)
                    check_code_response.raise_for_status()
                    check_code_result = check_code_response.json()
                    returned_code = check_code_result['returned_code']
                    referring_admin = check_code_result['referring_admin']
                    referring_admin_uuid = check_code_result['referring_admin_uuid']

                except requests.exceptions.HTTPError as http_err:
                    st.error(f'HTTP error occurred: {http_err}')
                    returned_code = None
                    referring_admin = None
                    referring_admin_uuid = None

                except Exception as err:
                    st.error(f'An error occurred: {err}')
                    returned_code = None
                    referring_admin = None
                    referring_admin_uuid = None

                if returned_code == ref_code:
                    st.success("Referral code is valid.")

                    st.divider()

                    st.subheader("📝's  - Membership Form:", anchor=False)

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
                        db_uuid = str(db_uuid)
                        
                    except Exception as err:
                        print(f'An error occurred: {err}')
                        st.error(f'An error occurred: {err}')
                        db_uuid = None

                    if db_uuid is None or db_uuid != uuid:
                        form = st.form("_form")

                        first_name = form.text_input("First Name", "", max_chars=50)
                        last_name = form.text_input("Last Name", "", max_chars=50)
                        min_date = datetime.date(1920, 1, 1)
                        max_date = datetime.date.today() - datetime.timedelta(days=6570)
                        default_date = datetime.date(1995, 1, 1)
                        date_of_birth = form.date_input("Date of Birth", help="Enter your date of birth.", min_value=min_date, max_value=max_date, value=default_date, format="DD-MM-YYYY")
                        age = form.number_input("Age", min_value=18, max_value=120, step=1, help="Must be 18 or older to join 's .")
                        date_of_birth_str = date_of_birth.strftime("%Y-%m-%d")
                        
                        with open('CountryCodes.json', 'r', encoding='utf-8') as file:
                            phone_codes = json.load(file)
                            file.close()
                            
                        country_codes = [code['dial_code'] for code in phone_codes]

                        phone_country_code = form.selectbox("Phone or Dial Code", options=country_codes, index=None, help="Select your Dial or Phone code.")
                        
                        phone_number = form.text_input("Phone Number", help="Enter your phone number without any symbols, spaces or dashes.")

                        with open('countries.json', encoding='utf-8') as file:
                            country_data = json.load(file)
                            file.close()

                        country_names = [country['name'] for country in country_data]

                        select_country = form.selectbox("Enter country:", options=country_names, index=None)

                        with open('states.json', 'r', encoding='utf-8') as file:
                            state_data = json.load(file)
                            file.close()

                        all_states = [state["name"] for state in state_data]

                        select_state = form.selectbox("Enter state or province:", options=all_states, index=None)
                        
                        if select_state:
                            with open('states+cities.json', 'r', encoding='utf-8') as file:
                                data = json.load(file)

                            target_state_data = [item for item in data if item['name'] == select_state]
                            city_list = [city['name'] for state in target_state_data for city in state.get('cities', [])]
                            if not city_list:
                                city_list.append(select_state)

                            select_city = form.selectbox("Enter city:", options=city_list, index=None)

                        discord_id = form.text_input("Discord ID (Optional)", "", help="Enter the Discord username instead of the dispaly name.", max_chars=50)
                        preference = form.radio("Would you prefer to lead and organize meetups in your neighborhood?", ["Yes", "No", "Maybe"])
                        consent = form.checkbox("I consent to the collection and processing of my personal data for the purpose of joining 's . I understand that this information will be used in accordance with the `🔒 Privacy Policy`. I acknowledge that I have the right to withdraw this consent at any time by using the `📞 Contact Form`.", value=False, help="Please check this box to consent to the processing of your personal data for the purpose of joining 's .")
                        
                        with st.expander("**Privacy Policy** 🔒", expanded=False):
                            policy = """

                            Effective Date: 01/01/2024

                            This Privacy Policy outlines how we handle your personal information in accordance with the General Data Protection Regulation (GDPR).

                            1. Information Collection:

                            We collect and process your name, email and other necessary details for membership verification.

                            2. Use of Information:

                            Your data is used for membership verification, granting exclusive podcast access, and, with your consent, sending newsletters or marketing communications.

                            """
                            st.markdown(policy)

                        if form.form_submit_button("Submit"):
                            time_of_submission = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            api_url = "https://bfsjebgg61.execute-api.us-east-1.amazonaws.com/user_verification_form_submission"

                            has_errors = False

                            if not first_name:
                                st.error("First name cannot be empty.")
                                has_errors = True
                            if not last_name:
                                st.error("Last name cannot be empty.")
                                has_errors = True
                            if not date_of_birth_str:
                                st.error("Date of birth cannot be empty.")
                                has_errors = True
                            if not age:
                                st.error("Age cannot be empty.")
                                has_errors = True
                            if not phone_country_code:
                                st.error("Phone or Dial code cannot be empty.")
                                has_errors = True
                            if not phone_number:
                                st.error("Phone number cannot be empty.")
                                has_errors = True
                            elif not (phone_number.isdigit() and 6 <= len(phone_number) <= 15):
                                st.error("Phone number must be a 6 to 15 digit number such as 12345678 without any '+' symbol, spaces or dashes.")
                                has_errors = True
                            if not select_country:
                                st.error("Country cannot be empty.")
                                has_errors = True
                            if not select_state:
                                st.error("Choose State or Province.")
                                has_errors = True
                            try:
                                if not select_city:
                                    st.error("Choose City.")
                                    has_errors = True
                            except Exception as err:
                                st.error("Choose City.")
                                has_errors = True
                            if not preference:
                                st.error("Preference cannot be empty.")
                                has_errors = True
                            if not consent:
                                st.error("Please consent to the processing of your personal data.")
                                has_errors = True

                            if not has_errors:
                                payload = {
                                "uuid": uuid,
                                "email": email,
                                "username": username,
                                "first_name": first_name,
                                "last_name": last_name,
                                "date_of_birth": date_of_birth_str,
                                "age": age,
                                "phone_country_code": phone_country_code,
                                "phone_number": phone_number,
                                "country": select_country,
                                "state_province": select_state,
                                "city": select_city,
                                "discord_id": discord_id,
                                "leadership_preference": preference,
                                "invite_code": returned_code,
                                "referring_admin": referring_admin,
                                "referring_admin_uuid": referring_admin_uuid,
                                "consent": consent,
                                "time_of_submission": time_of_submission
                                }

                                headers = {
                                    'Content-Type': 'application/json',
                                    'Authorization': access_token
                                }

                                try:
                                    with requests.post(api_url, data=json.dumps(payload), headers=headers) as response:
                                        if response.status_code == 200:
                                            st.success("Membership form submitted successfully. 🎉")
                                            st.subheader("Please check `📁 Upload ID` next.", anchor=False)

                                            if st.button("📁 Upload ID"):
                                                st.switch_page("pages/3_📁_Upload_ID.py")
                                        else:
                                            st.error("❌Error submitting membership form. Please try again later.")
                                except Exception as err:
                                    st.error('An error occurred: {}'.format(err))
                    else:
                        st.subheader("Membership form submitted successfully. 🎉", anchor=False)
                    
                if returned_code != ref_code:
                    st.error("Referral code is invalid. If you do not have a referral code, please write to us on discord.")
                    st.error("Invalid attempt count: " + str(st.session_state.count) + ". You have " + str(5 - st.session_state.count) + " attempts left.")


        authenticate.button_logout()
    
else:
    st.header("Please login to access this page.", anchor=False)
    authenticate.button_login()