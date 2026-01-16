import pandas as pd
import streamlit as st

from models.data import Station

def select_inline(lb, ops, index=0,  pc=0.5):
    """Gera entrada para selecionar nome de coluna."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    select_in = c02.selectbox(lb, options=ops, label_visibility='collapsed', index=index)
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
    if files_byname != {}:
        file = files_byname[filename]
        shts_name = list(pd.ExcelFile(file).sheet_names)
    else:
        shts_name = []
    return shts_name


def get_colsname(files_byname, filename, sht_name):
    """Recupera o nome das colunas do arquivo atual."""
    cols_name = []
    if files_byname != {}:
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


def get_value(label, key_values, index=None):
    """Recupera o tipo de dado"""
    value = select_inline(lb=label, ops=key_values.keys(), index=index)

    if value == None:
        return value
    else:
        return key_values[value]

def get_value_ops(label, value_in, value_ops):
    """Recupera a a opção a partir de uma lista de opções"""
    if value_in == None:
        ops = []
    else:
        ops = value_ops[value_in]
    op = select_inline(lb=label, ops=ops)
    return op

def get_num_month(label, index):
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
    month = get_value(label=label, key_values=months, index=index)
    return month

def load_station(files_byname, filename, sht_name, col_datetime, col_streamflow):
    """Carrega a estação"""
    if col_datetime is not None and col_streamflow is not None:
        station = Station()
        station.set_parameters(file_obj=files_byname[filename],
                            filename=filename,
                            sht_ts=sht_name)
    
        station.load_df()
    
        st.session_state['station'] = station
    
    else:
        if 'station' in st.session_state:
            del st.session_state['station']

def classify_season(start_wet, start_dry):
    """Faz classificação dos períodos chuvoso e seco."""
    if 'station' in st.session_state:
        classify = 'classes'


def plot_chart():
    """Faz plotagem do gráfico com as vazões"""
    if 'station' in st.session_state:
        fig = 'fig'


def input_box():
    """Entrada de arquivos."""
    with st.sidebar.expander("Input", expanded=True):
        files_up = st.file_uploader('Carregue os arquivos de entrada', type='xlsx',  accept_multiple_files=True)
        files_byname = get_filenames(files_up)
        filename = select_inline(lb="Arquivo:", ops=files_byname.keys())
        shts_name = get_shtnames(filename, files_byname)
        sht_name = select_inline(lb="Planilha:", ops=shts_name)
        cols_name = get_colsname(files_byname, filename, sht_name)
        col_datetime = select_inline(lb='Data:', ops=cols_name, index=None)
        col_streamflow = select_inline(lb='Vazão (m³/s):', ops=cols_name, index=None)
        load_station(files_byname, filename, sht_name, col_datetime, col_streamflow)


def config_box():
    """Configurações."""
    with st.sidebar.expander("Config", expanded=True):
        name = text_in_inline(lb="Estação:", value='Estação', pc=0.5)
        start_wet = get_num_month(label='Início Período Chuvoso:', index=9)
        start_dry = get_num_month(label='Início Período Seco:', index=3)
        classify_season(start_wet, start_dry)


def process_box():
    """Processamento"""
    with st.sidebar.expander("Process", expanded=True):
        k_value = num_in_inline(lb="α (1/s):", value=100)

def output_box():
    """Exportação"""
    with st.sidebar.expander("Output", expanded=True):
        plot_chart()

def content():
    """Conteúdo como função."""
    st.sidebar.markdown("""## Separador de Fluxo de Base""")
    input_box()
    config_box()
    process_box()
    output_box()


baseflow = st.Page(content, 
               title="Separador de Fluxo de Base",
               icon=":material/water_drop:",
               )
