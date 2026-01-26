import pandas as pd
import streamlit as st

from tools.data import Station
from tools.viewer import Fig2D
from src import utils


def load_about(row):
    """Carrega a página sobre caso não haja arquivo carregado."""
    row.html('gtebaseflow/src/about.html')


def num_in_inline(lb, value, pc=0.5):
    """Entrada de número."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    num_in = c02.number_input(label=lb, value=value, label_visibility='collapsed')
    return num_in


def text_in_inline(lb, value, pc=0.5):
    """Entrada de texto."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    txt_in = c02.text_input(label=lb, value=value, label_visibility='collapsed')
    return txt_in


def load_station(files_byname, filename, sht_name, cols_in_q):
    """Carrega a estação"""
    if cols_in_q['datetime'][1] is not None and cols_in_q['streamflow'][1] is not None:
        station = Station()
        station.set_parameters(file_obj=files_byname[filename],
                            filename=filename,
                            sht_ts=sht_name,
                            col_datetime=cols_in_q['datetime'][1],
                            col_streamflow=cols_in_q['streamflow'][1]
                            )
        station.load_df()
        st.session_state['station'] = station
    else:
        if 'station' in st.session_state:
            del st.session_state['station']


def get_configs(name_station, area_bacia, start_wet, start_dry):
    """Recupera as configurações."""
    if 'station' in st.session_state:
        st.session_state.station.name=name_station
        st.session_state.station.area_km2=area_bacia


def classify_season_hydroyear(start_wet, start_dry):
    """Faz classificação dos períodos chuvoso e seco."""
    if 'station' in st.session_state:
        st.session_state.station.classify_season(start_wet, start_dry)
        st.session_state.station.classify_hydroyears(start_wet)


def calc_baseflow(k):
    """Faz o cálculo do fluxo de base e etapas intermediárias."""
    if 'station' in st.session_state:
        st.session_state.station.calc_k_a_baseflow(k)


def plot_chart(row02):
    """Faz plotagem do gráfico com as vazões"""
    if 'station' in st.session_state:
        fig_q = Fig2D()
        dates = st.session_state.station.df_ts[st.session_state.station.col_datetime]
        streamflows = st.session_state.station.df_ts[st.session_state.station.col_streamflow]
        baseflows = st.session_state.station.df_ts[st.session_state.station.col_baseflow]
        fig_q.load_traces(dates, streamflows, baseflows)
        fig_q.create_fig()
        fig_q.update_layout(title=st.session_state.station.name)
        row02.plotly_chart(fig_q.fig)


def load_streamflow(row01):
    """Carregamento dos dados de vazão"""
    cols_in_q = {'datetime': ['Data:', None], 
                'streamflow': ['Vazão (m³/s):', None]}
    files_byname_q, filename_q, shtname_q = utils.choose_xlsx(title="Vazão", 
                    label_up="Carregue os arquivos de vazão:",
                    cols_in=cols_in_q,
                    sufix_id='q',
                    multiple=True)
    
    if files_byname_q != {}:
        load_station(files_byname_q, filename_q, shtname_q, cols_in_q)
    else:
        load_about(row01)


def load_rainfall():
    """Carregamento dos dados de precipitação"""
    cols_in_plu = {'datetime': ['Data:', None], 
                    'rainfall': ['Precipitação (mm):', None]}
    files_byname_plu, filename_plu, shtname_plu = utils.choose_xlsx(title="Precipitação", 
                    label_up="Carregue o arquivo de precipitação:",
                    cols_in=cols_in_plu,
                    sufix_id='plu',
                    multiple=False)


def export_dfs():
    """Exporta os dados atuais para arquivo Excel."""
    buffer = st.session_state.station.export_dfs()
    filename_output = st.session_state.station.filename_output
    return buffer, filename_output


def input_box(row01):
    """Entrada de arquivos."""
    with st.sidebar.expander("Arquivos de Entrada", expanded=True):
        load_streamflow(row01)
        load_rainfall()


def config_box():
    """Configurações."""
    with st.sidebar.expander("Configurações", expanded=True):
        name_station = st.text_input(label='name_station', label_visibility='collapsed', placeholder='Nome da Estação')
        area_bacia = st.number_input(label='area_bacia', label_visibility='collapsed', placeholder='Área de Bacia (km²)', min_value=0.0000001, value=None, format="%0.6f")
        start_wet = utils.get_num_month(label='Início Período Chuvoso:', index=9, key_id='start_wet')
        start_dry = utils.get_num_month(label='Início Período Seco:', index=3, key_id='start_dry')

        get_configs(name_station, area_bacia, start_wet, start_dry)
        classify_season_hydroyear(start_wet, start_dry)
        # type_plu = utils.get_type_plu(label="Dados Precipitação:", index=0, key_id='type_plu')


def process_box(row02):
    """Processamento"""
    with st.sidebar.expander("Processamento", expanded=True):
        k_value = num_in_inline(lb="α (1/s):", value=100)
        calc_baseflow(k=k_value)
        plot_chart(row02)


def output_box():
    """Exportação"""
    with st.sidebar.expander("Exportação dos Arquivos", expanded=True):
        if st.button('Preparar Dados para Download', width='stretch'):
            dfs_down = export_dfs()
            st.download_button('Baixar dados', data=dfs_down[0], file_name=dfs_down[1], width='stretch')


def content():
    """Conteúdo como função."""
    st.sidebar.markdown("""## GTE Baseflow""")
    row01 = st.container()
    row02 = st.container()
    row03 = st.container()
    input_box(row01)
    config_box()
    process_box(row02)
    output_box()


baseflow = st.Page(content, 
               title="Separador de Fluxo de Base",
               icon=":material/water_drop:", 
               )
st.set_page_config(layout="wide")
