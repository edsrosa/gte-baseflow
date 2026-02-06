import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class Fig2D():
    def __init__(self):
        """Fig base 2D."""
        self.type_ch=None  # tipo do gráfico
        self.title='' # Título do gráfico
        self.x=None
        self.y=None
        self.color=None
        self.limits_xy={'x':[], 'y':[]}
        self.frame=None
        self.layout=self.layout_base()
        self.traces=[]
        self.fig=None


    def layout_base(self):
        """Cria um mapa base onde os elementos serão plotados."""
        layout = dict(margin=dict(t=40, b=10, l=10, r=10),
            plot_bgcolor='#ffffff',
            xaxis=dict(color='#4d4d4d', separatethousands=True, linecolor='#4d4d4d', mirror=True, gridcolor='#808080'), 
            yaxis=dict(color='#4d4d4d', separatethousands=True, linecolor='#4d4d4d', mirror=True, gridcolor='#808080', rangemode='nonnegative'),
            )
        return layout


    def load_traces_sf(self, dates, streamflows, baseflows):
        """Carrega os traces para plotagem."""
        streamflow_trace = go.Scatter(x=dates, y=streamflows, name='Fluxo Total', mode='lines', marker_color="#6583e9")
        baseflow_trace = go.Scatter(x=dates, y=baseflows, name='Fluxo de Base', mode='lines', marker_color="#df5151")
        self.traces = [streamflow_trace, baseflow_trace]


    def load_traces_plu(self, dates, rainfalls):
        """Carrega os traces para plotagem."""
        rainfall_trace = go.Bar(x=dates, y=rainfalls, name='Precipitação', marker_color="#1A88D1")
        self.traces = [rainfall_trace]


    def load_traces_wb(self, yearhydros, streamflows, baseflows, rainfalls):
        """Carrega os traces para plotagem."""
        streamflows_trace = go.Scatter(x=yearhydros, y=streamflows, name='Fluxo Total', mode='lines', marker_color="#6583e9")
        baseflow_trace = go.Scatter(x=yearhydros, y=baseflows, name='Fluxo de Base', mode='lines', marker_color="#df5151")
        self.traces = [baseflow_trace, streamflows_trace,]
        if rainfalls is not None:
            rainfalls_trace = go.Scatter(x=yearhydros, y=rainfalls, name='Precipitação', mode='lines', marker_color="#6ee965")
            self.traces.append(rainfalls_trace)


    def create_fig(self):
        """Gera a figura."""
        fig = go.Figure(layout=self.layout)
        if self.traces != []:
            for trace in self.traces:
                fig.add_trace(trace)
        self.fig = fig


    def update_layout(self, title):
        """Atualizações no layout da figura caso haja dados."""
        layout_title = dict(title=dict(text=title, xref='paper', xanchor='center', x=0.5, yanchor='bottom', y=0.87,)
                            )
        self.fig.update_layout(layout_title)
        self.fig.update_xaxes(
            rangeslider=dict(visible=True),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 mês", step="month", stepmode="backward"),
                    dict(count=6, label="6 meses", step="month", stepmode="backward"),
                    dict(count=1, label="1 ano", step="year", stepmode="backward"),
                    dict(label="Todo o Período",step="all")
                ]),
                y=1.2, yanchor='bottom'
            )
        )
        self.fig.update_yaxes(title='Vazão (m³/s)')


    def update_layout_sf(self, title, range_x):
        """Atualizações no layout da figura caso haja dados."""
        layout_title = dict(title=dict(text=title, xref='paper', xanchor='center', x=0.5)
                            )
        self.fig.update_layout(layout_title, 
                               legend=dict(orientation='h',
                                           xanchor='center',
                                           x=0.5
                                            ),
                                height=350,
                                )
        self.fig.update_xaxes(range=range_x)
        self.fig.update_yaxes(title='Vazão (m³/s)')
        

    def update_layout_plu(self, title, range_x):
        """Atualizações no layout da figura caso haja dados."""
        layout_title = dict(title=dict(text=title, xref='paper', xanchor='center', x=0.5)
                            )
        self.fig.update_layout(layout_title, height=250)
        self.fig.update_xaxes(range=range_x)
        self.fig.update_yaxes(title='Precipitação (mm)')


    def update_layout_wb(self, title):
        """Atualizações no layout da figura caso haja dados."""
        layout_title = dict(title=dict(text=title, xref='paper', xanchor='center', x=0.5)
                            )
        self.fig.update_layout(layout_title, 
                               legend=dict(orientation='h',
                                           xanchor='center',
                                           x=0.5,
                                           y=-0.3
                                            ),
                                height=500,
                                )
        self.fig.update_yaxes(title='Volume (m³)')

    def plot_wet_dry(self, year_min, year_max, start_wet, start_dry):
        """Plota sazonalidade no gráfico."""
        for year in range(year_min, year_max):
            date_i = pd.to_datetime(f"{year}-{start_wet}-01")
            date_f = pd.to_datetime(f"{year+1}-{start_dry}-01") - pd.Timedelta(1, unit="D")
            self.fig.add_vrect(x0=date_i, x1=date_f, fillcolor="green", opacity=0.2)
