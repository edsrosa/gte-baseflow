import os
from math import exp
import io

import pandas as pd


class Station():
    def __init__(self):
        """Estação e dados de vazão."""
        self.df_ts=None # Dataframe com os dados timeserie
        self.df_hy=None # Dataframe com dados agrupados por ano hidrológico.
        self.col_datetime=None # Nome da coluna data
        self.col_streamflow=None # Nome da coluna com vazão
        self.col_baseflow='FluxoBase_m3s' # Nome da coluna com fluxo de base
        self.col_season='Periodo'
        self.col_yearhydro='AnoHidrologico'
        self.col_streamflow_vol="FluxoTotal_m3"
        self.col_baseflow_vol="FluxoBase_m3"
        self.name=None  # Nome da estação
        self.area_km2=None # Área da bacia em km²
        self.filename_in=None
        self.filename_out=None       


    def load_df(self, df, col_datetime, col_streamflow, filename_in):
        """Carrega os dados do dataframe."""
        self.col_datetime = col_datetime
        self.col_streamflow = col_streamflow
        df = df.dropna(subset=[col_datetime, col_streamflow])
        df = df.sort_values(by=[col_datetime])
        self.df_ts = df
        self.datetime = list(df[col_datetime])
        self.streamflow = list(df[col_streamflow])
        self.filename_in = filename_in
        self.filename_out = filename_in.replace('.xlsx', '_calculado.xlsx')


    def classify_season(self, start_wet, start_dry):
        """Faz classificação em período seco e chuvoso."""
        self.df_ts[self.col_season] = 'Chuvoso'
        dry_br = (self.df_ts[self.col_datetime].dt.month >= start_dry) & (self.df_ts[self.col_datetime].dt.month < start_wet)
        self.df_ts[self.col_season] = self.df_ts[self.col_season].mask(dry_br, 'Seco')
    

    def classify_hydroyear(self, date, start_wet):
        """Faz classificação do ano hidro para cada data."""
        if date.dt.month >= start_wet:
            start_year =  date.dt.year
        else:
            start_year =  date.dt.year - 1
        hydroyear = str(start_year) + '-' + str(start_year + 1)
        return hydroyear


    def classify_hydroyears(self, start_wet):
        """Classificação do ano hidrológico.
        Considera que ano hidrológico começa no primeiro dia do período chuvoso."""
        #self.df_ts[self.col_yearhydro] = self.df_ts[self.col_datetime].apply(self.classify_hydroyear, args=(start_wet,))
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_datetime].dt.year
        start_y = self.df_ts[self.col_datetime].dt.month < start_wet
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_yearhydro].mask(start_y, self.df_ts[self.col_yearhydro]-1)
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_yearhydro].astype('str') + '-' + (self.df_ts[self.col_yearhydro] +1).astype('str')


    def calc_a_from_k(self, k):
        """Seta o falor de k e calcula o a_k a partir dele."""
        self.k = k 
        self.a_k = exp(-1/self.k)
    

    def calc_rr(self, y, rr_tn):
        """Calcula recessão inversa para um ponto."""
        a = self.a_k
        rr = rr_tn/a
        if rr > y or rr == 0:
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


    def calc_volume(self):
        """Faz cálculo do volume para o balanço hídrico."""
        max_date = self.df_ts[self.col_datetime].max() + pd.Timedelta(days=1)
        n_days_lag = (self.df_ts[self.col_datetime].shift(-1, fill_value=max_date) - self.df_ts[self.col_datetime]).dt.days

        self.df_ts[self.col_streamflow_vol] = self.df_ts[self.col_streamflow]*86400*(n_days_lag)
        self.df_ts[self.col_baseflow_vol] = self.df_ts[self.col_baseflow]*86400*(n_days_lag)

        df_hy = self.df_ts[[self.col_yearhydro, self.col_streamflow_vol, self.col_baseflow_vol]]

        self.df_hy = df_hy.groupby([self.col_yearhydro]).sum().reset_index()


    def join_plu(self, df_hy_plu, col_yearhydro_plu):
        """Une dados de precipitação ao df de vazão."""
        self.df_hy = pd.merge(self.df_hy, df_hy_plu, left_on=self.col_yearhydro, right_on=col_yearhydro_plu)
    

    def create_file(self):
        """Cria arquivo Excel para exportação."""
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            self.df_ts.to_excel(writer, index=False, sheet_name='FluxoBase')
            self.df_hy.to_excel(writer, index=False, sheet_name='AnoHidrologico')
        return buffer


class StationPlu():
    def __init__(self):
        """Estação e dados de precipitação."""
        self.df_ts=None # Dataframe com os dados timeserie
        self.df_hy=None # Dataframe com dados agrupados por ano hidrológico.
        self.col_datetime=None # Nome da coluna data
        self.col_rainfall=None # Nome da coluna com precipitação
        self.col_season='Periodo'
        self.col_yearhydro='AnoHidrologico'
        self.col_rainfall_vol="Pluviometria_m3"
        self.name=None  # Nome da estação


    def load_df(self, df, col_datetime, col_rainfall):
        """Carrega os dados do dataframe."""
        self.col_datetime = col_datetime
        self.col_rainfall = col_rainfall
        df = df.dropna(subset=[col_datetime, col_rainfall])
        df = df.sort_values(by=[col_datetime])
        self.df_ts = df


    def classify_season(self, start_wet, start_dry):
        """Faz classificação em período seco e chuvoso."""
        self.df_ts[self.col_season] = 'Chuvoso'
        dry_br = (self.df_ts[self.col_datetime].dt.month >= start_dry) & (self.df_ts[self.col_datetime].dt.month < start_wet)
        self.df_ts[self.col_season] = self.df_ts[self.col_season].mask(dry_br, 'Seco')
    

    def classify_hydroyear(self, date, start_wet):
        """Faz classificação do ano hidro para cada data."""
        if date.dt.month >= start_wet:
            start_year =  date.dt.year
        else:
            start_year =  date.dt.year - 1
        hydroyear = str(start_year) + '-' + str(start_year + 1)
        return hydroyear


    def classify_hydroyears(self, start_wet):
        """Classificação do ano hidrológico.
        Considera que ano hidrológico começa no primeiro dia do período chuvoso."""
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_datetime].dt.year
        start_y = self.df_ts[self.col_datetime].dt.month < start_wet
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_yearhydro].mask(start_y, self.df_ts[self.col_yearhydro]-1)
        self.df_ts[self.col_yearhydro] = self.df_ts[self.col_yearhydro].astype('str') + '-' + (self.df_ts[self.col_yearhydro] +1).astype('str')


    def calc_rainfall_sum(self):
        """Faz cálculo dos volumes precipitados por ano hidro"""
        self.df_hy = self.df_ts[[self.col_yearhydro, self.col_rainfall]].groupby(self.col_yearhydro).sum().reset_index()


    def calc_rainfall_volume(self, area_km2):
        """Cálcula o volume precipitado na bacia"""
        self.df_hy[self.col_rainfall_vol] = self.df_hy[self.col_rainfall] * 1000 * area_km2
