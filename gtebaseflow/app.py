import streamlit as st

from src.baseflow import baseflow


def rodape():
    st.html("<div class='footer'>"
            "<p>© 2026 ESR Geology and Technology.</p>"
            "<p> All rights reserved.</p> </div>"
            )
    
st.html('gtebaseflow/pages/style.css')

pgs = st.navigation(pages=[baseflow], position="top")

pgs.run()
rodape()
