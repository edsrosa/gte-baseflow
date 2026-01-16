import os
import pandas as pd


class Station():
    def __init__(self):
        """Estação e dados de vazão."""
        self.file_obj=None # Arquivo importado como objeto
        self.filename=None # Nome do arquivo importado
        self.sht_ts=None # Aba com o df da timeserie
        self.name=None  # Nome da estação
        self.df_ts=None # Dataframe com os dados time série
        self.cols=None # Mapeamento com a relação dos nomes das colunas
    
    def set_parameters(self, file_obj, filename, sht_ts):
        """Recupera os parâmetros para carregar a estação"""
        self.file_obj = file_obj
        self.filename = filename
        self.sht_ts = sht_ts

        if self.name == None:
            self.name = os.path.splitext(filename)[0]
    
    def load_df(self):
        """Carrega os dados do dataframe."""
        self.df_ts = pd.read_excel(self.file_obj, sheet_name=self.sht_ts)
