# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import pandas as pd


# %%
file = 'covid_19_clean_complete.csv'
df = pd.read_csv(file, sep=',', parse_dates=['Date'])


# %%
import warnings
warnings.filterwarnings('ignore')


# %%
df.head(10)


# %%
df.info()


# %%
# Casos ativos = Casos Confirmados - Mortes - Casos Recoperados
df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']


# %%
# Subistituindo Mainland China por China
df['Country/Region'] = df['Country/Region'].replace('Mainland China', 'China')


# %%
# Preenchendo missing values 
df[['Province/State']] = df[['Province/State']].fillna('')
df[['Confirmed', 'Deaths', 'Recovered', 'Active']] = df[['Confirmed', 'Deaths', 'Recovered', 'Active']].fillna(0)


# %%
# Convertendo datatypes
df['Recovered'] = df['Recovered'].astype(int)


# %%
# imprimindo 5 primeiras linhas
df.head()

# %% [markdown]
# **Examinando os dados temporais**

# %%
df.Date.describe()

# %% [markdown]
# **Agrupando dados**

# %%
# Obtem o numero de casos confirmados, mortes, recuperados e ativos agrupado por data e por região.
df_agrupado = df.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()


# %%
# Ordena o dataframe por mais casos confirmados
df_agrupado.sort_values(by='Confirmed', ascending=False)


# %%
# Obtem o numero de casos confirmados, mortes, recuperados e ativos agrupando por região.
df_group_paises = df.groupby('Country/Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum().reset_index()


# %%
# ordena por paises com mais casos confirmados
df_group_paises.sort_values(by='Confirmed', ascending=False)


# %%
# Agrupa quantidade de casos recuperados, mortes e ativos por data
temp = df.groupby('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()


# %%
# Remodela o dataframe com variável e valor para ter quantidades de recuperados, mortos e ativos
temp = temp.melt(id_vars="Date", value_vars=['Recovered', 'Deaths', 'Active'],
                 var_name='Case', value_name='Count')


# %%
temp.head(20)


# %%
# habilita modo offline
from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)


# %%
# Definindo o renderizador:
import plotly.io as pio
pio.renderers
pio.renderers.default = "colab"


# %%
# Cores
recuperados = '#21bf73'
mortes = '#ff2e63'
ativos = '#fe9801'


# %%
import plotly.express as px
fig = px.area(temp, 
              x="Date", 
              y="Count", 
              color='Case', 
              height=600,
              title='Casos ao longo do tempo',
              color_discrete_sequence = [recuperados, mortes, ativos])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()

# %% [markdown]
# Casos ao longo do tempo

# %%
import numpy as np


# %%
# Mapa de Choropleth é um mapa composto por polígonos coloridos. 
# É usado para representar variações espaciais de uma quantidade
fig = px.choropleth(df_agrupado,                                                   # casos agrupados por país
                    locations="Country/Region",                                    # definindo as regiões no mapa
                    locationmode='country names',                                  # define o modo de localização para todas regiões
                    color=np.log(df_agrupado["Confirmed"]),                        # define a cor pelo o valor de casos confirmados (aplica o log)
                    hover_name='Country/Region',                                   # define o texto interativo com o nome da região
                    hover_data=["Confirmed", "Deaths"],                            # define o texto interativo com o numero de casos confirmasos e mortes
                    animation_frame=df_agrupado["Date"].dt.strftime('%d-%m-%Y'),   # define o animate_frame com as datas
                    title='Casos ao longo do tempo',                               # define título
                    color_continuous_scale=px.colors.sequential.Magenta)           # define a paleta de cores
fig.update_layout(autosize=False, width=1200, height=800)                          # define tamanho da figura
fig.show()

# %% [markdown]
# Mortes ao longo do tempo

# %%
# Mapa de Choropleth é um mapa composto por polígonos coloridos. 
# É usado para representar variações espaciais de uma quantidade
fig = px.choropleth(df_agrupado,                                                   # casos agrupados por país
                    locations="Country/Region",                                    # definindo as regiões no mapa
                    locationmode='country names',                                  # define o modo de localização para todas regiões
                    color=np.log(df_agrupado["Deaths"]),                        # define a cor pelo o valor de casos confirmados (aplica o log)
                    hover_name='Country/Region',                                   # define o texto interativo com o nome da região
                    hover_data=["Confirmed", "Deaths"],                            # define o texto interativo com o numero de casos confirmasos e mortes
                    animation_frame=df_agrupado["Date"].dt.strftime('%d-%m-%Y'),   # define o animate_frame com as datas
                    title='Mortes ao longo do tempo',                               # define título
                    color_continuous_scale=px.colors.sequential.Magenta)           # define a paleta de cores
fig.update_layout(autosize=False, width=1200, height=800)
fig.show()

# %% [markdown]
# Painel

# %%
get_ipython().system('pip install plotly==4.5.2')


# %%
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.express as px


# %%
# filtra os dados considerando o último dia da base de dados
completo = df[df['Date'] == max(df['Date'])]


# %%
# imprime as 5 primeiras linhas
completo.head()


# %%
# Plota painel                        
fig = px.treemap(completo.sort_values(by='Confirmed', ascending=False).reset_index(drop=True), 
                 path=["Country/Region", "Province/State"],
                 values="Confirmed",
                 height=600,
                 title='Número de Casos Confirmados',
                 color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
fig.show()
# Plota Painel
fig = px.treemap(completo.sort_values(by='Deaths', ascending=False).reset_index(drop=True), 
                 path=["Country/Region", "Province/State"],
                 values="Deaths",
                 height=600,
                 title='Número de Mortes Confirmadas',
                 color_discrete_sequence = px.colors.qualitative.Dark2)
fig.data[0].textinfo = 'label+text+value'
fig.show()

# %% [markdown]
# Picos de casos confirmados e mortes

# %%
fig = px.line(df_agrupado,
              x="Date",
              y="Confirmed",
              color='Country/Region',
              height=600,
              title='Casos Confirmados',
              color_discrete_sequence = px.colors.qualitative.Dark2 )
fig.show()

fig = px.line(df_agrupado,
              x="Date",
              y="Deaths",
              color='Country/Region',
              height=600,
              title='Mortes Confirmadas',
              color_discrete_sequence = px.colors.qualitative.Dark2)
fig.show()

# %% [markdown]
# Gráfico com Folium

# %%
# Obtem os dados do último dia da base de dados
temp = df[df['Date'] == max(df['Date'])]


# %%
import folium


# %%
m = folium.Map(location=[0, 0], tiles='cartodbpositron',
               min_zoom=1, max_zoom=4, zoom_start=1)

for i in range(0, len(temp)):
    folium.Circle(
        location=[temp.iloc[i]['Lat'], temp.iloc[i]['Long']],
        color='crimson', fill='crimson',
        tooltip =   '<li><bold>Country : '+str(temp.iloc[i]['Country/Region'])+
                    '<li><bold>Province : '+str(temp.iloc[i]['Province/State'])+
                    '<li><bold>Confirmed : '+str(temp.iloc[i]['Confirmed'])+
                    '<li><bold>Deaths : '+str(temp.iloc[i]['Deaths']),
        radius=int(temp.iloc[i]['Confirmed'])**1.1).add_to(m)
m

