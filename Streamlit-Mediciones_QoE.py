import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import glob
import os
from urllib.request import urlopen
import json
from streamlit_folium import folium_static
from st_aggrid import AgGrid
import geopandas as gpd
import folium
import urllib
def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

LogoComision="data:image/png;base64,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"
LogoComision2="https://postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

   

st.title("Mediciones de calidad desde la experiencia del usuario")

#################################Lectura de bases Internet fijo#######################################33
pathFijo='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Fijo/'

####Primera sección - Fijo
Colombia1Fijo=pd.read_csv(pathFijo+"Fij-historical_comparison_month(Colombia).csv", delimiter=',')
FeAntig1Fijo=Colombia1Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre1Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction1Fijo=dict(zip(FeAntig1Fijo, FeCorre1Fijo))
Colombia1Fijo['Aggregate Date'].replace(diction1Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Colombia1Fijo['Aggregate Date'] =pd.to_datetime(Colombia1Fijo['Aggregate Date']).dt.floor('d') 
Colombia1Fijo['month']=pd.DatetimeIndex(Colombia1Fijo['Aggregate Date']).month#Guardar el mes
Colombia1Fijo['year']=pd.DatetimeIndex(Colombia1Fijo['Aggregate Date']).year
Colombia1Fijo = Colombia1Fijo.drop(['Location','Platform','Technology Type','Metric Type','Provider'],axis=1)

####Segunda sección - Fijo
df2_1Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2018-12-01.csv',delimiter=';')
df2_2Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2019-12-01.csv',delimiter=';')
df2_3Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2020-12-01.csv',delimiter=';')
df2_4Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2022-01-01.csv',delimiter=';')
df2_5Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2018-12-01.csv',delimiter=';')
df2_6Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2019-12-01.csv',delimiter=';')
df2_7Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2020-12-01.csv',delimiter=';')
df2_8Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2022-01-01.csv',delimiter=';').dropna(how='all') 

OpCiud2Fijo=pd.concat([df2_1Fijo,df2_2Fijo,df2_3Fijo,df2_4Fijo,df2_5Fijo,df2_6Fijo,df2_7Fijo,df2_8Fijo])
OpCiud2Fijo['Location']=OpCiud2Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntig2Fijo=OpCiud2Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre2Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction2Fijo=dict(zip(FeAntig2Fijo, FeCorre2Fijo))
OpCiud2Fijo['Aggregate Date'].replace(diction2Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
OpCiud2Fijo['Aggregate Date'] =pd.to_datetime(OpCiud2Fijo['Aggregate Date']).dt.floor('d') 
OpCiud2Fijo['month']=pd.DatetimeIndex(OpCiud2Fijo['Aggregate Date']).month
OpCiud2Fijo['year']=pd.DatetimeIndex(OpCiud2Fijo['Aggregate Date']).year
OpCiud2Fijo= OpCiud2Fijo.drop(['Device','Platform','Technology Type','Metric Type'],axis=1)
OpCiud2Fijo['Location'] = OpCiud2Fijo['Location'].str.upper()
OpCiud2Fijo['Location'] = OpCiud2Fijo['Location'].replace({'SANTANDER DEPARTMENT':'SANTANDER','CAUCA DEPARTMENT':'CAUCA','SAN ANDRÉS AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA','NORTH SANTANDER':'NORTE DE SANTANDER','CAQUETÁ':'CAQUETA'})
gdf2 = gpd.read_file('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Colombia.geo.json')
with urllib.request.urlopen('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Colombia.geo.json') as url:
    Colombian_DPTO2 = json.loads(url.read().decode())
geoJSON_states2 = list(gdf2.NOMBRE_DPT.values)
denominations_json2 = []
Id_json2 = []
for index in range(len(Colombian_DPTO2['features'])):
    denominations_json2.append(Colombian_DPTO2['features'][index]['properties']['NOMBRE_DPT'])
    Id_json2.append(Colombian_DPTO2['features'][index]['properties']['DPTO'])
denominations_json2=sorted(denominations_json2)
dataframe_names2=sorted(OpCiud2Fijo.Location.unique().tolist())
Opciud2Fijo=OpCiud2Fijo.replace(dict(zip(dataframe_names2, denominations_json2)), inplace=True)
OpCiud2Fijo=OpCiud2Fijo[OpCiud2Fijo['Test Count']>30]
gdf2=gdf2.rename(columns={"NOMBRE_DPT":'Location'})

####Tercera sección - Fijo
df3_1Fijo=pd.read_csv(pathFijo+'Fij(1-10)historical_comparison_month_2018-12-01.csv',delimiter=';')
df3_2Fijo=pd.read_csv(pathFijo+'Fij(1-10)historical_comparison_month_2019-12-01.csv',delimiter=';')
df3_3Fijo=pd.read_csv(pathFijo+'Fij(1-10)historical_comparison_month_2020-12-01.csv',delimiter=';')
df3_4Fijo=pd.read_csv(pathFijo+'Fij(1-10)historical_comparison_month_2021-06-01.csv',delimiter=';')
df3_5Fijo=pd.read_csv(pathFijo+'Fij(1-10)historical_comparison_month_2022-01-01.csv',delimiter=';')
df3_6Fijo=pd.read_csv(pathFijo+'Fij(11-17)historical_comparison_month_2018-12-01.csv',delimiter=';')
df3_7Fijo=pd.read_csv(pathFijo+'Fij(11-17)historical_comparison_month_2019-12-01.csv',delimiter=';')
df3_8Fijo=pd.read_csv(pathFijo+'Fij(11-17)historical_comparison_month_2020-12-01.csv',delimiter=';')
df3_9Fijo=pd.read_csv(pathFijo+'Fij(11-17)historical_comparison_month_2021-06-01.csv',delimiter=';')
df3_10Fijo=pd.read_csv(pathFijo+'Fij(11-17)historical_comparison_month_2022-01-01.csv',delimiter=';')
from functools import reduce
Ciudades3Fijo=reduce(lambda x,y: pd.merge(x,y,how='outer'), [df3_1Fijo,df3_2Fijo,df3_3Fijo,df3_4Fijo,df3_5Fijo,df3_6Fijo,df3_7Fijo,df3_8Fijo,df3_9Fijo,df3_10Fijo])#Unir los dataframes
Ciudades3Fijo['Aggregate Date']=Ciudades3Fijo['Aggregate Date'].str.replace(" ", "-").str.title() #Unir espacios blancos 
Ciudades3Fijo['Location']=Ciudades3Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntig3Fijo=Ciudades3Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre3Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction3Fijo=dict(zip(FeAntig3Fijo, FeCorre3Fijo))
Ciudades3Fijo['Aggregate Date'].replace(diction3Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Ciudades3Fijo['Aggregate Date'] = Ciudades3Fijo['Aggregate Date'].astype('datetime64[D]') 
Ciudades3Fijo['year']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).year
Ciudades3Fijo['month']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).month
Ciudades3Fijo=Ciudades3Fijo.drop(['Device','Platform','Technology Type','Metric Type','Provider'], axis=1)


####Cuarta sección - Fijo
df4_1Fijo=pd.read_csv(pathFijo+'Fij-historical_comparison_month_2018-12-01OP.csv',delimiter=';')
cols_to_changeFijo=['Download Speed Mbps']
if df4_1Fijo['Download Speed Mbps'].dtypes !='float64':
    for col in cols_to_changeFijo:
        df4_1Fijo[col]=df4_1Fijo[col].str.replace(',','.')
        df4_1Fijo[col]=df4_1Fijo[col].astype(float)
df4_2Fijo=pd.read_csv(pathFijo+'Fij-historical_comparison_month_2019-12-01OP.csv',delimiter=';')
df4_3Fijo=pd.read_csv(pathFijo+'Fij-historical_comparison_month_2020-12-01OP.csv',delimiter=';')
df4_4Fijo=pd.read_csv(pathFijo+'Fij-historical_comparison_month_2021-06-01OP.csv',delimiter=';')
df4_5Fijo=pd.read_csv(pathFijo+'Fij-historical_comparison_month_2022-01-01OP.csv',delimiter=';').dropna(how='all')

Operadores4Fijo=pd.concat([df4_1Fijo,df4_2Fijo,df4_3Fijo,df4_4Fijo,df4_5Fijo])
FeAntig4Fijo=Operadores4Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre4Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction4Fijo=dict(zip(FeAntig4Fijo, FeCorre4Fijo))
Operadores4Fijo['Aggregate Date'].replace(diction4Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Operadores4Fijo['Aggregate Date'] =pd.to_datetime(Operadores4Fijo['Aggregate Date']).dt.floor('d') 
Operadores4Fijo['month']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).month
Operadores4Fijo['year']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).year
Operadores4Fijo=Operadores4Fijo.drop(['Location','Device','Platform','Technology Type','Metric Type'],axis=1)


