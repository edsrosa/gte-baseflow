import streamlit as st

from src.baseflow import baseflow

from src.utils import start_session_states

start_session_states()

def rodape():
    st.html("<div class='footer'>"
            "<p>© 2026 ESR Geology and Technology.</p>"
            "<p> All rights reserved.</p> </div>"
            )
    
st.html('gtebaseflow/src/style.css')

pgs = st.navigation(pages=[baseflow], position="top")

pgs.run()
rodape()
