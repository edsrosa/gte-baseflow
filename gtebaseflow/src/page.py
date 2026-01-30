import streamlit as st

from src import utils


def load_input_streamflow():
    """Carregamento dos dados de vazão."""
    cols_in_sf={'datetime':['Data:', None], 'streamflow': ['Vazão (m³/s):', None]}
    utils.choose_xlsx(title="Vazão Superficial", cols_in=cols_in_sf, sufix_id='sf', data_name='data_sf', multiple=True)

def load_input_rainfall():
    """Carregamento dos dados de precipitação."""
    cols_in_plu={'datetime':['Data:', None], 'rainfall': ['Precipitação (mm):', None]}
    utils.choose_xlsx(title="Precipitação", cols_in=cols_in_plu, sufix_id='plu', data_name='data_plu')


def input_box():
    """Entrada de arquivos."""
    with st.sidebar.expander("Arquivos de Entrada", expanded=True):
        load_input_streamflow()
        load_input_rainfall()

def config_box():
    """Configurações."""
    with st.sidebar.expander("Configurações", expanded=True):
        name_station = st.text_input(label='name_station', label_visibility='collapsed', placeholder='Nome da Estação')
        area_bacia = st.number_input(label='area_bacia', label_visibility='collapsed', placeholder='Área de Bacia (km²)', min_value=0.0000001, value=None, format="%0.6f")
        start_wet = utils.get_num_month(label='Início Período Chuvoso:', index=9, key_id='start_wet')
        start_dry = utils.get_num_month(label='Início Período Seco:', index=3, key_id='start_dry')

        utils.apply_configs(name_station, area_bacia, start_wet, start_dry)

def process_box(row):
    """Processamento"""
    with st.sidebar.expander("Processamento", expanded=True):
        utils.calc_baseflow(st.session_state.station)
        utils.plot_chart_sf(st.session_state.station, row)
        
def output_box():
    """Exportação"""
    with st.sidebar.expander("Exportação dos Arquivos", expanded=True):
        if st.button('Baixar Dados', width='stretch', type='primary'):
            st.write("Baixou!")

def help_box():
    """Exportação"""
    with st.sidebar.expander("Ajuda", expanded=True):
        utils.load_help()


def content():
    """Conteúdo como função."""
    rows = utils.start_session(title='GTE Baseflow', nrows=3)
    input_box()
    config_box()
    process_box(rows[2])
    output_box()
    help_box()
    utils.clear_sessions(st.session_state.data_sf)
    utils.load_about(st.session_state.data_sf)


baseflow = st.Page(content, 
               title="Separador de Fluxo de Base",
               icon=":material/water_drop:", 
               )
st.set_page_config(layout="wide")
