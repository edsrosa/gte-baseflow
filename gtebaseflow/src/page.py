import streamlit as st

from src import utils


def load_input_streamflow():
    """Carregamento dos dados de vazão."""
    cols_in_sf={'datetime':['Data:', None], 'streamflow': ['Vazão (m³/s):', None]}
    utils.choose_xlsx(title="Vazão Superficial", cols_in=cols_in_sf, sufix_id='sf', data_name='station_sf', multiple=True)


def load_input_rainfall():
    """Carregamento dos dados de precipitação."""
    cols_in_plu={'datetime':['Data:', None], 'rainfall': ['Precipitação (mm):', None]}
    utils.choose_xlsx(title="Precipitação", cols_in=cols_in_plu, sufix_id='plu', data_name='station_plu')


def input_box():
    """Entrada de arquivos."""
    with st.sidebar.expander("Arquivos de Entrada", expanded=True, icon=":material/upload:"):
        load_input_streamflow()
        load_input_rainfall()


def config_box():
    """Configurações."""
    with st.sidebar.expander("Configurações", expanded=True, icon=":material/settings:"):
        area_bacia = st.number_input(label='area_bacia', label_visibility='collapsed', placeholder='Área de Bacia (km²)', min_value=0.0000001, value=None, format="%0.6f")
        start_wet = utils.get_num_month(label='Início Período Chuvoso:', index=9, key_id='start_wet')
        start_dry = utils.get_num_month(label='Início Período Seco:', index=3, key_id='start_dry')
        utils.apply_configs(area_bacia, start_wet, start_dry)


def process_box(rows):
    """Processamento"""
    with st.sidebar.expander("Processamento", expanded=True, icon=":material/view_kanban:"):
        utils.calc_baseflow(st.session_state.station_sf)
        dates_plot = utils.select_time(rows[2])
        
        utils.plot_chart_sf(st.session_state.station_sf, rows[1], dates_plot)
        show_plu = st.checkbox('Plotar gráfico de precipitação')
        if show_plu:
            utils.plot_chart_plu(st.session_state.station_plu, rows[0], dates_plot)
        bt_calc_wb = st.button("Calcular Balanço Hídrico", width='stretch', type='primary')
        if bt_calc_wb:
            utils.calc_wb()
            st.session_state.plot_wb = True

        if st.session_state.plot_wb:
            utils.plot_chart_wb(st.session_state.station_sf, st.session_state.station_plu, rows[2])


def output_box():
    """Exportação"""
    with st.sidebar.expander("Exportação dos Arquivos", expanded=True, icon=":material/download:"):
        utils.download_file()


def help_box():
    """Exportação"""
    with st.sidebar.expander("Ajuda", expanded=True, icon=":material/help:"):
        utils.load_help()


def content():
    """Conteúdo como função."""
    rows = utils.start_session(title='GTE Baseflow', nrows=3)
    input_box()
    config_box()
    process_box(rows)
    output_box()
    help_box()
    utils.load_about(st.session_state.station_sf)


baseflow = st.Page(content, 
               title="Separador de Fluxo de Base",
               icon=":material/water_drop:", 
               )
st.set_page_config(layout="wide")
