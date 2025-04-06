import streamlit as st
import pyrebase
from google.cloud import firestore

ig_signup_version = "1.0.4"
signup_form_submitted = False

st.set_page_config(
    page_title=f"IntergalacticPro Signup (v{ig_signup_version})",
    page_icon=":rocket:",
    layout="centered",
    menu_items={
        'Get help': 'mailto:support@neuralbytes.net?subject=Need%20Help%20with%20IntergalacticPro',
        'Report a bug': 'mailto:bugs@neuralbytes.net?subject=IntergalacticPro%20Bug%20Report',
        'About': '''### The signup page for IntergalacticPro: A space and rockets expert who is highly knowledgeable, clear, concise, and friendly. \n
        https://intergalacticpro.neuralbytes.net'''
    }
)

st.title("IntergalacticPro Signup Page")
st.write("[Help improve IntergalacticPro](mailto:feedback@neuralbytes.net?subject=IntergalacticPro%20Feedback)")

firebaseConfig = {
    'apiKey': st.secrets.firebaseConfig['apiKey'],
    'authDomain': st.secrets.firebaseConfig['authDomain'],
    'databaseURL': st.secrets.firebaseConfig['databaseURL'],
    'projectId': st.secrets.firebaseConfig['projectId'],
    'storageBucket': st.secrets.firebaseConfig['storageBucket'],
    'messagingSenderId': st.secrets.firebaseConfig['messagingSenderId'],
    'appId': st.secrets.firebaseConfig['appId'],
    'measurementId': st.secrets.firebaseConfig['measurementId']
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firestore.Client.from_service_account_json(".streamlit/intergalacticpro-firebase-key.json")

def sign_up():
    """Returns `True` if the user had a correct password."""

    def signup_form():
        st.header("Signup Form")
        with st.form("Credentials"):
            st.session_state["first_name"] = st.text_input("First Name")
            st.session_state["last_name"] = st.text_input("Last Name")
            st.session_state["email"] = st.text_input("Email")
            st.session_state["password"] = st.text_input("Password", type="password")
            st.form_submit_button("Sign up", on_click=password_entered)
            st.caption("⬆️ Press it twice (not rapidly, though)")

    def password_entered():
        form_submitted = True
        try:
            signup = auth.create_user_with_email_and_password(st.session_state["email"], st.session_state["password"])
            auth.send_email_verification(signup['idToken'])
            print(signup)
            st.session_state["password_correct"] = True
            doc_ref = db.collection("users").document(st.session_state["email"])
            doc = doc_ref.get()
            doc_ref.set({
                "FirstName": st.session_state["first_name"],
                "LastName": st.session_state["last_name"],
            })
            del st.session_state["first_name"]
            del st.session_state["last_name"]
            st.session_state["user_name"] = doc.to_dict()["FirstName"] + " " + doc.to_dict()["LastName"]
        except Exception as e:
            return
    # Show inputs for username + password.
    signup_form()
    if not signup_form_submitted:
        return False

if not sign_up():
    st.stop()
