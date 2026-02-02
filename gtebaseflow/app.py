import streamlit as st

from src.page import baseflow


def rodape():
    st.html("<div class='footer'>"
            "<p><a href='https://github.com/edsrosa' target='_blank'>© 2026 Ednilson Rosa.</a></p>"
            "</div>"
            )
    
st.html('gtebaseflow/src/style.css')

pgs = st.navigation(pages=[baseflow], position="top")

pgs.run()
rodape()