st.sidebar.markdown("""<b>Seleccione el servicio</b>""", unsafe_allow_html=True)

select_servicio = st.sidebar.selectbox('Servicio',
                                    ['Internet fijo','Internet móvil','Comparación internacional'])

if select_servicio == 'Internet fijo':
    select_indicador=st.selectbox('Indicador de desempeño',['Velocidad de descarga','Velocidad de carga','Latencia'])
    
    if select_indicador== 'Velocidad de descarga':
        dimension_Vel_descarga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia', 'Operadores', 'Ciudades'),horizontal=True)
        if dimension_Vel_descarga_Fijo == 'Histórico Colombia':
            Downspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Download Speed Mbps'].mean().round(2).reset_index()
            Downspeed1Fijo=Downspeed1Fijo[Downspeed1Fijo['Aggregate Date']<'2022-01-01']
            fig1Fijo = make_subplots(rows=1, cols=1)
            fig1Fijo.add_trace(go.Scatter(x=Downspeed1Fijo['Aggregate Date'].values, y=Downspeed1Fijo['Download Speed Mbps'].values,
                                     line=dict(color='blue', width=2),name=' ',mode='lines+markers',fill='tonexty', fillcolor='rgba(0,0,255,0.2)'),row=1, col=1)
            fig1Fijo.add_shape(type="line",
                x0='2018-06-01', y0=0, x1='2018-06-01', y1=12.99,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2018-12-01', y0=0, x1='2018-12-01', y1=15.99,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2019-06-01', y0=0, x1='2019-06-01', y1=19.34,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2019-12-01', y0=0, x1='2019-12-01', y1=28.32,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2020-06-01', y0=0, x1='2020-06-01', y1=33.35,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2020-12-01', y0=0, x1='2020-12-01', y1=44.81,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2021-06-01', y0=0, x1='2021-06-01', y1=61.62,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_shape(type="line",
                x0='2021-12-01', y0=0, x1='2021-12-01', y1=84.82,
                line=dict(color="RoyalBlue",width=2,dash="dot"))
            fig1Fijo.add_trace(go.Scatter(name=' ',
                x=['2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01'],
                y=[15.9, 18.5, 24,31.4,38,47.8,68,87.5],
                text=["12,99",
                      "15,99",
                      "19,3","28,32","33,35","44,81","61,62","84,82"],
                mode="text"))
            fig1Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01'])
            fig1Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig1Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad descarga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig1Fijo.update_traces(textfont_size=18)
            fig1Fijo.update_layout(height=500,legend_title=None)
            #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            fig1Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            fig1Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Gráfico 1. Velocidad promedio mensual de descarga de internet fijo en <br>Colombia (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            st.plotly_chart(fig1Fijo, use_container_width=True)  
            st.download_button(label="Descargar CSV",data=convert_df(Downspeed1Fijo),file_name='Historico_descarga_Colombia.csv',mime='text/csv')


            ##
            Colombia2Fijo=pd.read_csv(pathFijo+'FijAllproviders21.csv',delimiter=';')
            Colombia2Fijo['Location']=Colombia2Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
            FeAntigFijo=Colombia2Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
            FeCorreFijo=pd.date_range('2020-06-01','2022-01-01', 
                          freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
            dictionFijo=dict(zip(FeAntigFijo, FeCorreFijo))
            Colombia2Fijo['Aggregate Date'].replace(dictionFijo, inplace=True) #Reemplazar fechas antiguas por nuevas
            Colombia2Fijo['Aggregate Date'] =pd.to_datetime(Colombia2Fijo['Aggregate Date']).dt.floor('d') 
            Colombia2Fijo['month']=pd.DatetimeIndex(Colombia2Fijo['Aggregate Date']).month
            Colombia2Fijo['year']=pd.DatetimeIndex(Colombia2Fijo['Aggregate Date']).year
            Colombia2Fijo = Colombia2Fijo.drop(['Device','Platform','Technology Type','Metric Type'],axis=1)
            Colombia2Fijo['Location'] = Colombia2Fijo['Location'].str.upper()
            Colombia2Fijo['Location'] = Colombia2Fijo['Location'].replace({'SANTANDER DEPARTMENT':'SANTANDER','CAUCA DEPARTMENT':'CAUCA','SAN ANDRÉS AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA','NORTH SANTANDER':'NORTE DE SANTANDER','CAQUETÁ':'CAQUETA'})
            Colombia2Fijo=Colombia2Fijo[Colombia2Fijo['Test Count']>30]
            Col2Fijo=Colombia2Fijo[(Colombia2Fijo['year']==2021)&(Colombia2Fijo['month']==12)].groupby(['Location'])['Download Speed Mbps'].mean()
            Col2Fijo=round(Col2Fijo,2)
            departamentos_df2Fijo=gdf2.merge(Col2Fijo, on='Location')
            departamentos_df2Fijo=departamentos_df2Fijo.sort_values(by='Download Speed Mbps')

            # create a plain world map
            colombia_map1Fijo = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
            tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
            for tile in tiles:
                folium.TileLayer(tile).add_to(colombia_map1Fijo)
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=departamentos_df2Fijo,
                bins=[0,5,15,25,50,75,100],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(colombia_map1Fijo)
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
            folium.LayerControl().add_to(colombia_map1Fijo)

            #Adicionar valores velocidad
            style_function = lambda x: {'fillColor': '#ffffff', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.1, 
                                        'weight': 0.1}
            highlight_function = lambda x: {'fillColor': '#000000', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.50, 
                                            'weight': 0.1}
            NIL = folium.features.GeoJson(
                data = departamentos_df2Fijo,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Download Speed Mbps'],
                    aliases=['Departamento','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            colombia_map1Fijo.add_child(NIL)
            colombia_map1Fijo.keep_in_front(NIL)
            col1, col2 ,col3= st.columns([1.5,4,1])
            with col2:
                folium_static(colombia_map1Fijo,width=480) 
        