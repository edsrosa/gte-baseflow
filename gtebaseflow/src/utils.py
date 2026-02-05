import os

import pandas as pd
import streamlit as st

from tools import use


def start_session_states():
    """Inicializa o session state"""
    states = {'station_sf': None, 
              'station_plu': None,
              'plot_wb': False}
    for k,v in states.items():
        if k not in st.session_state:
            st.session_state[k] = v


def start_session(title, nrows=1):
    start_session_states()
    """Incializa titulos e containers."""
    st.sidebar.html(f"""<div class="body-center"> <b>{title}</b> </div>""")
    rows = []
    for n in range(nrows):
        rows.append(st.container())
    return rows


def clear_sessions(data):
    """Reinicializa os sessions states se o arquivo de entrada é retirada."""
    if data == None:
        st.session_state['station'] = None


def load_about(data):
    """Carrega a página inicial sobre a ferramenta caso não haja arquivo carregado."""
    if data == None:
        st.html('gtebaseflow/src/about.html')


def load_help():
    """Carrega a página de ajuda sobre a ferramenta."""
    st.html('gtebaseflow/src/help.html')


def set_key_id(name, sufix_id):
    """Compõe chave"""
    return "_".join([name, sufix_id])


def select_inline(lb, ops, key_id, index=0,  pc=0.3):
    """Gera entrada para selecionar nome de coluna."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    select_in = c02.selectbox(lb, options=ops, key=key_id, index=index, label_visibility='collapsed')
    return select_in


def num_in_inline(lb, value, pc=0.3):
    """Entrada de número."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    num_in = c02.number_input(label=lb, value=value, label_visibility='collapsed')
    return num_in


def get_colsin(cols_in, cols_name, sufix_id):
    """Colunas necessárias"""
    for col, labels in cols_in.items():
        cols_in[col][1] = select_inline(lb=labels[0], ops=cols_name, index=None, key_id=set_key_id(col, sufix_id))


def get_files_byname(files_up, multiple):
    """Recupera as propriedades do arquivo carregados."""
    files_byname  = {}
    if multiple:
        files_in = files_up.copy()
    else:
        files_in = [files_up]

    if files_in != [] and files_in != [None]:
        for f in files_in:
            files_byname[f.name] = f
    return files_byname


def get_filename(files_byname, sufix_id):
    """Recupera o nome do arquivo atual."""
    filename = None
    if files_byname != {}:
        filename = select_inline(lb="Arquivo: ", ops=files_byname.keys(), key_id=set_key_id('filename', sufix_id), index=0)
    return filename


def get_shtname(filename, files_byname, sufix_id):
    """Recupera o nome da aba atual."""
    shtname = None
    if filename is not None and files_byname != {}:
        file = files_byname[filename]
        shtnames = list(pd.ExcelFile(file).sheet_names)
        shtname = select_inline(lb="Planilha:", ops=shtnames, key_id=set_key_id('shtname', sufix_id))
    return shtname


def get_colsname(files_byname, filename, shtname):
    """Recupera o nome das colunas do arquivo atual."""
    cols_name = []
    if shtname is not None:
        df = pd.read_excel(files_byname[filename], sheet_name=shtname)
        cols_name = list(df.columns)
    return cols_name


def choose_xlsx(title='Input', data_name='data', label_up='Files', cols_in={'name':['Nome:', None], 'datetime': ['Data:', None], 'value': ['Valor:', None]}, sufix_id='01', multiple=False):
    """Expander com carregamento de arquivos xlsx."""
    with st.expander(title, expanded=False):
        files_up = st.file_uploader(set_key_id(name=label_up, sufix_id=sufix_id), 
                                    type='xlsx',  accept_multiple_files=multiple, 
                                    label_visibility='collapsed'
                                    )
        files_byname = get_files_byname(files_up, multiple)
        filename = get_filename(files_byname, sufix_id)
        shtname = get_shtname(filename, files_byname, sufix_id)
        cols_name = get_colsname(files_byname, filename, shtname)
        get_colsin(cols_in, cols_name, sufix_id)
        name_station = st.text_input(label='name_station', label_visibility='collapsed', placeholder='Nome da Estação', key=set_key_id(name='name', sufix_id=sufix_id))

        bt_load = st.button('Carregar Dados', type='primary', width='stretch', key=set_key_id(name='bt_load', sufix_id=sufix_id))
        if bt_load:
            df = pd.read_excel(files_byname[filename], sheet_name=shtname)
            if data_name == 'station_sf':
                station = use.create_station(df, cols_in, name_station, filename)
            elif data_name == 'station_plu':
                station = use.create_station_plu(df, cols_in, name_station)

            st.session_state[data_name] = station
        
        if files_up is None or files_up == []:
            st.session_state[data_name] = None


