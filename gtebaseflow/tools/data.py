import os
from math import exp

import pandas as pd


class Station():
    def __init__(self):
        """Estação e dados de vazão."""
        self.file_obj=None # Arquivo importado como objeto
        self.filename=None # Nome do arquivo importado
        self.sht_ts=None # Aba com o df da timeserie
        self.col_datetime=None # Nome da coluna data
        self.col_streamflow=None # Nome da coluna com vazão
        self.col_baseflow='baseflow' # Nome da coluna com fluxo de base
        self.name=None  # Nome da estação
        self.area_km2=None # Área da bacia em km²
        self.df_ts=None # Dataframe com os dados timeserie
    
    def set_parameters(self, file_obj, filename, sht_ts, col_datetime, col_streamflow):
        """Recupera os parâmetros para carregar a estação"""
        self.file_obj = file_obj
        self.filename = filename
        self.sht_ts = sht_ts
        self.col_datetime = col_datetime
        self.col_streamflow = col_streamflow

        if self.name == None:
            self.name = os.path.splitext(filename)[0]
        
    def load_df(self):
        """Carrega os dados do dataframe."""
        df = pd.read_excel(self.file_obj, sheet_name=self.sht_ts)
        df = df.dropna(subset=[self.col_datetime, self.col_streamflow])
        df = df.sort_values(by=[self.col_datetime])
        self.df_ts = df
        self.datetime = list(df[self.col_datetime])
        self.streamflow = list(df[self.col_streamflow])

    def calc_a_from_k(self, k):
        """Seta o falor de k e calcula o a_k a partir dele."""
        self.k = k 
        self.a_k = exp(-1/self.k)
    
    def calc_rr(self, y, rr_tn):
        """Calcula recessão inversa para um ponto."""
        a = self.a_k
        rr = rr_tn/a
        if rr > y:
            rr = y
        return rr
    
    def calc_reverse_recess(self):
        """Calcula recessão inversa para a série."""
        r_values = self.streamflow[::-1]
        n_ts = len(r_values)
        for i in range(1, n_ts):
            r_values[i] = self.calc_rr(r_values[i], r_values[i-1])

        self.reverss = r_values[::-1]
    
    def calc_bfimax(self):
        """BFImax."""
        self.bfi_max = sum(self.reverss)/sum(self.streamflow)

    def calc_b(self, y, b_tb):
        """Calcula o fluxo de base para um tempo."""
        a = self.a_k
        b = ((1 - self.bfi_max) * a * b_tb + (1 - a) * self.bfi_max * y) / (1 - a * self.bfi_max)
        if b > y:
            b = y
        return b
    
    def calc_baseflow(self):
        """Calcula o fluxo de base para toda a série histórica."""
        n_time = len(self.datetime)
        self.baseflow = []
        self.baseflow.append(self.streamflow[0])
        
        for i in range(1, n_time):
            y = self.streamflow[i]
            b_tb = self.baseflow[i-1]
            b = self.calc_b(y, b_tb, )
            self.baseflow.append(b)

    def calc_bfi(self):
        """Calcula o BFi"""
        self.bfi = sum(self.baseflow)/sum(self.streamflow)

    def calc_k_a_baseflow(self, k):
        """Faz o cálculo do fluxo de base, inclusive etapas intermediárias."""
        self.calc_a_from_k(k)
        self.calc_reverse_recess()
        self.calc_bfimax()
        self.calc_baseflow()
        self.calc_bfi()
        self.df_ts[self.col_baseflow] = self.baseflow

    def classify_season(self, start_wet, start_dry):
        """Faz classificação em período seco e chuvoso."""
        self.df_ts['season'] = 'wet'
        dry_br = (self.df_ts[self.col_datetime].dt.month >= start_dry) & (self.df_ts[self.col_datetime].dt.month < start_wet)
        self.df_ts['season'] = self.df_ts['season'].mask(dry_br, 'dry')
