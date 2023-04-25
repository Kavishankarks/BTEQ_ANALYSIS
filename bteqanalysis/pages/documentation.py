import streamlit as st
def display_docs():
    """
    Displays documentation for your Streamlit app.
    """
    st.title('Documentation')

    st.header('Introduction')
    st.write('Welcome to my Streamlit app! This app allows you to ...')

    st.header('Usage')
    st.write('To use this app, simply ...')

    st.header('FAQ')
    st.write('Q: What do I do if ...')
    st.write('A: You can ...')

    st.header('Contact')
    st.write('If you have any questions or feedback, please contact us at ...')