def get_value(label, key_values, key_id, index=None):
    """Recupera o tipo de dado"""
    value = select_inline(lb=label, ops=key_values.keys(), key_id=key_id, index=index)
    if value == None:
        return value
    else:
        return key_values[value]


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


def apply_configs(area_bacia, start_wet, start_dry):
    """Recupera as configurações."""
    bt_apply_configs = st.button("Carregar Configurações", width='stretch', type='primary')

    if bt_apply_configs:
        st.session_state['wet_dry'] = {'wet': start_wet, 'dry': start_dry}
        use.insert_configs_station(st.session_state.station_sf, area_bacia)
        use.classify_season_hydroyears(st.session_state.station_sf, start_wet, start_dry)


def calc_baseflow(station):
    "Faz seleção do k e cálculo do baseflow."
    k_value = num_in_inline(lb="α (1/s):", value=100)
    if station is not None:
        use.calc_baseflow(station, k_value)


def select_time(row):
    """Range slider com o período de plotagem dos gráficos"""
    if st.session_state.station_sf is not None:
        dates = use.get_dates_range(st.session_state.station_sf)
        dates_plot = row.slider(label='Intervalo Data', 
                                label_visibility='collapsed', 
                                value=dates,
                                format='DD/MM/YYYY')
        return dates_plot


def select_ymax_sf(row):
    """Slider para o eixo y."""
    if st.session_state.station_sf is not None:
        y_max_sf = use.get_value_max_sf(st.session_state.station_sf)
        y_plot_sf = row.slider(label="max_sf",
                              label_visibility='collapsed',
                              min_value=0,
                              max_value=y_max_sf,
                              value=y_max_sf)
        return y_plot_sf


def calc_wb():
    """Faz cálculos da precipitação, como parte dos cálculos do balanço."""
    use.calc_volume_sf(st.session_state.station_sf)
    if st.session_state.station_plu is not None:
        use.classify_season_hydroyears_plu(st.session_state.station_plu, st.session_state.wet_dry['wet'],st.session_state.wet_dry['dry'])
        use.calc_rainfall_sum_vol(st.session_state.station_plu, st.session_state.station_sf.area_km2)
        use.join_sf_plu(st.session_state.station_sf, st.session_state.station_plu)

 
def plot_chart_sf(station, row, range_x):
    """Plota o grafico gerado."""
    if station is not None:
        fig_sf = use.create_chart_sf(station.df_ts, station.col_datetime, station.col_streamflow, station.col_baseflow, station.name, range_x)
        row.plotly_chart(fig_sf.fig)


def plot_chart_plu(station, row, range_x):
    """Plota o grafico gerado."""
    if station is not None:
        fig_plu = use.create_chart_plu(station.df_ts, station.col_datetime, station.col_rainfall, name=station.name, range_x=range_x)
        row.plotly_chart(fig_plu.fig)


def plot_chart_wb(station, station_plu, row):
    """Plota o grafico gerado."""
    if station is not None:
        fig_wb = use.create_chart_wb(station.df_hy, station.col_yearhydro, station.col_streamflow_vol, station.col_baseflow_vol, station_plu.col_rainfall_vol, name=station.name)
        row.plotly_chart(fig_wb.fig)


def download_file(station, plot_wb):
    """Cria e baixa arquivo com dfs."""
    if plot_wb:
        file = use.create_xlsx(station)
        st.download_button('Baixar Dados', 
                       data=file,
                       file_name=station.filename_out,
                       type="primary",
                       width='stretch')

# old functions
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


def get_value_ops(label, value_in, value_ops, key_id):
    """Recupera a a opção a partir de uma lista de opções"""
    if value_in == None:
        ops = []
    else:
        ops = value_ops[value_in]
    op = select_inline(lb=label, ops=ops, key_id=key_id)
    return op


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
