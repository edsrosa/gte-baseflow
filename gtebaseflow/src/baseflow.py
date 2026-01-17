import pandas as pd
import streamlit as st

from tools.data import Station
from tools.viewer import Fig2D


def select_inline(lb, ops, key_id, index=0,  pc=0.5):
    """Gera entrada para selecionar nome de coluna."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    select_in = c02.selectbox(lb, options=ops, key=key_id, index=index, label_visibility='collapsed')
    return select_in


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


def get_filenames(files_up):
    """Recupera as propriedades do arquivo carregados."""
    files_byname  = {}
    if files_up != []:
        for f in files_up:
            files_byname[f.name] = f
    return files_byname


def get_shtnames(filename, files_byname):
    """Recupera as abas do arquivo atual."""
    if filename is not None:
        file = files_byname[filename]
        shts_name = list(pd.ExcelFile(file).sheet_names)
    else:
        shts_name = []
    return shts_name


def get_colsname(files_byname, filename, sht_name):
    """Recupera o nome das colunas do arquivo atual."""
    cols_name = []
    if sht_name is not None:
        df = pd.read_excel(files_byname[filename], sheet_name=sht_name)
        cols_name = list(df.columns)
    return cols_name


def get_cols_types(df):
    """Retorna os tipos das colunas como um dicionario."""
    dtys = list(df.dtypes.unique())
    dtypes_cols = {dty: [] for dty in dtys}
    dtypes_cols['all']=[]
    nm_dty = dict(df.dtypes)
    for nm, dty in nm_dty.items():
         dtypes_cols[dty].append(nm)
         dtypes_cols['all'].append(nm)
    return dtypes_cols


def get_value(label, key_values, key_id, index=None):
    """Recupera o tipo de dado"""
    value = select_inline(lb=label, ops=key_values.keys(), key_id=key_id, index=index)

    if value == None:
        return value
    else:
        return key_values[value]


def get_value_ops(label, value_in, value_ops, key_id):
    """Recupera a a opção a partir de uma lista de opções"""
    if value_in == None:
        ops = []
    else:
        ops = value_ops[value_in]
    op = select_inline(lb=label, ops=ops, key_id=key_id)
    return op


def get_num_month(label, index, key_id):
    """Recupera mês de início do perído chuvoso e seco."""
    months = {'Janeiro': 1,
                'Fevereiro': 2,
                'Março': 3,
                'Abril': 4,
                'Maio':5,
                'Junho':6,
                'Julho':7,
                'Agosto':8,
                'Setembro':9,
                'Outubro': 10,
                'Novembro': 11,
                'Dezembro':12}
    month = get_value(label=label, key_values=months, key_id=key_id, index=index)
    return month


def get_type_plu(label, index, key_id):
    """Recupera o tipo de série histórica de precipitação."""
    types_plu= {'Diário - Média': 1,
                'Diário - Acumulado': 2,
                'Semanal - Média': 3,
                'Semanal - Acumulado': 4,
                'Mensal - Média':5,
                'Mensal - Acumulado':6,
                'Anual - Média':7,
                'Anual - Acumulado':8,
                }
    type_plu = get_value(label=label, key_values=types_plu, key_id=key_id, index=index)
    return type_plu


def load_station(files_byname, filename, sht_name, col_datetime, col_streamflow):
    """Carrega a estação"""
    if col_datetime is not None and col_streamflow is not None:
        station = Station()
        station.set_parameters(file_obj=files_byname[filename],
                            filename=filename,
                            sht_ts=sht_name,
                            col_datetime=col_datetime,
                            col_streamflow=col_streamflow
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


def classify_season(start_wet, start_dry):
    """Faz classificação dos períodos chuvoso e seco."""
    if 'station' in st.session_state:
        classify = 'classes'


def calc_baseflow(k):
    """Faz o cálculo do fluxo de base e etapas intermediárias."""
    if 'station' in st.session_state:
        st.session_state.station.calc_k_a_baseflow(k)


def plot_chart(row02):
    """Faz plotagem do gráfico com as vazões"""
    fig_q = Fig2D()
    if 'station' in st.session_state:
        dates = st.session_state.station.df_ts[st.session_state.station.col_datetime]
        streamflows = st.session_state.station.df_ts[st.session_state.station.col_streamflow]
        baseflows = st.session_state.station.df_ts[st.session_state.station.col_baseflow]
        fig_q.load_traces(dates, streamflows, baseflows)

    fig_q.create_fig()
    if 'station' in st.session_state:
        fig_q.update_layout(title=st.session_state.station.name)
    
    row02.plotly_chart(fig_q.fig)


def input_box():
    """Entrada de arquivos."""
    with st.sidebar.expander("Arquivos de Entrada", expanded=True):
        files_up = st.file_uploader('Carregue o(s) arquivo(s) de vazão:', type='xlsx',  accept_multiple_files=True)
        files_byname = get_filenames(files_up)
        filename = select_inline(lb="Arquivo:", ops=files_byname.keys(), key_id='filename_q')
        shts_name = get_shtnames(filename, files_byname)
        sht_name = select_inline(lb="Planilha:", ops=shts_name, key_id='sht_name_q')
        cols_name = get_colsname(files_byname, filename, sht_name)
        col_datetime = select_inline(lb='Data:', ops=cols_name, index=None, key_id='col_datetime_q')
        col_streamflow = select_inline(lb='Vazão (m³/s):', ops=cols_name, index=None, key_id='col_streamflow_q')
        load_station(files_byname, filename, sht_name, col_datetime, col_streamflow)

        with st.expander('Precipitação'):
            st.info('Dados de precipitação são opcionais, porém enriquecem a análise.')
            files_up_plu = st.file_uploader('Carregue o arquivo de precipitação:', type='xlsx',  accept_multiple_files=False)
            if files_up_plu != None:
                files_up_plu = [files_up_plu]
            else:
                files_up_plu = []
            
            files_byname_plu = get_filenames(files_up_plu)
            filename_plu = select_inline(lb="Arquivo:", ops=files_byname_plu.keys(), key_id='filename_plu')
            shts_name_plu = get_shtnames(filename_plu, files_byname_plu)
            sht_name_plu = select_inline(lb="Planilha:", ops=shts_name_plu, key_id='sht_name_plu')
            cols_name_plu = get_colsname(files_byname_plu, filename_plu, sht_name_plu)
            col_datetime_plu = select_inline(lb='Data:', ops=cols_name_plu, index=None, key_id='col_datetime_plu')
            col_value_plu = select_inline(lb='Precipitação (mm):', ops=cols_name_plu, index=None, key_id='col_value_plu')
            type_plu = get_type_plu(label="Tipo de Dados:", index=0, key_id='type_plu')


def config_box():
    """Configurações."""
    with st.sidebar.expander("Configuração", expanded=True):
        name_station = st.text_input(label='name_station', label_visibility='collapsed', placeholder='Nome da Estação')
        area_bacia = st.number_input(label='area_bacia', label_visibility='collapsed', placeholder='Área de Bacia (km²)', min_value=0.0000001, value=None, format="%0.6f")
        start_wet = get_num_month(label='Início Período Chuvoso:', index=9, key_id='start_wet')
        start_dry = get_num_month(label='Início Período Seco:', index=3, key_id='start_dry')

        get_configs(name_station, area_bacia, start_wet, start_dry)
        classify_season(start_wet, start_dry)


def process_box(row02):
    """Processamento"""
    with st.sidebar.expander("Processamento", expanded=True):
        k_value = num_in_inline(lb="α (1/s):", value=100)
        calc_baseflow(k=k_value)
        plot_chart(row02)


def output_box():
    """Exportação"""
    with st.sidebar.expander("Exportação dos Arquivos", expanded=True):
        st.button('Export', width='stretch')


def content():
    """Conteúdo como função."""
    st.sidebar.markdown("""## Separador de Fluxo de Base""")
    row01 = st.container()
    row02 = st.container()
    row03 = st.container()
    input_box()
    config_box()
    process_box(row02)
    output_box()


baseflow = st.Page(content, 
               title="Separador de Fluxo de Base",
               icon=":material/water_drop:", 
               )
st.set_page_config(layout="wide")
