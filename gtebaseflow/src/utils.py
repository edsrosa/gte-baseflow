import streamlit as st


def start_session_states():
    """Inicializa o sesseion state"""
    states = {'files_byname_q': {}}
    for k,v in states.items():
        if k not in st.session_state:
            st.session_state[k] = v


def select_inline(lb, ops, key_id, index=0,  pc=0.5):
    """Gera entrada para selecionar nome de coluna."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    select_in = c02.selectbox(lb, options=ops, key=key_id, index=index, label_visibility='collapsed')
    return select_in


def get_files_byname():
    """Recupera as propriedades do arquivo carregados."""
    files_byname_q  = {}
    if st.session_state.files_up_q != []:
        for f in st.session_state.files_up_q:
            files_byname_q[f.name] = f
        
    st.session_state.files_byname_q = files_byname_q
