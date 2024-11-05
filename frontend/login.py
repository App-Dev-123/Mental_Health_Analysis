import streamlit as st
import base64
from app import app
from user import user

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_image(image_file):
    bin_str = get_base64_of_bin_file(image_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: contain;
        background-position: left;
        min-height: 100vh;
        background-repeat: no-repeat;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def login_form():
    set_bg_image('C:/Users/sahit/OneDrive/Desktop/Mental health awareness.jpg')

    col1, col2, col3 = st.columns([1, 0.75, 1.25])
    with col3:
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button('Login'):
            # Your login logic here
            if(username == 'Admin' and password == 'admin_6732'):
                st.session_state['authenticated'] = "upload_page"
                st.success("You are logged in")
                st.experimental_rerun()
            elif (username == 'User' and password == 'user_9012'):
                st.session_state['authenticated'] = "user_page"
                st.success("You are logged in")
                st.experimental_rerun()
            else:
                st.write("Incorrect password or username")
    return st.session_state['authenticated']

if __name__ == "__main__":
    # Initialize session state
    page = st.experimental_get_query_params().get("page", ["login"])[0]
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = "Login_page"
    if st.session_state.authenticated == "Login_page":
        login_form()
    elif st.session_state.authenticated == "upload_page":
        app()
    elif st.session_state.authenticated == "user_page":
        user()
        
login.py
Displaying login.py.
