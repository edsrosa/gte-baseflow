from tools.database import Station
from tools.viewer import Fig2D


def create_station(data, name_station, area_bacia):
    """Cria a Station e faz alguns tratamentos"""
    col_datetime = data['cols_in']['datetime'][1]
    col_streamflow = data['cols_in']['streamflow'][1]
    station = Station()
    station.load_df(data['df'], col_datetime, col_streamflow)
    station.name=name_station
    station.area_km2=area_bacia
    return station

def classify_season_hydroyears(station, start_wet, start_dry):
    """Faz classificação dos períodos seco e chuvo e dos anos hidrológicos."""
    station.classify_season(start_wet, start_dry)
    station.classify_hydroyears(start_wet)

def calc_baseflow(station, k):
    """Faz o cálculo do fluxo de base e etapas intermediárias."""
    station.calc_k_a_baseflow(k)

def create_chart_sf(df_ts, col_datetime, col_streamflow, col_baseflow, name):
    """Cria o gráfico para plotar."""
    fig_sf = Fig2D()
    dates = df_ts[col_datetime]
    streamflows = df_ts[col_streamflow]
    baseflows = df_ts[col_baseflow]
    fig_sf.load_traces(dates, streamflows, baseflows)
    fig_sf.create_fig()
    fig_sf.update_layout(title=name)
    return fig_sf
