"""Supports authentication page."""


import streamlit as st
import streamlit_authenticator as stauth
from modules.deta import (get_config_from_deta, init_deta_drive,
                          CONFIG_FN, dump_dict_to_yaml_stringio,
                          save_config_to_deta)


config = get_config_from_deta()


def get_auth():    
    return stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )


def get_login(authenticator):
    authenticator.login('Login', 'main')

    if st.session_state["authentication_status"]:
        st.write(f'Logged username: **{st.session_state.username}**')

    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    else:
        st.error('Username/password is incorrect')


def get_register(authenticator):
    try:
        if authenticator.register_user('Register user', 'main', preauthorization=False):
            save_config_to_deta(config)
            st.success('Registration is successful!')
    except Exception as e:
        st.error(e)


def get_logout(authenticator):
    st.markdown(f'''Welcome **{st.session_state["name"]}**''')
    authenticator.logout('Logout', 'main', key='unique_key')
    