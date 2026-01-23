import pandas as pd
import streamlit as st


def start_session_states():
    """Inicializa o sesseion state"""
    states = {'files_byname_q': {}}
    for k,v in states.items():
        if k not in st.session_state:
            st.session_state[k] = v

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

def set_key_id(name, sufix_id):
    """Compõe chave"""
    return "_".join([name, sufix_id])

def get_colsin(cols_in, cols_name, sufix_id):
    """Colunas necessárias"""
    for col, labels in cols_in.items():
        cols_in[col][1] = select_inline(lb=labels[0], ops=cols_name, index=None, key_id=set_key_id(col, sufix_id))

def select_inline(lb, ops, key_id, index=0,  pc=0.25):
    """Gera entrada para selecionar nome de coluna."""
    c01, c02 = st.columns([pc, 1-pc])
    c01.write(lb)
    select_in = c02.selectbox(lb, options=ops, key=key_id, index=index, label_visibility='collapsed')
    return select_in

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

def choose_xlsx(title='Input', label_up='Files', cols_in={'name':['Nome:', None], 'datetime': ['Data:', None], 'value': ['Valor:', None]}, sufix_id='01', multiple=True):
    """Expander com carregamento de arquivos xlsx."""

    with st.expander(title, expanded=True):
        files_up = st.file_uploader(label_up, 
                                    type='xlsx',  accept_multiple_files=multiple, 
                                    )
        
        files_byname = get_files_byname(files_up, multiple)
        filename = get_filename(files_byname, sufix_id)
        shtname = get_shtname(filename, files_byname, sufix_id)
        cols_name = get_colsname(files_byname, filename, shtname)
        get_colsin(cols_in, cols_name, sufix_id)

        return files_byname, filename, shtname

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
