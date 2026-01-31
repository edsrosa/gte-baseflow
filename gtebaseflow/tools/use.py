import pandas as pd

from tools.database import Station
from tools.viewer import Fig2D


def create_station(df, cols_in, name_station):
    """Cria a Station e faz alguns tratamentos"""
    col_datetime = cols_in['datetime'][1]
    col_streamflow = cols_in['streamflow'][1]
    station = Station()
    station.load_df(df, col_datetime, col_streamflow)
    station.name=name_station
    return station


def get_dates_range(station):
    """Recupera a data mímima e máxima com dados."""
    date_min = (station.df_ts[station.col_datetime].min()).to_pydatetime()
    date_max = (station.df_ts[station.col_datetime].max()).to_pydatetime()
    return (date_min, date_max)


def get_value_max_sf(station):
    """Recupera o maior valor da série."""
    y_max = station.df_ts[station.col_streamflow].max()
    y_max = int(y_max)
    return y_max


def insert_configs_station(station, area_bacia):
    """Insere configurações na estação."""
    station.area_km2=area_bacia


def classify_season_hydroyears(station, start_wet, start_dry):
    """Faz classificação dos períodos seco e chuvo e dos anos hidrológicos."""
    station.classify_season(start_wet, start_dry)
    station.classify_hydroyears(start_wet)


def calc_baseflow(station, k):
    """Faz o cálculo do fluxo de base e etapas intermediárias."""
    station.calc_k_a_baseflow(k)


def create_chart_sf(df_ts, col_datetime, col_streamflow, col_baseflow, name, range_x):
    """Cria o gráfico para plotar."""
    fig_sf = Fig2D()
    dates = df_ts[col_datetime]
    streamflows = df_ts[col_streamflow]
    baseflows = df_ts[col_baseflow]
    fig_sf.load_traces_sf(dates, streamflows, baseflows)
    fig_sf.create_fig()
    fig_sf.update_layout_sf(title=name, range_x=range_x)
    return fig_sf


def create_chart_plu(df_ts, col_datetime, col_rainfall, name, range_x):
    """Cria o gráfico para plotar."""
    fig_plu = Fig2D()
    dates = df_ts[col_datetime]
    rainfalls = df_ts[col_rainfall]
    fig_plu.load_traces_plu(dates, rainfalls)
    fig_plu.create_fig()
    fig_plu.update_layout_plu(title=name, range_x=range_x)
    return fig_plu
