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
from folium.plugins import FloatImage
import urllib
from functools import partial, reduce

def convert_df(df):
     return df.to_csv(index=False).encode('utf-8')
def Excluir_ciudades(anno,annos_excluir,municipio,municipios_excluir):
    return (anno.isin(annos_excluir)) & (municipio.isin(municipios_excluir))

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

LogoComision="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAkFBMVEX/////K2b/AFf/J2T/AFb/ImL/IGH/G1//Fl3/BVn/EVv//f7/mK//9/n/1+D/7fH/PXH/w9D/0tz/aY3/tsb/qr3/4uj/iKP/6u//y9b/RHX/5ev/ssP/8/b/dZX/NWz/UX3/hqL/XYX/obb/fJv/u8r/VH//XIT/gJ3/lKz/Snn/l6//ZYr/bpH/dpb/AEtCvlPnAAAR2UlEQVR4nO1d2XrqPK9eiXEcO8xjoUxlLHzQff93tzFQCrFsy0po1/qfvkc9KIkVy5ol//nzi1/84he/+MXfgUZ/2Bovd7vBBbvqsttqv05+elll4GXYGxxmSkqlUiFEcsHpr1QpqdLmcTdu/7OEvqx3WxGrNOEssoHxE6mVqLMc/mtkvo6nkVSCW0nL06lk8239r1CZDQeRTBP7xlnITJQcVes/vXovauujUsHU3agUkr0Pf5oGF4Yn8pCc6dhKPvhLd/J1J4qS90mknC3/vjPZ2saCypwAkamc/lUbmfWicrbvDoncr3+ark/Udiotb/u+wFQ0/mnaNGoDJZ5A3pVG1vtp+rLq8+g705hG3R8lcCzQ9J0Ml7MxerLj+BknY1Vbq4nvd6r5cxpy2FSI86dtT1nh8+Outx7WXye1WnZGrdbot1u9dx+JEZOL1x+hb9KRXvq0wck6u3W9Zn3MUPk/Eo9330jYJ3rS8/FPJli6rQ4bnucsUXwuou9m1de589OfbK/KZlnPEE9aebn08sR4aueDJ2AZOxT8iTzx0cKuZ49VpUnyfds42Tg2kCsR4h5kuC28bOP782h6QCu1biATlUMLw5s3vEg0hafTOOs/i6h7vMU2vjqZWcE+AUaU3m/j8+24yT61vJ3LTSv8eb1Akyj+KJ+mB9RtsRde6ZDcHaQo/YIYPdV1HFdgDuXySDwh82CvhKdP9BwHMfhOFh/IEiDoGF5fV3ma43gEl8PUiP5Rg0TpDfGyRKq+kM1BoSBYEfcmTJTeIN9KI+sLtREkE1jlLUj95TG2SWYP1LQsum6ozSAhmjaDGLRRX/d279PtfnbGaPOBttmMNx9KJrABEcjkf9jfv7SW070652cSzm5wpDR8EItSCZxEAIFYG6q97OgkBjkS/h0kgiwqV4hf9pcLnaF5RiguEuUxatY0CWTKr5Tag0hi808UpKWJm7kpRZPZi+dH9QGTZTNmHqokpXEw9aDquH9S6zVliUF+K2S1DALfTZXlCQz1358TBAdQhgHXM+wqVnFaMe2FL0ZVJuLCZviwYhAoXUGK9lw+UbaYYKkvmOeBaRkzl/NS31oDAM8CbxajsJlfMEvs8efG8Xv37wJRSGdM82KUJXYtUY29OQienJMX6lxd4ypDCYEskJ8a53nUsYPtmctNYEmqYjE6rKrLcWs4HLa6vepqMYsJRRsAiWT/+zUvZew7mK3sB5CnUm0G3TogErJ6d9CU9OKN67JmVArzh5BZP1Y7soTMdPy703NL9EnrPSpmHwhiAG6QZzvZtvznzrKBiYwGbZSHXN9FRaSUJMQxTy/N82hsecwEztKwNH23fRIIwyN9I5mgpG1muddJS/inDboPXI66ofGNSZVTrb3EYyhDGOROVmpxB8EQKo+3Idt3QzZmRBrD+bSfC40mG/j/3oBwIJNburU45qTgFGOhHJMLETEGM3oHOIIFSwuyqqJY7mIQ9ppxbuUVcFOyjakkeBET44JGh2LdVoL0fpY7DfCqs735seWhjMTJ0KZfHeCWcwQjJ2ZgSZU1DQKZLCm/57KRbAgRNjmfiXHoFGdmEFw0fdEbPByZZgtCjLfj49pjUPKbLIqKL6Ix2YQKVYWWAP1Ha0aAEa2FcVIqZVfZWZJ5VrAE++TDA3/Am/+R/8Du4AYNa0tC1oYUmXWrP346AQmP/wzPUfiFdaM93k0XoxkXfDZaTHfjti/GUg+zVJnAUdjJHXFlxg7XhucYeYrr+r3jTF7zMvr/tbufKjk79pxf5gVKmNiRog5K3l7TObTcKvrGDjLnbgzfmUzBmAU7uccnD8v+05qpkhxgDEMhUB3BKg+x5SzKu8bCQWB/kLideHZyI6vWBwBKyQGFSEhPjACpRjq628ZO7p1M2TmttcFkL5iQR5uxXhsFMCpDxBarsL3EvqoDjCi4Pe7cavprUK/g8cLyGDj9bAFCojPbktT+IkyMQ2jNHdT3aPrONFaOMK9O8qfC9RBvUrFlL45gFy8/H58CRO0ZBNMyseSSXgO+lPQZjlsXR+htzMenbPGDIacU8Rti+4I2KBxACE/C7cVtKHH1X26P2Qz2rd8CzZHb8+BqIDMDZn1A5KbQIme+kBfdsN9pr2D0Qy2gb2bkF6zwyJqAM31ZDmhE1IM9n3skoH1k5IisP3eGh+uBZWYJWPHRChKhJpgCjJxXtKMhXTGpfAjRBwWFLLp4sWABg4LPPWwJnHL5+oFMKiFN2CtMYATr2A2S9fnRTmAgk3KIRw23g4aKuRHoSk1hZ1OvJH2EBEyQYaBfbgUQOlkiBbSyS9NREJMKQHP1CwqZLzBlStR8KsWCxFpI1Aj7/qn5BMOvKgAWGcw2xPGpPei2DlPTbGY4A9syK2kS04he4IRNbAs4hHYG5Bzj00Gh1TTboIxjUMdxWWqLS1sdJ/saNvfCpl+OGP1CbJiE+RgSjMRSgPJKqJvn90WYaMMKC9NjN4NI4O8sgdPAY3jFV5sOnkfPFdCY/zNTXriTKOGDOKCJCRFdljHBsABLUllJRvP5PqpI5YmGpkAaBCdOUzjsQK2bvwqcqf8DJZKtuv1PJfDS2rmqUFkMqjXUUUjAdGlGd+l0SsYvZoT8MOyU/s5WnMBT2IDuYZbJwFyiEWHCQxfaHD0HhMcDMHea9cCefjW3ZFonKFkD5gNpgkaD7f1CTh7sMd+BEbJisT3acsDIGlDU7MjjH7TGcFsLTDpj0fVccCRhjjg/aidAHxGnTKHliz9/ak4W5768Tba4X7Y8uCqc3K+6AvIK6PpaCy7n+U/2/pqs1U2ZMl8xB0YlJlDbN1nQ6KC+y+9K9phinvcrif5eI4w0ZVvzd7Rex+jiq7jkMJvhquo6Zzkg/YWUGKEPRU3bVL9AFyO5hltYLCgTp2PCEb1GOA8hNn9GVhY69Ocwh9xS9B6vMh2hqlUwMhFwEVG2AoQ0+9Ow840/F/SFJXIqBGYcijJTdVR1yLfOhBUUrSoKTPMwoBCDW/+v0Lkeu1cCVgy2dtPOavncBnDAzacqfB26s48NkKZ1uVNKcJ4IOSN3ZSFMU0Dlhw83uNLw4lCliVEH1o9u553FB2IfOMI4EWbelmrSKFfSROZZsf0QT02atLlBCH4DYqbIaGsebOQ4+YbebeQCxsmcROEbwtk2qwiJgoZPHWMDjA9p5NDx5YT3QGQfuBluIyoLbXZbFU0+XNI2e/0SylFE6O7yKBSnTbAOlcsbbEAoB2Wm5YGYNVEehVrvTG0HX+beAVRHuXPSFnS/lcK13WHLCxqo0ENLqmA4bKjyKdQK30rh/PEVdWhh/F+mMG91QylmXL0kgUIz1U3M/GkKbXVUPFcuBeUn4chmcQoBfUjU+NqGt5kYxuqBd8DRaQ8QkgYI1BBj+unJwf2waAsjdQQUs8CdDh4gtAXw5VCBVoDCnsOIUrl3mAYspuLVBGKMHeBb2DYC8SSrz224v2/5j18htTAgrDbAP0RYsxA0v1uPhVn2katLV5RT6DCi7ig0bSXcLFgDWiOAek7DrPWsNe9fQ20j8mWBokt8LAfiXDFtt8DF79ElZZNDNq18Lk+QOxURUhForCfOhotkzRHAhEqS251YpWkq0wE5SIXYjNj0ranpQ+3GW31uuCS5Nuz21gXmymBSiEB/UI1YKqIVovUM+0qSaUBsBnA+yGabFqb2mkb1jJmxiPA8WIG5JQZqtM62yuGwTZwuUR4/IngNHg+EkgGh1bpdfKfowYMnGRSnHNNBiDC/UihbQk1c6Ic5+CZgeMzJMGep8KsQRO7JCGNqUNNrmuUdmWe85bk6Mx9LfXdaYKrTFBSIRdU0QdC18Y4YrXCUXd+j96kDfDQifCfLZyV6iOdwmasYC2d8tu60FUu5g0ZEDskS30JYeyDOBe0uXSMRJLZyIwBS+x0zCLVm6ZYNHR7+RcGLp8pceUOGY3Pwne0eHUwBJihowhtmbtB5nsxZZyj2bht0Bb2aKQbRiGkosLXNkKsxdIOD+8XcZdzUZ7Y5WioyBxUhGgqs4S1n76ELmu0zj7JRe0tEpjF1dDCw/8tXHGA8BGsPItEJvlYd+/qSWAzdLFD/qLhEozmxAsOkUGfY5W3ksqiz7PLmWE8H6611l/bO2tWmexIoMMMLo9OATpAryIMMWVrTZqX//xI9RmGwHI97u4+R8o4vM08vpgo6H4m+A7Ue48pNKxSXn+dF6MGQ/s8JjA3CBD2t7RaoaLkNZwO7xJ6gy0MNHePpU7b97IYancJzlswY01cMQMEYxsUD/ftPkKtoT6yhJfSSXituQpixRpR3AFbPfmJdoHHpbCkdy7tJjwO50zfM4yuu8r+sQH/kZWhd0CQS5+O4WU7lqBC8+6GLScnZCw2e6E0MGtPhWic0LwXRtOKUpBrIHkbowfvLN2+UMx0YGvKHE2RAKd0DqAJf3jKSDVZ8Fxk4DBbVxJv4QgqBzc6fK7q/S6sxK3oWGVD/im3I9w6oQR3mPDh/ODS1fTGJysGJ0w0UgYjBe4RYRrrJ28fHInoxhdsz5qiFIaZ9mbVnPkBddEvi8Bb9ODipiOzfdA7FuCKsKd9WjF8nzOfU4OAkCnSPM2pOa6D5DQoFjXfCmFUmt7DVXEPqIO8MpTPC4qbgcIwz2qjLdO8hhK05A3cIrU3cOXTDNlEALUZX9ETIZOckHtgOEXbCELY/J1DrO0jMqmgahVxZ3bod8ps7nPtHBG6ii0R9sTxinDxLlSOrj/bJKui7n0MzGMJZfjc8SufcKCbk3DW/vYd1eAKqcVuhOlG4Wwxr66OQ4M1dTCi5WToFIJrAoA6k4PaSZO7TtPVlh1f0ANOEc8Z5ch5fKre7lscVwIcNgmaWI/XrPYmY5pBJfb0cvHcO88Xh463aHSKUFzTVHgZzDE8CEO4Jc2SraBgOeKEXWPaBapjOkRiVfo1to4k3/YJL4tHT0e7ewcubV35G0GS78Mu7CDXDjJd6bfZbiDAIvRrhD21gkPM+r9D325KK8JspJf9VQn1NeWPLB2EOZoV0JUqoo3ghkXRrTx6tQO9SIHukc6DMjTp9zSIXIF/Q3wbOtSNfaYUf/PpAYsELBF4+KqGhIvgGFQwOpLAg/pZgAK+r8PshzbluaBCHBNJvza53vPfvmQBm8wW8kRYVpN2anY1HlJvJWFTIXDTuB8SBcGt2e5XSLrMKuyPIxIpWdSq83tQjeQNBuuTphLiw7N4Qe2lGWN556U4F/QZEYtfNPTJiUSaPEB53v/velGmBRE4pd3M3iHe9eezw+niwkUUv6Uzc+V4sqKVScI7sEwU48+sNZXnd5q3HyAW47PASRoGypLThNy1qnYzDSKXOUrkjMEWHR/1YU2s04JsONJAjgV0ElupvkwetS9s17NSq8huBlkpnMsij1m013vQqwQuB5e7gmUQqo1osOGJX7ieB5YaELhhSr02HLbjQaxgegDInwhF4CdoXkiYQSaWVtVwfOCo9NHvBi3EHCxI8MiOp5KLyE9+D97SUgtqc2N8GhBmJndXRffnVM7AiyhvTvEH0Z8FPKv0iyRx65FuOclUkxIprnpIioyGoM+JhrDyaNzQKU9uI6DJRC8h4PeDRvKE0dLJKcX8XBWpJ14N5Q+j/T0T5V51a0G/SxER6V10UHFFnsvOMHKwNO5qBI77KDlGdE3dIwPbsJ6I/Ip3GZPYpKcLajk8b+A0iJoclKf7HkqvJHNQWkEalpLRC0ThSJM7tUjW8O5bEu6eZaR60R6HVh5rE63Vc2D1kcafk+oAgrGcEGi92F47HmZw/3YjxYGy7gsOBs+7HRJqZHH2bCnSgx4L3Uet+fxKdy9GPCBgA3WZoWuyk+33TYpJ4+zfs3yeGi0pYBEBsFs6brNN49YRITCG87rgK2UjXCJZENpffaaGh0epIYhbnHlyJ1U+LTzsm402lyD2yutf7+LdIFxsm3Y7wXcZl2Twho9XfTt4F2XC3j5UIufT9RJ1aFLhM4AdQG1YXqVRgcfcDbSwRSvLjsv1TpmchvLaqx2YilZ4vwO+FJ2N67sCJNMn2q+XwKQHs70PWaK+Xu+liP+Np5YxYRM35YbXrterf7/T94he/+MUvfvGL/0n8PxO8HWcj0wB/AAAAAElFTkSuQmCC"
LogoComision2="https://postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png"

st.set_page_config(
    page_title="Mediciones QoE", page_icon=LogoComision,layout="wide",initial_sidebar_state="expanded")  

st.markdown("""<style type="text/css">
    h1{ 
        background: linear-gradient(to bottom, #ffde00, #f0a30a);
        text-align: center;
        padding: 15px;
        font-family: sans-serif;
        font-size:1.60rem;
        color: black;
        width:100%;
        z-index:9999;
        top:0px;
        left:0;
    }
    .e8zbici0 {display:none}
    .e8zbici2 {display:none}
    .e16nr0p31 {display:none}
    .barra-superior{top: 0;
        position: fixed;
        background-color: #27348b;
        width: 100%;
        color:white;
        z-index: 999;
        height: 80px;
        left: 0px;
        text-align: center;
        padding: 0px;
        font-size: 36px;
        font-weight: 700;
    }
    .css-y3whyl, .css-xqnn38 {background-color:#ccc}
    .css-1uvyptr:hover,.css-1uvyptr {background: #ccc}
    .block-container {padding-top:0;}
    .css-k0sv6k {height:0rem}
    .e1tzin5v3 {text-align: center}
    h2{
        background: #fffdf7;
        text-align: center;
        padding: 50px;
        text-decoration: underline;
        text-decoration-style: double;
        color: #27348b;}
    h3{ 
        background: linear-gradient(to right, #27348b, #0c2340);
        text-align: center;
        padding: 15px;
        font-family: sans-serif;
        font-size:1.30rem;
        color: white;
        width:100%;
        z-index:9999;
        top:0px;
        left:0;
        }

    .imagen-flotar{float:left;}
    @media (max-width:1230px){
        .barra-superior{height:160px;} 
        .imagen-flotar{float:none}
        h1{top:160px;}
    }    
    </style>""", unsafe_allow_html=True)  

gdf2 = gpd.read_file('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Colombia.geo.json')
with urllib.request.urlopen('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Colombia.geo.json') as url:
    Colombian_DPTO2 = json.loads(url.read().decode())
Servidores=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Fijo/Fij-Servidores_Colombia.csv',encoding='latin-1',delimiter=';')
Servidores['latitude']=Servidores['latitude'].str.replace(',','.')
Servidores['longitude']=Servidores['longitude'].str.replace(',','.')
dict_serv_colores={'Cali':'rgb(255,128,0)', 'Bogotá D.C.':'rgb(255,0,0)', 'Cartagena':'rgb(128,255,0)',
        'Medellín':'rgb(0,255,0)', 'Barranquilla':'rgb(0,255,128)',
       'San Andrés':'rgb(255,255,0)', 'San Agustín, Huila':'rgb(0,255,255)', 'Choachí, Cundinamarca':'rgb(128,128,128)',
       'Pasto':'rgb(0,128,255)', 'Popayán':'rgb(0,0,255)', 'Rosas, Cauca':'rgb(127,0,255)', 'Guamal, Magdalena':'rgb(255,0,255)',
       'Plato, Magdalena':'rgb(255,0,127)', 'Valledupar':'rgb(153,0,0)', 'Santander de Quilichao, Cauca':'rgb(0,102,102)',
       'Colón, Nariño':'rgb(153,0,76)'}

st.markdown("# <center>Mediciones de calidad desde la experiencia del usuario</center>",unsafe_allow_html=True)

select_servicio = st.selectbox('Servicio',
                                    ['Información general','Internet fijo','Comparación internacional'])

if select_servicio=='Información general':
    st.markdown('<p style="text-align:justify;">La Comisión de regulación de comunicaciones presenta la aplicación interactiva que contiene información sobre la calidad de los servicios ofrecidos a través de redes móviles y fijas por los diferentes proveedores en el territorio nacional, para el periodo comprendido entre los años 2018 y 2023-1S. Los valores mostrados en este tablero corresponden a la mediana de las mediciones, debido a que ésta métrica presenta menor sensibilidad frente a valores atípicos de las distribuciones de datos, garantizando la validez de los resultados.</p>',unsafe_allow_html=True)
    st.markdown('<p style="text-align:justify;">Las mediciones de calidad que soportan las gráficas de la aplicación están basadas en la metodología crowdsourcing, utilizando para ellos los datos proporcionados por la aplicación Speedtest®, desarrollada por la empresa Ookla®. A través de esta metodología se recopila información directamente desde los dispositivos que los usuarios utilizan para acceder a los servicios de Internet móvil e Internet fijo, suministrados por los proveedores de redes y servicios de telecomunicaciones.</p>',unsafe_allow_html=True)
    Sevidores_map = folium.Map(location=[3, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
    scrollWheelZoom=True,
    dragging=True)
    tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
    folium.TileLayer('openstreetmap').add_to(Sevidores_map)
    choropleth=folium.Choropleth(
        geo_data=Colombian_DPTO2,
        key_on='feature.properties.NOMBRE_DPT',
        fill_color='rgb(0,204,0)', 
        fill_opacity=0.2, 
        line_opacity=1,
        nan_fill_color ="rgba(0,0,0,0)",
        smooth_factor=0).add_to(Sevidores_map)


    # add marker one by one on the map
    for i in range(0,len(Servidores)):
        html2=f"""<b>Nombre:</b>\n
        {Servidores.iloc[i]['server_name']}<br>
        <b>Cantidad servidores:</b>\n
        {Servidores.iloc[i]['Cantidad servidores']}
        """
        iframe2=folium.IFrame(html=html2, width=110, height=105)
        popup2=folium.Popup(iframe2)    
        folium.CircleMarker(
          location=[Servidores.iloc[i]['latitude'], Servidores.iloc[i]['longitude']],
          popup=popup2,radius=10,weight=1,
     color='black',       
     fill=True,
     #fill_color=dict_serv_colores[Servidores.iloc[i]['server_name']],
     fill_opacity=0.2
       ).add_to(Sevidores_map) 
       
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### <b>Distribución de servidores de pruebas en Colombia</b>",unsafe_allow_html=True)
        st.markdown('<p style="text-align:justify;">Las mediciones de los indicadores de calidad se soportan en el uso de una red que para 2021 incorporaba 38 servidores de prueba dispersos en el territorio nacional. Estas se muestran en el mapa a continuación.</p>',unsafe_allow_html=True)    
        st.markdown("")
        folium_static(Sevidores_map,width=350)  
        st.markdown(r"""<p style=font-size:10px>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022. 
        Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.</p>""",unsafe_allow_html=True)
    with col2:
        st.markdown("### Indicadores de desempeño",unsafe_allow_html=True)
        st.markdown('<p style="text-align:justify;">el rendimiento o desempeño del servicio de internet se refiere a los resultados de los indicadores de calidad del servicio de telecomunicaciones desde el punto de vista del usuario. Los más relevantes están relacionados con las velocidades y los tiempos de retardo de las conexiones.</p>',unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Velocidad de descarga", "Velocidad de carga", "Latencia"])
        with tab1:
            st.markdown('<p style="text-align:justify;">La velocidad de descarga Se entiende como la rapidez con la se pueden descargar contenidos, normalmente desde una página Web. A mayor velocidad obtenida en la medición, mayor rapidez en la descarga, por lo tanto, mejor experiencia del usuario. Es usual medirla en  Megabit por segundo (Mbps)</p>',unsafe_allow_html=True)
        with tab2:
            st.markdown('<p style="text-align:justify;">La velocidad de carga se entiende como la medida de qué tan rápido se envían los datos en dirección desde un dispositivo hacia Internet. Es decir, es la rapidez con la que se pueden subir contenidos a Internet. A mayor velocidad obtenida en la medición, mayor rapidez en la carga, por lo tanto, mejor es la experiencia del usuario. Se mide en Mebagit por segundo (Mbps)</p>',unsafe_allow_html=True)
        with tab3:
            st.markdown('<p style="text-align:justify;">El parámetro de latencia sirve para medir qué tan rápido viajan los datos desde un punto de origen al destino. La experiencia al intentar acceder a audio, video y videojuegos es mejor con latencias más bajas, por lo cual, si el tiempo obtenido en la medición es pequeño, la experiencia del usuario es mejor. La latencia se mide en milisegundos (ms).</p>',unsafe_allow_html=True)

        
#################################Lectura de bases Internet fijo#######################################33
pathFijo2='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2023/Fijo/'
#pathFijo=r'C:\Users\santiago.bermudez\COMISION DE REGULACIÓN DE COMUNICACIONES\Mediciones Calidad QoE - Documents\Datos\Internet fijo\Mediana\\'
periodo_tope='2023-06-01'

####Primera sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion1Fijo():
    Colombia1Fijo=pd.read_csv(pathFijo2+"Colombia-histcomp_month_2018-2023(Med).csv", delimiter=';')
    FeAntig1Fijo = Colombia1Fijo['Aggregate Date'].unique()
    FeCorre1Fijo = pd.date_range('2018-01-01',periodo_tope, freq='MS').strftime("%d-%b-%y").tolist()
    diction1Fijo = dict(zip(FeAntig1Fijo, FeCorre1Fijo))
    Colombia1Fijo['Aggregate Date'] = pd.to_datetime(Colombia1Fijo['Aggregate Date'].replace(diction1Fijo), dayfirst=True)
    Colombia1Fijo['month'] = Colombia1Fijo['Aggregate Date'].dt.month
    Colombia1Fijo['year'] = Colombia1Fijo['Aggregate Date'].dt.year
    Colombia1Fijo.drop(['Location', 'Platform', 'Technology Type', 'Metric Type', 'Provider'], axis=1, inplace=True)
    return Colombia1Fijo
Colombia1Fijo=Seccion1Fijo()
Colombia1Fijo=Colombia1Fijo.rename(columns={'Minimum Latency':'Latency'})

####Segunda sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion2Fijo():
    df2_1Fijo=pd.read_csv(pathFijo2+'ETBMOVCLA-histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig').dropna(how='all') 
    df2_2Fijo=pd.read_csv(pathFijo2+'TIGOEMCALI-histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig').dropna(how='all') 
    OpCiud2Fijo=pd.concat([df2_1Fijo,df2_2Fijo])
    return OpCiud2Fijo
OpCiud2Fijo=Seccion2Fijo()    
OpCiud2Fijo['Location']=OpCiud2Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntig2Fijo=OpCiud2Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre2Fijo=pd.date_range('2018-01-01',periodo_tope, 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction2Fijo=dict(zip(FeAntig2Fijo, FeCorre2Fijo))
OpCiud2Fijo['Aggregate Date'].replace(diction2Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
OpCiud2Fijo['Aggregate Date'] =pd.to_datetime(OpCiud2Fijo['Aggregate Date']).dt.floor('d') 
OpCiud2Fijo['month']=pd.DatetimeIndex(OpCiud2Fijo['Aggregate Date']).month
OpCiud2Fijo['year']=pd.DatetimeIndex(OpCiud2Fijo['Aggregate Date']).year
OpCiud2Fijo= OpCiud2Fijo.drop(['Device','Platform','Technology Type','Metric Type'],axis=1)
OpCiud2Fijo['Location'] = OpCiud2Fijo['Location'].str.upper()
OpCiud2Fijo['Location'] = OpCiud2Fijo['Location'].replace({'SANTANDER DEPARTMENT':'SANTANDER','CAUCA DEPARTMENT':'CAUCA','SAN ANDRÉS AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA','NORTH SANTANDER':'NORTE DE SANTANDER','CAQUETÁ':'CAQUETA'})
OpCiud2Fijo=OpCiud2Fijo.rename(columns={'Minimum Latency':'Latency'})
geoJSON_states2 = list(gdf2.NOMBRE_DPT.values)
denominations_json2 = []
Id_json2 = []

for index in range(len(Colombian_DPTO2['features'])):
    denominations_json2.append(Colombian_DPTO2['features'][index]['properties']['NOMBRE_DPT'])
    Id_json2.append(Colombian_DPTO2['features'][index]['properties']['DPTO'])
denominations_json2=sorted(denominations_json2)
dataframe_names2=sorted(OpCiud2Fijo.Location.unique().tolist())
OpCiud2Fijo=OpCiud2Fijo[OpCiud2Fijo['Test Count']>30]
gdf2=gdf2.rename(columns={"NOMBRE_DPT":'Location'})
# Filtro calidad Ookla
OpCiud2Fijocond = OpCiud2Fijo.groupby(['year', 'Location'])['User Count'].agg(['count', lambda x: (x > 200).sum()])
OpCiud2Fijocond.rename(columns={'count':'meses_obs','<lambda_0>':'Cumple'},inplace=True)
OpCiud2Fijocond['Porc_cumplimiento'] = (OpCiud2Fijocond['Cumple'] / OpCiud2Fijocond['meses_obs']) 
filtroOpCiud2Fijocond = OpCiud2Fijocond[OpCiud2Fijocond['Porc_cumplimiento'] < 0.75]
annos_excluirOpCiud2Fijocond = filtroOpCiud2Fijocond.index.get_level_values('year').tolist()
muni_excluirOpCiud2Fijocond = filtroOpCiud2Fijocond.index.get_level_values('Location').tolist()
filtro_completoOpCiud2Fijo = None
for year, location in zip(annos_excluirOpCiud2Fijocond, muni_excluirOpCiud2Fijocond):
    condition_OpCiud2Fijo = (OpCiud2Fijo['year'] == year) & (OpCiud2Fijo['Location'] == location)
    if filtro_completoOpCiud2Fijo is None:
        filtro_completoOpCiud2Fijo = condition_OpCiud2Fijo
    else:
        filtro_completoOpCiud2Fijo = filtro_completoOpCiud2Fijo | condition_OpCiud2Fijo
OpCiud2Fijo = OpCiud2Fijo[~filtro_completoOpCiud2Fijo]


####Tercera sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion3Fijo():
    df3_1Fijo=pd.read_csv(pathFijo2+'Ciud(1-10)histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig')
    df3_2Fijo=pd.read_csv(pathFijo2+'Ciud(11-17)histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig')
    df3_3Fijo=pd.read_csv(pathFijo2+'Ciud(18-24)histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig')
    df3_4Fijo=pd.read_csv(pathFijo2+'Ciud(24-32)histcomp_month_2018-2023(Med).csv',delimiter=';',encoding='utf-8-sig')
    Ciudades3Fijo=pd.concat([df3_1Fijo,df3_2Fijo,df3_3Fijo,df3_4Fijo])#Unir los dataframes
    return Ciudades3Fijo
Ciudades3Fijo=Seccion3Fijo()
Ciudades3Fijo['Aggregate Date']=Ciudades3Fijo['Aggregate Date'].astype('str')    
Ciudades3Fijo['Aggregate Date']=Ciudades3Fijo['Aggregate Date'].replace(" ", "-").str.title() #Unir espacios blancos 
Ciudades3Fijo['Location']=Ciudades3Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntig3Fijo=Ciudades3Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre3Fijo=pd.date_range('2018-01-01',periodo_tope, 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction3Fijo=dict(zip(FeAntig3Fijo, FeCorre3Fijo))
Ciudades3Fijo['Aggregate Date'].replace(diction3Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Ciudades3Fijo['Aggregate Date'] = pd.to_datetime(Ciudades3Fijo['Aggregate Date'],errors='coerce')
Ciudades3Fijo['year']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).year
Ciudades3Fijo['month']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).month
Ciudades3Fijo=Ciudades3Fijo.drop(['Device','Platform','Technology Type','Metric Type','Provider'], axis=1)
Ciudades3Fijo=Ciudades3Fijo.rename(columns={'Minimum Latency':'Latency'})
Ciudades3Fijo['Location']=Ciudades3Fijo['Location'].replace({'San José Del Guaviare':'San José<br>Del Guaviare'},regex=True)
# Filtro calidad Ookla
Ciudades3Fijocond = Ciudades3Fijo.groupby(['year', 'Location'])['User Count'].agg(['count', lambda x: (x > 200).sum()])
Ciudades3Fijocond.rename(columns={'count':'meses_obs','<lambda_0>':'Cumple'},inplace=True)
Ciudades3Fijocond['Porc_cumplimiento'] = (Ciudades3Fijocond['Cumple'] / Ciudades3Fijocond['meses_obs']) 
filtroCiudades3Fijocond = Ciudades3Fijocond[Ciudades3Fijocond['Porc_cumplimiento'] < 0.75]
annos_excluirCiudades3Fijocond = filtroCiudades3Fijocond.index.get_level_values('year').tolist()
muni_excluirCiudades3Fijocond = filtroCiudades3Fijocond.index.get_level_values('Location').tolist()
filtro_completoCiudades3Fijo = None
for year, location in zip(annos_excluirCiudades3Fijocond, muni_excluirCiudades3Fijocond):
    condition_Ciudades3Fijo = (Ciudades3Fijo['year'] == year) & (Ciudades3Fijo['Location'] == location)
    if filtro_completoCiudades3Fijo is None:
        filtro_completoCiudades3Fijo = condition_Ciudades3Fijo
    else:
        filtro_completoCiudades3Fijo = filtro_completoCiudades3Fijo | condition_Ciudades3Fijo
Ciudades3Fijo = Ciudades3Fijo[~filtro_completoCiudades3Fijo]


####Cuarta sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion4Fijo():
    Operadores4Fijo=pd.read_csv(pathFijo2+'Op-histcomp_month_2018-2023(Med).csv',delimiter=';')
    cols_to_changeFijo=['Download Speed Mbps']
    if Operadores4Fijo['Download Speed Mbps'].dtypes !='float64':
        for col in cols_to_changeFijo:
            Operadores4Fijo[col]=Operadores4Fijo[col].str.replace(',','.')
            Operadores4Fijo[col]=Operadores4Fijo[col].astype(float)
    return Operadores4Fijo
Operadores4Fijo=Seccion4Fijo()    
FeAntig4Fijo=Operadores4Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre4Fijo=pd.date_range('2018-01-01',periodo_tope, 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction4Fijo=dict(zip(FeAntig4Fijo, FeCorre4Fijo))
Operadores4Fijo['Aggregate Date'].replace(diction4Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Operadores4Fijo['Aggregate Date'] =pd.to_datetime(Operadores4Fijo['Aggregate Date']).dt.floor('d') 
Operadores4Fijo['month']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).month
Operadores4Fijo['year']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).year
Operadores4Fijo=Operadores4Fijo.drop(['Location','Device','Platform','Technology Type','Metric Type'],axis=1)
Operadores4Fijo=Operadores4Fijo.rename(columns={'Minimum Latency':'Latency'})

Colombia2Fijo=pd.read_csv(pathFijo2+'Allproviders-histcomp_month_2020-2023(Med).csv',delimiter=';')
Colombia2Fijo['Location']=Colombia2Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntigFijo=Colombia2Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorreFijo=pd.date_range('2020-06-01',periodo_tope, 
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
Colombia2Fijo=Colombia2Fijo.rename(columns={'Minimum Latency':'Latency'})
# Filtro calidad Ookla
Colombia2Fijocond = Colombia2Fijo.groupby(['year', 'Location'])['User Count'].agg(['count', lambda x: (x > 200).sum()])
Colombia2Fijocond.rename(columns={'count':'meses_obs','<lambda_0>':'Cumple'},inplace=True)
Colombia2Fijocond['Porc_cumplimiento'] = (Colombia2Fijocond['Cumple'] / Colombia2Fijocond['meses_obs']) 
filtroColombia2Fijocond = Colombia2Fijocond[Colombia2Fijocond['Porc_cumplimiento'] < 0.75]
annos_excluirColombia2Fijocond = filtroColombia2Fijocond.index.get_level_values('year').tolist()
muni_excluirColombia2Fijocond = filtroColombia2Fijocond.index.get_level_values('Location').tolist()
filtro_completoColombia2Fijo = None
for year, location in zip(annos_excluirColombia2Fijocond, muni_excluirColombia2Fijocond):
    condition_Colombia2Fijo = (Colombia2Fijo['year'] == year) & (Colombia2Fijo['Location'] == location)
    if filtro_completoColombia2Fijo is None:
        filtro_completoColombia2Fijo = condition_Colombia2Fijo
    else:
        filtro_completoColombia2Fijo = filtro_completoColombia2Fijo | condition_Colombia2Fijo
Colombia2Fijo = Colombia2Fijo[~filtro_completoColombia2Fijo]



def DataMuni2023():
    datamuni2023=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2023/Fijo/CRC_Fixed_Aggs_Monthly_2023.csv',delimiter=',')
    datamuni2023=datamuni2023.rename(columns={'name':'DESC_MUNICIPIO'})
    datamuni2023['DESC_MUNICIPIO']=datamuni2023['DESC_MUNICIPIO'].str.upper()
    return datamuni2023
datamuni2023=DataMuni2023()
CapDep=['LETICIA','MEDELLIN','ARAUCA','BARRANQUILLA','BOGOTA','CARTAGENA','TUNJA','MANIZALES','FLORENCIA','YOPAL','POPAYÁN',
            'VALLEDUPAR','QUIBDÓ','MONTERÍA','INÍRIDA','SAN JOSÉ DEL GUAVIARE','NEIVA','RIOHACHA','SANTA MARTA','VILLAVICENCIO',
            'PASTO','CUCUTA','MOCOA','ARMENIA','PEREIRA','SAN ANDRÉS','BUCARAMANGA','SINCELEJO','IBAGUE','CALI','MITÚ',
            'PUERTO CARREÑO']
datamuni2023=datamuni2023[datamuni2023['DESC_MUNICIPIO'].isin(CapDep)]
datamuni2023=datamuni2023[(datamuni2023['connection_type']=='All Fixed')&(datamuni2023['aggregate_date']<'2023-07-01')&(datamuni2023['test_count']>=30)]
dict_colores_op={'Claro':'red','Tigo':'rgb(153,51,255)','ETB':'rgb(0,153,153)','Movistar':'rgb(51,255,51)','All combined':'black'}


if select_servicio == 'Internet fijo':
    select_indicador=st.selectbox('Indicador de desempeño',['Velocidad de descarga','Velocidad de carga','Latencia'])
    
    if select_indicador== 'Velocidad de descarga':
        dimension_Vel_descarga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_descarga_Fijo == 'Histórico Colombia':
            tab1,tab2=st.tabs(["Evolución indicador","Mapa departamental"])
            with tab1:
                Downspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Download Speed Mbps'].mean().round(2).reset_index()
                Downspeed1Fijo['Aggregate Date']=Downspeed1Fijo['Aggregate Date'].astype('str')
                
                fig1Fijo = make_subplots(rows=1, cols=1)
                fig1Fijo.add_trace(go.Scatter(x=Downspeed1Fijo['Aggregate Date'].values, y=Downspeed1Fijo['Download Speed Mbps'].values,
                                         line=dict(color='blue', width=2),name=' ',mode='lines+markers',fill='tonexty', fillcolor='rgba(0,0,255,0.2)'),row=1, col=1)
                fig1Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01','2022-06-01','2022-12-01','2023-06-01'])
                fig1Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig1Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad descarga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig1Fijo.update_traces(textfont_size=18)
                fig1Fijo.update_layout(height=500,legend_title=None)
                #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                fig1Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                fig1Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
                title={
                'text': "<b>Velocidad mensual de descarga de Internet fijo en <br>Colombia (2018-2023/1S) (en Mbps) </b>",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig1Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2023/1S.',
                font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
                st.plotly_chart(fig1Fijo, use_container_width=True)
            #st.download_button(label="Descargar CSV",data=convert_df(Downspeed1Fijo),file_name='Historico_descarga_Colombia.csv',mime='text/csv')


            ##
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                Col2Fijo=Colombia2Fijo[(Colombia2Fijo['year']==año_opFijo)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Download Speed Mbps'].mean()
                Col2Fijo=round(Col2Fijo,2)
                departamentos_df2Fijo=gdf2.merge(Col2Fijo, on='Location')
                departamentos_df2Fijo=departamentos_df2Fijo.sort_values(by='Download Speed Mbps')
                if departamentos_df2Fijo.empty==True:
                    st.markdown('No se presentan datos para el mes seleccionado.')
                else:    
                    # create a plain world map
                    colombia_map1Fijo = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                       scrollWheelZoom=True,
                       dragging=True)
                    tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                    for tile in tiles:
                        folium.TileLayer(tile).add_to(colombia_map1Fijo)
                    choropleth=folium.Choropleth(
                        geo_data=Colombian_DPTO2,
                        data=departamentos_df2Fijo,
                        #bins=[0,5,15,25,50,75,100],
                        columns=['Location', 'Download Speed Mbps'],
                        key_on='feature.properties.NOMBRE_DPT',
                        fill_color='YlGnBu', 
                        fill_opacity=0.9, 
                        line_opacity=0.9,
                        #legend_name='Velocidad de descarga (Mbps)',
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
                    #Quitar barra de colores
                    for key in choropleth._children:
                        if key.startswith('color_map'):
                            del(choropleth._children[key])
                    colombia_map1Fijo.add_child(NIL)
                    colombia_map1Fijo.keep_in_front(NIL)
                    
                    col1b, col2b ,col3b= st.columns([1,4,1])
                    with col2b:
                        st.markdown("<b><center>Velocidad de descarga de Internet fijo en Colombia<br>por departamento (en Mbps)</center></b>",unsafe_allow_html=True)  
                        folium_static(colombia_map1Fijo,width=480) 
                        st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2023</i></p> """,unsafe_allow_html=True)
                
        if dimension_Vel_descarga_Fijo == 'Ciudades':  
            tab1,tab2,tab3=st.tabs(["Comparación anual","Diagrama de dispersión","Información por operadores"])
            with tab1:
                col1, col2,col3= st.columns(3)
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
                mes=mes_opFijoNombre[mes_opFijo]     
                
                df19A3Fijo=pd.DataFrame();df20A3Fijo=pd.DataFrame();df21A3Fijo=pd.DataFrame();df22A3Fijo=pd.DataFrame();df23A3Fijo=pd.DataFrame()
                p19A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
                p20A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
                p21A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
                p22A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
                p23A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2023)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
                df19A3Fijo['Location']=p19A3Fijo.index;df19A3Fijo['2019']=p19A3Fijo.values;
                df20A3Fijo['Location']=p20A3Fijo.index;df20A3Fijo['2020']=p20A3Fijo.values;
                df21A3Fijo['Location']=p21A3Fijo.index;df21A3Fijo['2021']=p21A3Fijo.values;
                df22A3Fijo['Location']=p22A3Fijo.index;df22A3Fijo['2022']=p22A3Fijo.values;
                df23A3Fijo['Location']=p23A3Fijo.index;df23A3Fijo['2023']=p23A3Fijo.values;
                from functools import reduce
                DepJoinA3Fijo=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19A3Fijo,df20A3Fijo,df21A3Fijo,df22A3Fijo,df23A3Fijo]).set_index('Location')
                DepJoinA3Fijo=DepJoinA3Fijo.round(2).reset_index()
                DepJoinA3Fijo=DepJoinA3Fijo[DepJoinA3Fijo.Location != 'Colombia']

                DepJoinA3Fijo=DepJoinA3Fijo.sort_values(by=['2023'],ascending=False)
                DepJoinA3Fijo['relatGrow']=100*np.abs(DepJoinA3Fijo['2023']-DepJoinA3Fijo['2022'])/DepJoinA3Fijo['2022']
                DepJoinA3Fijo['absGrow']=DepJoinA3Fijo['2023']-DepJoinA3Fijo['2022']
                DepJoinA3Fijocopy=DepJoinA3Fijo.copy()
                DepJoinA3Fijocopy['2018']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2019'],1).astype(str)]
                DepJoinA3Fijocopy['2019']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2020'],1).astype(str)]
                DepJoinA3Fijocopy['2020']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2021'],1).astype(str)]
                DepJoinA3Fijocopy['2021']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2022'],1).astype(str)]
                DepJoinA3Fijocopy['2022']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2022'],1).astype(str)]
                name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
                
                fig2Fijo =go.Figure()
                fig2Fijo.add_trace(go.Bar(
                x=DepJoinA3Fijo['Location'],
                y=DepJoinA3Fijo['2020'],
                name=mes_opFijo+' 2020',
                marker_color='rgb(213,3,85)',textposition = "inside"))
                fig2Fijo.add_trace(go.Bar(
                x=DepJoinA3Fijo['Location'],
                y=DepJoinA3Fijo['2021'],
                name=mes_opFijo+' 2021',
                marker_color='rgb(255,152,0)',textposition = "inside"))
                fig2Fijo.add_trace(go.Bar(
                x=DepJoinA3Fijo['Location'],
                y=DepJoinA3Fijo['2022'],
                name=mes_opFijo+' 2022',
                marker_color='rgb(44,198,190)',textposition = "inside"))
                fig2Fijo.add_trace(go.Bar(
                x=DepJoinA3Fijo['Location'],
                y=DepJoinA3Fijo['2023'],
                name=mes_opFijo+' 2023',
                marker_color='rgb(72,68,242)',textposition = "outside"))
                fig2Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig2Fijo.update_yaxes(range=[0,max(DepJoinA3Fijo['2023'].values.tolist())+5],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Velocidad descarga (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig2Fijo.update_traces(textfont_size=18)
                fig2Fijo.update_layout(height=600,width=1200,legend_title=None)
                fig2Fijo.update_layout(legend=dict(orientation="h",yanchor='top',xanchor='center',x=0.5,y=0.8))
                fig2Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig2Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,font=dict(size=14),
                title={
                'text': "<b>Velocidad anual de descarga de Internet fijo por ciudad<br> (2020-2023/1S) </b>",
                'y':0.8,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig2Fijo.update_layout(barmode='group')
                fig2Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.4)
                st.plotly_chart(fig2Fijo, use_container_width=True)  

            with tab2:
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12} 

                col1, col2= st.columns(2)
                with col1:
                    Año_opFijoIz = st.selectbox('Escoja el año para el panel de la izquierda',[2018,2019,2020,2021,2022],index=4)
                    Mes_opFijoIz = st.selectbox('Escoja el mes para el panel de la izquierda',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],index=5) 
                    mesIz=mes_opFijoNombre[Mes_opFijoIz] 
                with col2:
                    Mes_opFijoDer = st.selectbox('Escoja el mes de 2023 para el panel de la derecha',['Enero','Febrero','Marzo','Abril','Mayo','Junio'],index=5)           
                    mesDer=mes_opFijoNombre[Mes_opFijoDer]
                name_mes2={1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
                DicIz=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==Año_opFijoIz)&(Ciudades3Fijo['month']==mesIz)&(Ciudades3Fijo['Latency']<100)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
                DicDer=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2023)&(Ciudades3Fijo['month']==mesDer)&(Ciudades3Fijo['Latency']<100)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
                DicIzList=DicIz['Location'].unique().tolist()
                DicDerList=DicDer['Location'].unique().tolist()
                if 'Colombia' in DicIzList:
                    DicIzList.remove('Colombia')
                if 'Colombia' in DicDerList:
                    DicDerList.remove('Colombia')            
                dict_coloresFijo = {
                    'Bucaramanga': 'rgb(255,128,0)',
                    'Bogotá': 'rgb(255,0,0)',
                    'Cali': 'rgb(255,255,0)',
                    'Medellín': 'rgb(128,255,0)',
                    'Barranquilla': 'rgb(0,255,0)',
                    'Cartagena': 'rgb(0,255,128)',
                    'Villavicencio': 'rgb(255,102,102)',
                    'Ibagué': 'rgb(0,128,255)',
                    'Manizales': 'rgb(0,0,255)',
                    'Tunja': 'rgb(127,0,255)',
                    'Pasto': 'rgb(255,0,255)',
                    'Santa Marta': 'rgb(255,0,127)',
                    'Sincelejo': 'rgb(128,128,128)',
                    'Armenia': 'rgb(102,0,0)',
                    'Montería': 'rgb(0,255,255)',
                    'Pereira': 'rgb(0,51,51)',
                    'Popayán': 'rgb(51,0,25)',
                    'Cúcuta': 'rgb(0, 204, 102)',
                    'Neiva': 'rgb(255, 102, 0)',
                    'Valledupar': 'rgb(102, 102, 255)',
                    'Riohacha': 'rgb(255, 153, 204)',
                    'Arauca': 'rgb(0, 153, 153)',
                    'Yopal': 'rgb(255, 204, 0)',
                    'Florencia': 'rgb(153, 51, 255)',
                    'San José<br>Del Guaviare': 'rgb(204, 204, 204)',
                    'San Andrés': 'rgb(204, 0, 204)',
                    'Quibdo': 'rgb(255, 204, 153)',
                    'Puerto Carreño':'rgb(192,192,192)',
                    'Leticia':'rgb(0,0,0)',
                     'Mitú':'rgb(0,100,0)',
                    'Inírida':'rgb(132,142,124)'
                    }
                fig4Fijo = make_subplots(rows=1, cols=2,subplot_titles=(Mes_opFijoIz+' '+str(Año_opFijoIz),
                Mes_opFijoDer+" 2023"))

                for location in DicIzList:
                    fig4Fijo.add_trace(go.Scatter(
                        x=DicIz[DicIz['Location']==location]['Download Speed Mbps'].values, y=DicIz[DicIz['Location']==location]['Upload Speed Mbps'].values, 
                        mode='markers',
                        marker=dict(
                            color=dict_coloresFijo[location],
                            opacity=0.7,
                            size=2*DicIz[DicIz['Location']==location]['Latency'].values,
                        ),
                    text=DicIz[DicIz['Location']==location]['Latency'].values,showlegend=False,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
                    
                for location in DicDerList:
                    fig4Fijo.add_trace(go.Scatter(
                        x=DicDer[DicDer['Location']==location]['Download Speed Mbps'].values, y=DicDer[DicDer['Location']==location]['Upload Speed Mbps'].values, name=location,
                        mode='markers',
                        marker=dict(
                            color=dict_coloresFijo[location],
                            opacity=0.7,
                            size=2*DicDer[DicDer['Location']==location]['Latency'].values,
                        ),
                    text=DicDer[DicDer['Location']==location]['Latency'].values,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=2)


                fig4Fijo.update_xaxes(tickangle=0,range=[0,max(DicDer['Download Speed Mbps'].values.tolist())+10],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig4Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18,ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig4Fijo.update_traces(textfont_size=18)
                fig4Fijo.update_layout(height=700,legend_title=None)
                fig4Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
                fig4Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
                title={
                'text': "<b> Diagrama de burbujas para índices de desempeño de Internet fijo por ciudad</b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  

                fig4Fijo.update_xaxes(showspikes=True,title_text='Velocidad de descarga (Mbps)',titlefont_size=18)
                fig4Fijo.update_yaxes(showspikes=True,range=[0,max(DicDer['Upload Speed Mbps'].values.tolist())+10],title_text="Velocidad de carga (Mbps)", row=1, col=1)
                fig4Fijo.update_yaxes(showspikes=True,range=[0,max(DicDer['Upload Speed Mbps'].values.tolist())+10],title_text=None, row=1, col=2)
                fig4Fijo.update_layout(legend=dict(y=0.95,x=1,orientation='v'))
                fig4Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='x domain',x=0.33,yref='y domain',y=-0.16)            
                st.plotly_chart(fig4Fijo, use_container_width=True)

                DicIz_maxLat=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==Año_opFijoIz)&(Ciudades3Fijo['month']==mesIz)&(Ciudades3Fijo['Latency']>=100)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
                DicDer_maxLat=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2023)&(Ciudades3Fijo['month']==mesDer)&(Ciudades3Fijo['Latency']>=100)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
                listDicIz_maxLat=DicIz_maxLat[['Location','Latency']].values.tolist()
                resultDicIz_maxLat = [f'{item[0]} ({item[1]} ms)' for item in listDicIz_maxLat]
                listDicDer_maxLat=DicDer_maxLat[['Location','Latency']].values.tolist()
                resultDicDer_maxLat = [f'{item[0]} ({item[1]} ms)' for item in listDicDer_maxLat]
                st.markdown(f"""<b>Nota</b>: Las ciudades exlcuidas de la gráfica para el periodo {Año_opFijoIz}-{mesIz} son: {resultDicIz_maxLat}.<br>
                            Para el periodo 2023-{mesDer} estas son: {resultDicDer_maxLat}""",unsafe_allow_html=True)

            with tab3:
                select_capdep=st.selectbox('Escoja la ciudad capital de departamento',CapDep,4)
                datamuni2023_cap=datamuni2023[(datamuni2023['DESC_MUNICIPIO']==select_capdep)].sort_values(by='aggregate_date')

                fig_muniOp=go.Figure()
                for op in datamuni2023_cap['provider'].unique():
                    if op not in dict_colores_op.keys():
                        color_op='rgb(192,192,192)'
                    else:
                        color_op=dict_colores_op[op]
                    df_muniOp=datamuni2023_cap[datamuni2023_cap['provider']==op]
                    fig_muniOp.add_trace(go.Scatter(x=df_muniOp['aggregate_date'],y=df_muniOp['median_download_mbps'],mode='lines+markers',name=op,marker_color=color_op
                    ))
                    
                    fig_muniOp.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                    fig_muniOp.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                    fig_muniOp.update_traces(textfont_size=18)
                    fig_muniOp.update_layout(height=500,legend_title=None,font=dict(size=18))
                    fig_muniOp.update_layout(legend=dict(orientation="h",y=1.1,x=0.35),showlegend=True)
                    fig_muniOp.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                    fig_muniOp.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,
                    title={
                    'text': f"<b>Velocidad mensual de descarga de Internet fijo por proveedor ({select_capdep}) </b>",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})  
                    fig_muniOp.update_xaxes(tickvals=['2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01'])
                    fig_muniOp.add_annotation(
                    showarrow=False,
                    text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                    font=dict(size=10), xref='paper',yref='y domain',y=-0.25)                     
                st.plotly_chart(fig_muniOp, use_container_width=True)     
                
        if dimension_Vel_descarga_Fijo == 'Operadores': 
            TodosDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            TodosDescarga4Fijo['Aggregate Date']=TodosDescarga4Fijo['Aggregate Date'].astype('str')
            ETBDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            ETBDescarga4Fijo['Aggregate Date']=ETBDescarga4Fijo['Aggregate Date'].astype('str')
            MOVISTARDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            MOVISTARDescarga4Fijo['Aggregate Date']=MOVISTARDescarga4Fijo['Aggregate Date'].astype('str')
            CLARODescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            CLARODescarga4Fijo['Aggregate Date']=CLARODescarga4Fijo['Aggregate Date'].astype('str')
            TIGODescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            TIGODescarga4Fijo['Aggregate Date']=TIGODescarga4Fijo['Aggregate Date'].astype('str')
            
            JuntosDescarga4Fijo=pd.concat([TodosDescarga4Fijo,ETBDescarga4Fijo,MOVISTARDescarga4Fijo,CLARODescarga4Fijo,TIGODescarga4Fijo])
        
            tab1,tab2,tab3=st.tabs(["Evolución indicador","Mapa departamental","Diagrama de dispersión"])
            with tab1:
                fig3Fijo = make_subplots(rows=1, cols=1)
                fig3Fijo.add_trace(go.Scatter(x=TodosDescarga4Fijo['Aggregate Date'].values, y=TodosDescarga4Fijo['Download Speed Mbps'].values,
                                         line=dict(color='black', width=1, dash='dash'),mode='lines',name='Colombia'),row=1, col=1)
                fig3Fijo.add_trace(go.Scatter(x=ETBDescarga4Fijo['Aggregate Date'].values, y=ETBDescarga4Fijo['Download Speed Mbps'].values,
                                         line=dict(color='rgb(0,153,153)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(0,153,153)',width=1)),mode='lines+markers',name='ETB'),row=1, col=1)
                fig3Fijo.add_trace(go.Scatter(x=MOVISTARDescarga4Fijo['Aggregate Date'].values, y=MOVISTARDescarga4Fijo['Download Speed Mbps'].values,
                                         line=dict(color='rgb(51,255,51)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(51,255,51)',width=1)),mode='lines+markers',name='Movistar'),row=1, col=1)
                fig3Fijo.add_trace(go.Scatter(x=CLARODescarga4Fijo['Aggregate Date'].values, y=CLARODescarga4Fijo['Download Speed Mbps'].values,
                                         line=dict(color='red', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='red',width=1)),mode='lines+markers',name='Claro'),row=1, col=1)
                fig3Fijo.add_trace(go.Scatter(x=TIGODescarga4Fijo['Aggregate Date'].values, y=TIGODescarga4Fijo['Download Speed Mbps'].values,
                                         line=dict(color='rgb(153,51,255)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(153,51,255)',width=1)),mode='lines+markers',name='Tigo'),row=1, col=1)

                fig3Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig3Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad descarga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig3Fijo.update_traces(textfont_size=18)
                fig3Fijo.update_layout(height=500,legend_title=None,font=dict(size=18))
                fig3Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.01),showlegend=True)
                fig3Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig3Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,
                title={
                'text': "<b>Velocidad mensual de descarga de Internet fijo<br>por proveedor (2018-2023/1S) (en Mbps)</b>",
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig3Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01',
                '2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01',
                '2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01','2022-03-01','2022-06-01','2022-09-01','2022-12-01','2023-03-01','2023-06-01'])
                fig3Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
                st.plotly_chart(fig3Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosDescarga4Fijo),file_name='Historico_descarga_Operadores.csv',mime='text/csv')            
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                final_dfAncFijo=gdf2.merge(OpCiud2Fijo.groupby(['Location'])['Download Speed Mbps'].median().reset_index(), on='Location')
                final_dfAncFijo['Download Speed Mbps']=np.nan
                
                Proveedor1Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor1Fijo['Download Speed Mbps'] =round(Proveedor1Fijo['Download Speed Mbps'], 2)
                if Proveedor1Fijo.empty==True:
                    final_df1Fijo=final_dfAncFijo
                else:    
                    final_df1Fijo=gdf2.merge(Proveedor1Fijo, on='Location')
                ##
                Proveedor2Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor2Fijo['Download Speed Mbps'] =round(Proveedor2Fijo['Download Speed Mbps'], 2)
                if Proveedor2Fijo.empty==True:
                    final_df2Fijo=final_dfAncFijo
                else:    
                    final_df2Fijo=gdf2.merge(Proveedor2Fijo, on='Location')
                ##
                Proveedor3Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor3Fijo['Download Speed Mbps'] =round(Proveedor3Fijo['Download Speed Mbps'], 2)
                if Proveedor3Fijo.empty==True:
                    final_df3Fijo=final_dfAncFijo
                else:    
                    final_df3Fijo=gdf2.merge(Proveedor3Fijo, on='Location')
                ##
                Proveedor4Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor4Fijo['Download Speed Mbps'] =round(Proveedor4Fijo['Download Speed Mbps'], 2)
                if Proveedor4Fijo.empty==True:
                    final_df4Fijo=final_dfAncFijo
                else:    
                    final_df4Fijo=gdf2.merge(Proveedor4Fijo, on='Location')
                

                dualmap1_1Fijo=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                   scrollWheelZoom=True,
                   dragging=True)
                ########
                choropleth1=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df1Fijo,
                    #bins=[0,15,50,75,100,125,150,175,190],
                    columns=['Location', 'Download Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de descarga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_1Fijo.m1)
                #######
                choropleth2=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df2Fijo,
                    #bins=[0,15,50,75,100,125,150,175,190],
                    columns=['Location', 'Download Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de descarga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_1Fijo.m2)

                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth1.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_1Fijo.m1)
                choropleth2.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_1Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_df1Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Download Speed Mbps'],
                        aliases=['Departamento','Velocidad descarga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_df2Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Download Speed Mbps'],
                        aliases=['Departamento','Velocidad descarga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth1._children:
                    if key.startswith('color_map'):
                        del(choropleth1._children[key])
                for key in choropleth2._children:
                    if key.startswith('color_map'):
                        del(choropleth2._children[key])

                dualmap1_1Fijo.m1.add_child(NIL1)
                dualmap1_1Fijo.m1.keep_in_front(NIL1)
                dualmap1_1Fijo.m2.add_child(NIL2)
                dualmap1_1Fijo.m2.keep_in_front(NIL2)

                url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
                url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

                FloatImage(url1, bottom=5, left=1).add_to(dualmap1_1Fijo.m1)
                FloatImage(url2, bottom=5, left=53).add_to(dualmap1_1Fijo.m2)

                dualmap1_2Fijo=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                   scrollWheelZoom=True,
                   dragging=True)
                ########
                choropleth3=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df3Fijo,
                    #bins=[0,15,50,75,100,125,150,175,190],
                    columns=['Location', 'Download Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de descarga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_2Fijo.m1)
                #######
                choropleth4=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df4Fijo,
                    #bins=[0,15,50,75,100,125,150,175,190],
                    columns=['Location', 'Download Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de descarga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_2Fijo.m2)
                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth3.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_2Fijo.m1)
                choropleth4.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_2Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_df3Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Download Speed Mbps'],
                        aliases=['Departamento','Velocidad descarga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_df4Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Download Speed Mbps'],
                        aliases=['Departamento','Velocidad descarga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth3._children:
                    if key.startswith('color_map'):
                        del(choropleth3._children[key])
                for key in choropleth4._children:
                    if key.startswith('color_map'):
                        del(choropleth4._children[key])

                dualmap1_2Fijo.m1.add_child(NIL1)
                dualmap1_2Fijo.m1.keep_in_front(NIL1)
                dualmap1_2Fijo.m2.add_child(NIL2)
                dualmap1_2Fijo.m2.keep_in_front(NIL2)

                url3 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
                url4 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")

                FloatImage(url3, bottom=5, left=1).add_to(dualmap1_2Fijo.m1)
                FloatImage(url4, bottom=5, left=53).add_to(dualmap1_2Fijo.m2)
                
                
                col1, col2 ,col3= st.columns(3)
                with col2:
                    st.markdown("<center><b> Velocidad de descarga de Internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
                col1b, col2b ,col3b= st.columns([1,4,1])
    #            with col2b:
                folium_static(dualmap1_1Fijo,width=800) 
                folium_static(dualmap1_2Fijo,width=800)  
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

            with tab3:
                etb=Operadores4Fijo[Operadores4Fijo['Provider']=='ETB'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
                claro=Operadores4Fijo[Operadores4Fijo['Provider']=='Claro'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
                movistar=Operadores4Fijo[Operadores4Fijo['Provider']=='Movistar'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
                tigo=Operadores4Fijo[Operadores4Fijo['Provider']=='Tigo'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]     

                dict_color_periodos={2020:'rgb(213,3,85)',2021:'rgb(255,152,0)',2022:'rgb(44,198,190)',2023:'rgb(72,68,242)'}
                fig5Fijo = make_subplots(rows=2, cols=2,subplot_titles=("<b>ETB</b>",
                    "<b>CLARO</b>","<b>MOVISTAR</b>","<b>TIGO</b>"),vertical_spacing=0.2)  
                for año in [2020,2021,2022,2023]:  
                    fig5Fijo.add_trace(go.Scatter(
                    x=etb[etb['year']==año]['Download Speed Mbps'].values, y=etb[etb['year']==año]['Upload Speed Mbps'].values,showlegend=True, name=año,
                    mode='markers',
                    marker=dict(
                        color=dict_color_periodos[año],
                        opacity=0.7,
                        size=1.5*etb[etb['year']==año]['Latency'].values,
                    ),legendgroup = '1',
                    text=etb[etb['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)

                    fig5Fijo.add_trace(go.Scatter(
                    x=claro[claro['year']==año]['Download Speed Mbps'].values, y=claro[claro['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                    mode='markers',
                    marker=dict(
                        color=dict_color_periodos[año],
                        opacity=0.7,
                        size=1.5*claro[claro['year']==año]['Latency'].values,
                    ),legendgroup = '1',
                    text=claro[claro['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=2)

                    fig5Fijo.add_trace(go.Scatter(
                    x=movistar[movistar['year']==año]['Download Speed Mbps'].values, y=movistar[movistar['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                    mode='markers',
                    marker=dict(
                        color=dict_color_periodos[año],
                        opacity=0.7,
                        size=1.5*movistar[movistar['year']==año]['Latency'].values,
                    ),legendgroup = '1',
                    text=movistar[movistar['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=2, col=1)
                    
                    fig5Fijo.add_trace(go.Scatter(
                    x=tigo[tigo['year']==año]['Download Speed Mbps'].values, y=tigo[tigo['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                    mode='markers',
                    marker=dict(
                        color=dict_color_periodos[año],
                        opacity=0.7,
                        size=1.5*tigo[tigo['year']==año]['Latency'].values,
                    ),legendgroup = '1',
                    text=tigo[tigo['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=2, col=2)    
                    
                fig5Fijo.add_shape(type="line",
                    x0=0, y0=0, x1=170, y1=170,
                    line=dict(
                        color="indianred",
                        width=4,
                        dash="dot",
                    ),row=1,col=1)
                fig5Fijo.add_shape(type="line",
                    x0=0, y0=0, x1=170, y1=170,
                    line=dict(
                        color="indianred",
                        width=4,
                        dash="dot",
                    ),row=1,col=2)
                fig5Fijo.add_shape(type="line",
                    x0=0, y0=0, x1=170, y1=170,
                    line=dict(
                        color="indianred",
                        width=4,
                        dash="dot",
                    ),row=2,col=1)
                fig5Fijo.add_shape(type="line",
                    x0=0, y0=0, x1=170, y1=170,
                    line=dict(
                        color="indianred",
                        width=4,
                        dash="dot",
                    ),row=2,col=2)
                ###################################


                fig5Fijo.update_xaxes(range=[0,170],tickangle=0,tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig5Fijo.update_yaxes(range=[0,170],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18,ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig5Fijo.update_traces(textfont_size=18)
                fig5Fijo.update_layout(height=700,legend_title=None)
                fig5Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
                fig5Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
                title={
                'text': "<b> Diagrama de burbujas de índices de desempeño de Internet fijo por operador</b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig5Fijo.update_xaxes(row=1, col=1,title_text=None)
                fig5Fijo.update_yaxes(row=1, col=2,title_text=None)
                fig5Fijo.update_yaxes(row=2, col=2,title_text=None)
                fig5Fijo.update_xaxes(row=1, col=2,title_text=None)
                fig5Fijo.update_xaxes(row=2, col=1,title_text='Velocidad de descarga (Mbps)')
                fig5Fijo.update_xaxes(row=2, col=2,title_text='Velocidad de descarga (Mbps)')
                fig5Fijo.update_yaxes(title_text="Velocidad de carga (Mbps)", row=1, col=1)
                fig5Fijo.update_yaxes(title_text="Velocidad de carga (Mbps)", row=2, col=1)
                fig5Fijo.update_layout(legend=dict(yanchor="top",y=1,xanchor="left",x=0.01))
                fig5Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-1.9)             
                st.plotly_chart(fig5Fijo, use_container_width=True)  

    if select_indicador== 'Velocidad de carga':
        dimension_Vel_carga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_carga_Fijo == 'Histórico Colombia':
            tab1,tab2=st.tabs(["Evolución indicador","Mapa departamental"])
            
            Upspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            Upspeed1Fijo['Aggregate Date']=Upspeed1Fijo['Aggregate Date'].astype('str')
            with tab1:
                fig6Fijo = make_subplots(rows=1, cols=1)
                fig6Fijo.add_trace(go.Scatter(x=Upspeed1Fijo['Aggregate Date'].values, y=Upspeed1Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='red', width=2),mode='lines+markers',fill='tonexty', fillcolor='rgba(255,0,0,0.2)'),row=1, col=1)
                fig6Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01',
                '2021-06-01','2021-12-01','2022-06-01','2022-12-01','2023-06-01'])
                fig6Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig6Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad carga<br>(Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig6Fijo.update_traces(textfont_size=18)
                fig6Fijo.update_layout(height=500,legend_title=None)
                #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                fig6Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                fig6Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
                title={
                'text': "<b>Velocidad mensual de carga de Internet fijo en Colombia (2018-2023/1S) (en Mbps)</b>",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig6Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2023/1S.',
                font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
                st.plotly_chart(fig6Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Upspeed1Fijo),file_name='Historico_carga_Colombia.csv',mime='text/csv')
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo]    

                Col2bFijo=Colombia2Fijo[(Colombia2Fijo['year']==año_opFijo)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Upload Speed Mbps'].mean()
                Col2bFijo=round(Col2bFijo,2)
                departamentos_df2bFijo=gdf2.merge(Col2bFijo, on='Location')
                departamentos_df2bFijo=departamentos_df2bFijo.sort_values(by='Upload Speed Mbps')  
                
                if departamentos_df2bFijo.empty==True:
                    st.markdown('No se presentan datos para el mes seleccionado.')
                else:
                    colombia_map2Fijo = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                       scrollWheelZoom=True,
                       dragging=True)
                    tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                    for tile in tiles:
                        folium.TileLayer(tile).add_to(colombia_map2Fijo)
                    choropleth=folium.Choropleth(
                        geo_data=Colombian_DPTO2,
                        data=departamentos_df2bFijo,
                        #bins=[0,5,15,25,35,45,55,70],
                        columns=['Location', 'Upload Speed Mbps'],
                        key_on='feature.properties.NOMBRE_DPT',
                        fill_color='YlGnBu', 
                        fill_opacity=0.9, 
                        line_opacity=0.9,
                        legend_name='Velocidad de carga (Mbps)',
                        nan_fill_color = "black",
                        smooth_factor=0).add_to(colombia_map2Fijo)
                    # Adicionar nombres del departamento
                    style_function = "font-size: 15px; font-weight: bold"
                    choropleth.geojson.add_child(
                        folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
                    folium.LayerControl().add_to(colombia_map2Fijo)

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
                        data = departamentos_df2bFijo,
                        style_function=style_function, 
                        control=False,
                        highlight_function=highlight_function, 
                        tooltip=folium.features.GeoJsonTooltip(
                            fields=['Location','Upload Speed Mbps'],
                            aliases=['Departamento','Velocidad de carga'],
                            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                        )
                    )
                    for key in choropleth._children:
                        if key.startswith('color_map'):
                            del(choropleth._children[key])            
                    colombia_map2Fijo.add_child(NIL)
                    colombia_map2Fijo.keep_in_front(NIL)
                    
                    col1b, col2b ,col3b= st.columns([1,4,1])
                    with col2b:
                        st.markdown("<b><center>Velocidad de carga de Internet fijo en Colombia<br>por departamento (en Mbps)</center></b>",unsafe_allow_html=True)                        
                        folium_static(colombia_map2Fijo,width=480) 
                        st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Fijo == 'Ciudades':    
            tab1,tab2=st.tabs(["Comparación anual","Información por operadores"])
            with tab1:
                col1, col2,col3= st.columns(3)
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                df19B3=pd.DataFrame();df20B3=pd.DataFrame();df21B3=pd.DataFrame();df22B3=pd.DataFrame();df23B3=pd.DataFrame()
                p19B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
                p20B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
                p21B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
                p22B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
                p23B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2023)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
                df19B3['Location']=p19B3.index;df19B3['2019']=p19B3.values;
                df20B3['Location']=p20B3.index;df20B3['2020']=p20B3.values;
                df21B3['Location']=p21B3.index;df21B3['2021']=p21B3.values;
                df22B3['Location']=p22B3.index;df22B3['2022']=p22B3.values;
                df23B3['Location']=p23B3.index;df23B3['2023']=p23B3.values;
                from functools import reduce
                DepJoinB3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19B3,df20B3,df21B3,df22B3,df23B3]).set_index('Location')
                DepJoinB3=DepJoinB3.round(2).reset_index()
                DepJoinB3 = DepJoinB3[DepJoinB3.Location != 'Colombia']
                DepJoinB3 = DepJoinB3.sort_values(by=['2023'],ascending=False)
                DepJoinB3['relatGrow']=100*(DepJoinB3['2023']-DepJoinB3['2022'])/DepJoinB3['2022']
                DepJoinB3['absGrow']=DepJoinB3['2023']-DepJoinB3['2022']
                DepJoinBcopy3=DepJoinB3.copy()
                DepJoinBcopy3['2019']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2019'],1).astype(str)]
                DepJoinBcopy3['2020']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2020'],1).astype(str)]
                DepJoinBcopy3['2021']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2021'],1).astype(str)]
                DepJoinBcopy3['2022']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2022'],1).astype(str)]
                DepJoinBcopy3['2023']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2023'],1).astype(str)]
                name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
                
                fig7Fijo = go.Figure()
                fig7Fijo.add_trace(go.Bar(
                    x=DepJoinB3['Location'],
                    y=DepJoinB3['2020'],
                    name=mes_opFijo+' 2020',
                    marker_color='rgb(213,3,85)'))
                fig7Fijo.add_trace(go.Bar(
                    x=DepJoinB3['Location'],
                    y=DepJoinB3['2021'],
                    name=mes_opFijo+' 2021',
                    marker_color='rgb(255,152,0)'))
                fig7Fijo.add_trace(go.Bar(
                    x=DepJoinB3['Location'],
                    y=DepJoinB3['2022'],
                    name=mes_opFijo+' 2022',
                    marker_color='rgb(44,198,190)'))
                fig7Fijo.add_trace(go.Bar(
                    x=DepJoinB3['Location'],
                    y=DepJoinB3['2023'],
                    name=mes_opFijo+' 2023',
                    marker_color='rgb(72,68,242)'))

                fig7Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig7Fijo.update_yaxes(range=[0,max(DepJoinB3['2023'].values.tolist())+5],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Velocidad carga promedio (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig7Fijo.update_traces(textfont_size=22)
                fig7Fijo.update_layout(height=600,width=1200,legend_title=None)
                fig7Fijo.update_layout(legend=dict(orientation="h",y=1.1,xanchor='center',x=0.5))
                fig7Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig7Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,font=dict(size=18),
                title={
                'text': "<b>Velocidad anual de carga de Internet fijo por ciudad<br> (2020-2023/1S)</b>",
                'y':0.95,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig7Fijo.update_layout(barmode='group')
                fig7Fijo.update_layout(uniformtext_minsize=22, uniformtext_mode='show')
                fig7Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2020 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='x domain',x=0.1,yref='y domain',y=-0.5)             
                st.plotly_chart(fig7Fijo, use_container_width=True)  
            
            with tab2:    
                select_capdep=st.selectbox('Escoja la ciudad capital de departamento',CapDep,4)
                datamuni2023_cap=datamuni2023[(datamuni2023['DESC_MUNICIPIO']==select_capdep)].sort_values(by='aggregate_date')

                fig_muniOp=go.Figure()
                for op in datamuni2023_cap['provider'].unique():
                    if op not in dict_colores_op.keys():
                        color_op='rgb(192,192,192)'
                    else:
                        color_op=dict_colores_op[op]
                    df_muniOp=datamuni2023_cap[datamuni2023_cap['provider']==op]
                    fig_muniOp.add_trace(go.Scatter(x=df_muniOp['aggregate_date'],y=df_muniOp['median_upload_mbps'],mode='lines+markers',name=op,marker_color=color_op
                    ))
                    
                    fig_muniOp.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                    fig_muniOp.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                    fig_muniOp.update_traces(textfont_size=18)
                    fig_muniOp.update_layout(height=500,legend_title=None,font=dict(size=18))
                    fig_muniOp.update_layout(legend=dict(orientation="h",y=1.1,x=0.35),showlegend=True)
                    fig_muniOp.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                    fig_muniOp.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,
                    title={
                    'text': f"<b>Velocidad mensual de carga de Internet fijo por proveedor ({select_capdep}) </b>",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})  
                    fig_muniOp.update_xaxes(tickvals=['2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01'])
                    fig_muniOp.add_annotation(
                    showarrow=False,
                    text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                    font=dict(size=10), xref='paper',yref='y domain',y=-0.25)                     
                st.plotly_chart(fig_muniOp, use_container_width=True)     
            
        if dimension_Vel_carga_Fijo == 'Operadores':   
            TodosCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            TodosCarga4Fijo['Aggregate Date']=TodosCarga4Fijo['Aggregate Date'].astype('str')
            ETBCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            ETBCarga4Fijo['Aggregate Date']=ETBCarga4Fijo['Aggregate Date'].astype('str')
            MOVISTARCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            MOVISTARCarga4Fijo['Aggregate Date']=MOVISTARCarga4Fijo['Aggregate Date'].astype('str')
            CLAROCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            CLAROCarga4Fijo['Aggregate Date']=CLAROCarga4Fijo['Aggregate Date'].astype('str')
            TIGOCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index() 
            TIGOCarga4Fijo['Aggregate Date']=TIGOCarga4Fijo['Aggregate Date'].astype('str')            

            JuntosCarga4Fijo=pd.concat([TodosCarga4Fijo,ETBCarga4Fijo,MOVISTARCarga4Fijo,CLAROCarga4Fijo,TIGOCarga4Fijo])
            
            tab1,tab2=st.tabs(["Evolución indicador","Mapa departamental"])
            with tab1:            
                fig8Fijo = make_subplots(rows=1, cols=1)
                fig8Fijo.add_trace(go.Scatter(x=TodosCarga4Fijo['Aggregate Date'].values, y=TodosCarga4Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='black', width=1, dash='dash'),mode='lines',name='Colombia'),row=1, col=1)
                fig8Fijo.add_trace(go.Scatter(x=ETBCarga4Fijo['Aggregate Date'].values, y=ETBCarga4Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='rgb(0,153,153)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(0,153,153)',width=1)),mode='lines+markers',name='ETB'),row=1, col=1)
                fig8Fijo.add_trace(go.Scatter(x=MOVISTARCarga4Fijo['Aggregate Date'].values, y=MOVISTARCarga4Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='rgb(51,255,51)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(51,255,51)',width=1)),mode='lines+markers',name='Movistar'),row=1, col=1)
                fig8Fijo.add_trace(go.Scatter(x=CLAROCarga4Fijo['Aggregate Date'].values, y=CLAROCarga4Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='red', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='red',width=1)),mode='lines+markers',name='Claro'),row=1, col=1)
                fig8Fijo.add_trace(go.Scatter(x=TIGOCarga4Fijo['Aggregate Date'].values, y=TIGOCarga4Fijo['Upload Speed Mbps'].values,
                                         line=dict(color='rgb(153,51,255)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(153,51,255)',width=1)),mode='lines+markers',name='Tigo'),row=1, col=1)

                fig8Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig8Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig8Fijo.update_traces(textfont_size=14)
                fig8Fijo.update_layout(height=500,legend_title=None,font=dict(size=18))
                fig8Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.01),showlegend=True)
                fig8Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig8Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
                title={
                'text': "<b>Velocidad mensual de carga de Internet fijo<br>por proveedor (2018-2023/1S) (en Mbps)</b>",
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig8Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01',
                '2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01',
                '2022-03-01','2022-06-01','2022-09-01','2022-12-01','2023-03-01','2023-06-01'])
                fig8Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
                st.plotly_chart(fig8Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosCarga4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')            
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                final_dfAncFijo=gdf2.merge(OpCiud2Fijo.groupby(['Location'])['Upload Speed Mbps'].median().reset_index(), on='Location')
                final_dfAncFijo['Upload Speed Mbps']=np.nan

                Proveedor1bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor1bFijo['Upload Speed Mbps'] =round(Proveedor1bFijo['Upload Speed Mbps'], 2)
                if Proveedor1bFijo.empty==True:
                    final_df1bFijo=final_dfAncFijo
                else: 
                    final_df1bFijo=gdf2.merge(Proveedor1bFijo, on='Location')
                ##
                Proveedor2bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor2bFijo['Upload Speed Mbps'] =round(Proveedor2bFijo['Upload Speed Mbps'], 2)
                if Proveedor2bFijo.empty==True:
                    final_df2bFijo=final_dfAncFijo
                else: 
                    final_df2bFijo=gdf2.merge(Proveedor2bFijo, on='Location')
                ##
                Proveedor3bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor3bFijo['Upload Speed Mbps'] =round(Proveedor3bFijo['Upload Speed Mbps'], 2)
                if Proveedor3bFijo.empty==True:
                    final_df3bFijo=final_dfAncFijo
                else: 
                    final_df3bFijo=gdf2.merge(Proveedor3bFijo, on='Location')
                ##
                Proveedor4bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor4bFijo['Upload Speed Mbps'] =round(Proveedor4bFijo['Upload Speed Mbps'], 2)
                if Proveedor4bFijo.empty==True:
                    final_df4bFijo=final_dfAncFijo
                else: 
                    final_df4bFijo=gdf2.merge(Proveedor4bFijo, on='Location') 


                dualmap1_3Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
                ########
                choropleth1=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df1bFijo,
                    #bins=[0,5,15,25,50,75,100,125,150,200],
                    columns=['Location', 'Upload Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de carga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_3Fijo.m1)
                #######
                choropleth2=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df2bFijo,
                    #bins=[0,5,15,25,50,75,100,125,150,200],
                    columns=['Location', 'Upload Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de carga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_3Fijo.m2)
                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth1.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_3Fijo.m1)
                choropleth2.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_3Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_df1bFijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Upload Speed Mbps'],
                        aliases=['Departamento','Velocidad carga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_df2bFijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Upload Speed Mbps'],
                        aliases=['Departamento','Velocidad carga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth1._children:
                    if key.startswith('color_map'):
                        del(choropleth1._children[key])
                for key in choropleth2._children:
                    if key.startswith('color_map'):
                        del(choropleth2._children[key])

                dualmap1_3Fijo.m1.add_child(NIL1)
                dualmap1_3Fijo.m1.keep_in_front(NIL1)
                dualmap1_3Fijo.m2.add_child(NIL2)
                dualmap1_3Fijo.m2.keep_in_front(NIL2)

                url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
                url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

                FloatImage(url1, bottom=5, left=1).add_to(dualmap1_3Fijo.m1)
                FloatImage(url2, bottom=5, left=53).add_to(dualmap1_3Fijo.m2)

                dualmap1_4Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
                ########
                choropleth3=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df3bFijo,
                    #bins=[0,5,15,25,50,75,100,125,150,190],
                    columns=['Location', 'Upload Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de carga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_4Fijo.m1)
                #######
                choropleth4=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_df4bFijo,
                    #bins=[0,5,15,25,50,75,100,125,150,190],
                    columns=['Location', 'Upload Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de carga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_4Fijo.m2)
                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth3.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_4Fijo.m1)
                choropleth4.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_4Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_df3bFijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Upload Speed Mbps'],
                        aliases=['Departamento','Velocidad carga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_df4bFijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Upload Speed Mbps'],
                        aliases=['Departamento','Velocidad carga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth3._children:
                    if key.startswith('color_map'):
                        del(choropleth3._children[key])
                for key in choropleth4._children:
                    if key.startswith('color_map'):
                        del(choropleth4._children[key])

                dualmap1_4Fijo.m1.add_child(NIL1)
                dualmap1_4Fijo.m1.keep_in_front(NIL1)
                dualmap1_4Fijo.m2.add_child(NIL2)
                dualmap1_4Fijo.m2.keep_in_front(NIL2)

                url3 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
                url4 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")

                FloatImage(url3, bottom=5, left=1).add_to(dualmap1_4Fijo.m1)
                FloatImage(url4, bottom=5, left=53).add_to(dualmap1_4Fijo.m2)


                col1, col2 ,col3= st.columns(3)
                with col2:
                    st.markdown("<center><b> Velocidad de carga de Internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
                col1b, col2b ,col3b= st.columns([1,4,1])
                with col2b:
                    folium_static(dualmap1_3Fijo,width=800) 
                    folium_static(dualmap1_4Fijo,width=800)  
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)
                     
    if select_indicador== 'Latencia':            
        dimension_Latencia_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Latencia_Fijo == 'Histórico Colombia':    
            Latency1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            Latency1Fijo['Aggregate Date']=Latency1Fijo['Aggregate Date'].astype('str')
            tab1,tab2=st.tabs(["Evolución indicador","Mapa departamental"])
            with tab1:
                fig9Fijo = make_subplots(rows=1, cols=1)
                fig9Fijo.add_trace(go.Scatter(x=Latency1Fijo['Aggregate Date'].values, y=Latency1Fijo['Latency'].values,
                             line=dict(color='purple', width=2),mode='lines+markers',fill='tonexty', fillcolor='rgba(153,0,153,0.2)'),row=1, col=1)
                fig9Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig9Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig9Fijo.update_traces(textfont_size=18)
                fig9Fijo.update_layout(height=500,legend_title=None)
                #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                fig9Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
                fig9Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
                title={
                'text': "<b>Latencia mensual de Internet fijo en Colombia<br>(2018-2023/1S)</b>",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig9Fijo.update_xaxes(tickvals=['2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01',
                '2022-06-01','2022-12-01','2023-06-01'])
                fig9Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2023/1S.',
                font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
                st.plotly_chart(fig9Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Latency1Fijo),file_name='Historico_latencia_Colombia.csv',mime='text/csv')             
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo]    
                    
                Servidores=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Fijo/Fij-Servidores_Colombia.csv',encoding='latin-1',delimiter=';')
                Servidores['latitude']=Servidores['latitude'].str.replace(',','.')
                Servidores['longitude']=Servidores['longitude'].str.replace(',','.')
                ColLat2=Colombia2Fijo[(Colombia2Fijo['year']==2023)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Latency'].mean()
                ColLat2=round(ColLat2,2)
                departamentosLat_df2Fijo=gdf2.merge(ColLat2, on='Location')
                departamentosLat_df2Fijo=departamentosLat_df2Fijo.sort_values(by='Latency')
                
                if departamentosLat_df2Fijo.empty==True:
                    st.markdown('No se presentan datos para el mes seleccionado.')
                else:
                
                    colombia_map3Fijo = folium.Map(height=600,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                       scrollWheelZoom=True,
                       dragging=True)
                    tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                    for tile in tiles:
                        folium.TileLayer(tile).add_to(colombia_map3Fijo)
                    choropleth=folium.Choropleth(
                        geo_data=Colombian_DPTO2,
                        data=departamentosLat_df2Fijo,
                        #bins=[10,20,30,50,75],
                        columns=['Location', 'Latency'],
                        key_on='feature.properties.NOMBRE_DPT',
                        fill_color='YlGnBu', 
                        fill_opacity=0.9, 
                        line_opacity=0.9,
                        legend_name='Latencia (ms)',
                        nan_fill_color = "black",
                        smooth_factor=0).add_to(colombia_map3Fijo)
                    # Adicionar nombres del departamento
                    style_function = "font-size: 15px; font-weight: bold"
                    choropleth.geojson.add_child(
                        folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
                    folium.LayerControl().add_to(colombia_map3Fijo)

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
                        data = departamentosLat_df2Fijo,
                        style_function=style_function, 
                        control=False,
                        highlight_function=highlight_function, 
                        tooltip=folium.features.GeoJsonTooltip(
                            fields=['Location','Latency'],
                            aliases=['Departamento','Latencia'],
                            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                        )
                    )
                    colombia_map3Fijo.add_child(NIL)
                    colombia_map3Fijo.keep_in_front(NIL)
                    # add marker one by one on the map
                    for i in range(0,len(Servidores)):
                       folium.Marker(
                          location=[Servidores.iloc[i]['latitude'], Servidores.iloc[i]['longitude']],
                          popup=Servidores.iloc[i]['server_name'],icon=folium.Icon(color='red', icon='wifi', prefix='fa'),radius=3,
                     color='red',
                     fill=True,
                     fill_color='red',
                     fill_opacity=1
                       ).add_to(colombia_map3Fijo)
                    for key in choropleth._children:
                        if key.startswith('color_map'):
                            del(choropleth._children[key])
                           
                    col1b, col2b ,col3b= st.columns([1,4,1])
                    with col2b:
                        st.markdown("<center><b>Latencia de Internet fijo en Colombia<br>por departamento (en Mbps)</b></center>",unsafe_allow_html=True) 
                        folium_static(colombia_map3Fijo,width=480) 
                        st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022.<br> Los puntos rojos indican la posición de los servidores de prueba en 2021.</i></p> """,unsafe_allow_html=True)

        if dimension_Latencia_Fijo == 'Ciudades':    
            tab1,tab2=st.tabs(["Comparación anual","Información por operadores"])
            with tab1:   
                col1, col2,col3= st.columns(3)
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                df19C3=pd.DataFrame();df20C3=pd.DataFrame();df21C3=pd.DataFrame();df22C3=pd.DataFrame();df23C3=pd.DataFrame()
                p19C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
                p20C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
                p21C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
                p22C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
                p23C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2023)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
                df19C3['Location']=p19C3.index;df19C3['2019']=p19C3.values;
                df20C3['Location']=p20C3.index;df20C3['2020']=p20C3.values;
                df21C3['Location']=p21C3.index;df21C3['2021']=p21C3.values;
                df22C3['Location']=p22C3.index;df22C3['2022']=p22C3.values;
                df23C3['Location']=p23C3.index;df23C3['2023']=p23C3.values;
                from functools import reduce
                DepJoinC3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19C3,df20C3,df21C3,df22C3,df23C3]).set_index('Location')
                DepJoinC3=DepJoinC3.round(2).reset_index()
                DepJoinC3 = DepJoinC3[DepJoinC3.Location != 'Colombia']
                DepJoinC3 = DepJoinC3.sort_values(by=['2023'],ascending=True)
                DepJoinC3['relatGrow']=100*(DepJoinC3['2023']-DepJoinC3['2022'])/DepJoinC3['2022']
                DepJoinC3['absGrow']=DepJoinC3['2023']-DepJoinC3['2022']
                name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}            
                fig10Fijo = go.Figure()
                fig10Fijo.add_trace(go.Bar(
                    x=DepJoinC3['Location'],
                    y=DepJoinC3['2020'],
                    name=mes_opFijo+' 2020',
                    marker_color='rgb(213,3,85)'))
                fig10Fijo.add_trace(go.Bar(
                    x=DepJoinC3['Location'],
                    y=DepJoinC3['2021'],
                    name=mes_opFijo+' 2021',
                    marker_color='rgb(255,152,0)'))
                fig10Fijo.add_trace(go.Bar(
                    x=DepJoinC3['Location'],
                    y=DepJoinC3['2022'],
                    name=mes_opFijo+' 2022',
                    marker_color='rgb(44,198,190)'))
                fig10Fijo.add_trace(go.Bar(
                    x=DepJoinC3['Location'],
                    y=DepJoinC3['2023'],
                    name=mes_opFijo+' 2023',
                    marker_color='rgb(72,68,242)'))


                fig10Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig10Fijo.update_yaxes(range=[0,100],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Latencia (ms)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig10Fijo.update_traces(textfont_size=22)
                fig10Fijo.update_layout(height=600,width=1200,legend_title=None)
                fig10Fijo.update_layout(legend=dict(orientation="h",y=1,xanchor='center',x=0.5))
                fig10Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig10Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,font=dict(size=18),
                title={
                'text': "<b>Latencia anual de Internet fijo por ciudad en ms<br> (2019-2023/1S) </b>",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig10Fijo.update_layout(barmode='group')
                fig10Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='x domain',x=0.1,yref='y domain',y=-0.5)                 
                st.plotly_chart(fig10Fijo, use_container_width=True)  

            with tab2:    
                select_capdep=st.selectbox('Escoja la ciudad capital de departamento',CapDep,4)
                datamuni2023_cap=datamuni2023[(datamuni2023['DESC_MUNICIPIO']==select_capdep)].sort_values(by='aggregate_date')

                fig_muniOp=go.Figure()
                for op in datamuni2023_cap['provider'].unique():
                    if op not in dict_colores_op.keys():
                        color_op='rgb(192,192,192)'
                    else:
                        color_op=dict_colores_op[op]
                    df_muniOp=datamuni2023_cap[datamuni2023_cap['provider']==op]
                    fig_muniOp.add_trace(go.Scatter(x=df_muniOp['aggregate_date'],y=df_muniOp['median_latency_ms'],mode='lines+markers',name=op,marker_color=color_op
                    ))
                    
                    fig_muniOp.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                    fig_muniOp.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                    fig_muniOp.update_traces(textfont_size=18)
                    fig_muniOp.update_layout(height=500,legend_title=None,font=dict(size=18))
                    fig_muniOp.update_layout(legend=dict(orientation="h",y=1.1,x=0.35),showlegend=True)
                    fig_muniOp.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                    fig_muniOp.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,
                    title={
                    'text': f"<b>Latencia mensual de Internet fijo por proveedor ({select_capdep}) </b>",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'})  
                    fig_muniOp.update_xaxes(tickvals=['2023-01-01','2023-02-01','2023-03-01','2023-04-01','2023-05-01','2023-06-01'])
                    fig_muniOp.add_annotation(
                    showarrow=False,
                    text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                    font=dict(size=10), xref='paper',yref='y domain',y=-0.25)                     
                st.plotly_chart(fig_muniOp, use_container_width=True)

        if dimension_Latencia_Fijo == 'Operadores':  
            TodosLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            TodosLatencia4Fijo['Aggregate Date']=TodosLatencia4Fijo['Aggregate Date'].astype('str')
            ETBLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            ETBLatencia4Fijo['Aggregate Date']=ETBLatencia4Fijo['Aggregate Date'].astype('str')
            MOVISTARLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            MOVISTARLatencia4Fijo['Aggregate Date']=MOVISTARLatencia4Fijo['Aggregate Date'].astype('str')
            CLAROLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            CLAROLatencia4Fijo['Aggregate Date']=CLAROLatencia4Fijo['Aggregate Date'].astype('str')
            TIGOLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            TIGOLatencia4Fijo['Aggregate Date']=TIGOLatencia4Fijo['Aggregate Date'].astype('str')
            
            JuntosLatencia4Fijo=pd.concat([TodosLatencia4Fijo,ETBLatencia4Fijo,MOVISTARLatencia4Fijo,CLAROLatencia4Fijo,TIGOLatencia4Fijo])
            tab1,tab2=st.tabs(["Evolución indicador","Mapa departamental"])
            with tab1:                        
                fig11Fijo = make_subplots(rows=1, cols=1)
                fig11Fijo.add_trace(go.Scatter(x=TodosLatencia4Fijo['Aggregate Date'].values, y=TodosLatencia4Fijo['Latency'].values,
                                         line=dict(color='black', width=1, dash='dash'),mode='lines',name='Colombia'),row=1, col=1)
                fig11Fijo.add_trace(go.Scatter(x=ETBLatencia4Fijo['Aggregate Date'].values, y=ETBLatencia4Fijo['Latency'].values,
                                         line=dict(color='rgb(0,153,153)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(0,153,153)',width=1)),mode='lines+markers',name='ETB'),row=1, col=1)
                fig11Fijo.add_trace(go.Scatter(x=MOVISTARLatencia4Fijo['Aggregate Date'].values, y=MOVISTARLatencia4Fijo['Latency'].values,
                                         line=dict(color='rgb(51,255,51)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(51,255,51)',width=1)),mode='lines+markers',name='Movistar'),row=1, col=1)
                fig11Fijo.add_trace(go.Scatter(x=CLAROLatencia4Fijo['Aggregate Date'].values, y=CLAROLatencia4Fijo['Latency'].values,
                                         line=dict(color='red', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='red',width=1)),mode='lines+markers',name='Claro'),row=1, col=1)
                fig11Fijo.add_trace(go.Scatter(x=TIGOLatencia4Fijo['Aggregate Date'].values, y=TIGOLatencia4Fijo['Latency'].values,
                                         line=dict(color='rgb(153,51,255)', width=1),marker=dict(
                            color='white',
                            size=4,line=dict(color='rgb(153,51,255)',width=1)),mode='lines+markers',name='Tigo'),row=1, col=1)

                fig11Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
                fig11Fijo.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
                zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
                fig11Fijo.update_traces(textfont_size=14)
                fig11Fijo.update_layout(height=500,legend_title=None,font=dict(size=18))
                fig11Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.87),showlegend=True)
                fig11Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
                fig11Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
                title={
                'text': "<b>Latencia mensual de Internet fijo en Colombia (2018-2022) (en ms)</b>",
                'y':0.85,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})  
                fig11Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01',
                '2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01',
                '2022-03-01','2022-06-01','2022-09-01','2022-12-01','2023-03-01','2023-06-01'])
                fig11Fijo.add_annotation(
                showarrow=False,
                text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2023/1S. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
                font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
                st.plotly_chart(fig11Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosLatencia4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')   
            with tab2:
                col1,col2,col3,col4= st.columns([2,1,1,2])
                mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
                with col2:
                    mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],5) 
                with col3:    
                    año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022,2023],3) 
                mes=mes_opFijoNombre[mes_opFijo] 
                
                final_dfAncFijo=gdf2.merge(OpCiud2Fijo.groupby(['Location'])['Latency'].median().reset_index(), on='Location')
                final_dfAncFijo['Latency']=np.nan

                ProveedorLat1Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                ProveedorLat1Fijo['Latency'] =round(ProveedorLat1Fijo['Latency'], 2)
                if ProveedorLat1Fijo.empty==True:
                    final_dfLat1Fijo=final_dfAncFijo
                else: 
                    final_dfLat1Fijo=gdf2.merge(ProveedorLat1Fijo, on='Location')
                ##
                ProveedorLat2Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                ProveedorLat2Fijo['Latency'] =round(ProveedorLat2Fijo['Latency'], 2)
                if ProveedorLat2Fijo.empty==True:
                    final_dfLat2Fijo=final_dfAncFijo
                else: 
                    final_dfLat2Fijo=gdf2.merge(ProveedorLat2Fijo, on='Location')
                ##
                ProveedorLat3Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                ProveedorLat3Fijo['Latency'] =round(ProveedorLat3Fijo['Latency'], 2)
                if ProveedorLat3Fijo.empty==True:
                    final_dfLat3Fijo=final_dfAncFijo
                else: 
                    final_dfLat3Fijo=gdf2.merge(ProveedorLat3Fijo, on='Location')
                ##
                ProveedorLat4Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==año_opFijo)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                ProveedorLat4Fijo['Latency'] =round(ProveedorLat4Fijo['Latency'], 2)
                if ProveedorLat4Fijo.empty==True:
                    final_dfLat4Fijo=final_dfAncFijo
                else: 
                    final_dfLat4Fijo=gdf2.merge(ProveedorLat4Fijo, on='Location')
                
                dualmap1_5Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
                ########
                choropleth1=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_dfLat1Fijo,
                    #bins=[5,10,20,30,50,70,90],
                    columns=['Location', 'Latency'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Latencia (ms)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_5Fijo.m1)
                #######
                choropleth2=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_dfLat2Fijo,
                    #bins=[5,10,20,30,50,70,90],
                    columns=['Location', 'Latency'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Latencia (ms)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_5Fijo.m2)
                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth1.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_5Fijo.m1)
                choropleth2.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_5Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_dfLat1Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Latency'],
                        aliases=['Departamento','Latencia'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_dfLat2Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Latency'],
                        aliases=['Departamento','Latencia'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth1._children:
                    if key.startswith('color_map'):
                        del(choropleth1._children[key])
                for key in choropleth2._children:
                    if key.startswith('color_map'):
                        del(choropleth2._children[key])

                dualmap1_5Fijo.m1.add_child(NIL1)
                dualmap1_5Fijo.m1.keep_in_front(NIL1)
                dualmap1_5Fijo.m2.add_child(NIL2)
                dualmap1_5Fijo.m2.keep_in_front(NIL2)

                url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
                url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

                FloatImage(url1, bottom=5, left=1).add_to(dualmap1_5Fijo.m1)
                FloatImage(url2, bottom=5, left=53).add_to(dualmap1_5Fijo.m2)

                dualmap1_6Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
                ########
                choropleth3=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_dfLat3Fijo,
                    #bins=[5,10,20,30,50,70,90],
                    columns=['Location', 'Latency'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Latencia (ms)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_6Fijo.m1)
                #######
                choropleth4=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=final_dfLat4Fijo,
                    #bins=[5,10,20,30,50,70,90],
                    columns=['Location', 'Latency'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Latencia (ms)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(dualmap1_6Fijo.m2)
                #######
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth3.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_6Fijo.m1)
                choropleth4.geojson.add_child(
                    folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
                folium.LayerControl().add_to(dualmap1_6Fijo.m2)
                ##
                #Adicionar valores porcentaje
                style_function = lambda x: {'fillColor': '#ffffff', 
                                            'color':'#000000', 
                                            'fillOpacity': 0.1, 
                                            'weight': 0.1}
                highlight_function = lambda x: {'fillColor': '#000000', 
                                                'color':'#000000', 
                                                'fillOpacity': 0.50, 
                                                'weight': 0.1}
                NIL1 = folium.features.GeoJson(
                    data = final_dfLat3Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Latency'],
                        aliases=['Departamento','Latencia'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                NIL2 = folium.features.GeoJson(
                    data = final_dfLat4Fijo,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Latency'],
                        aliases=['Departamento','Latencia'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                for key in choropleth3._children:
                    if key.startswith('color_map'):
                        del(choropleth3._children[key])
                for key in choropleth4._children:
                    if key.startswith('color_map'):
                        del(choropleth4._children[key])

                dualmap1_6Fijo.m1.add_child(NIL1)
                dualmap1_6Fijo.m1.keep_in_front(NIL1)
                dualmap1_6Fijo.m2.add_child(NIL2)
                dualmap1_6Fijo.m2.keep_in_front(NIL2)

                url3 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
                url4 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")

                FloatImage(url3, bottom=5, left=1).add_to(dualmap1_6Fijo.m1)
                FloatImage(url4, bottom=5, left=53).add_to(dualmap1_6Fijo.m2)

                col1, col2 ,col3= st.columns(3)
                with col2:
                    st.markdown("<center><b> Latencia de Internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
                col1b, col2b ,col3b= st.columns([1,4,1])
                with col2b:
                    folium_static(dualmap1_5Fijo,width=800) 
                    folium_static(dualmap1_6Fijo,width=800)  
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)
 

######################################################### Comparación Internacional #######################################        

fijos_int=pd.read_csv(r'https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2023/Fijo/Ookla_Internacional-FijosAct.csv',delimiter=';')
fijos_int.rename(columns={'Country':'País'},inplace=True)
fijos_int=fijos_int[fijos_int['Date']=='2023-06-01']
fijos_int['País']=fijos_int['País'].str.capitalize()
fijos_int['País']=fijos_int['País'].replace({'United-kingdom':'Reino Unido','Germany':'Alemania','Brazil':'Brasil','South-korea':'Corea del sur','Japan':'Japón',
                                             'United-states':'Estados Unidos','Spain':'España','Canada':'Canadá','Mexico':'México'})

fijo_Intdict = {'Estados Unidos':[192.73,22.57,14],'Uruguay':[94.69,31.9,6],'Colombia':[90.76,32.62,11],
'Venezuela':[15.35,12.28,22],'Ecuador':[46.8,43.02,6],'Peru':[67.57,32.43,9],'Bolivia':[24.71,13.5,8],
'Paraguay':[68.93,26.14,9],'Brasil':[100.95,73.32,6],'Chile':[220.96,131.14,6],'Argentina':[56.13,24.61,12],
'Canadá':[144.5,34.33,11],'México':[49.61,18.79,8],'España':[168.63,114.09,12],'Reino Unido':[71.14,19.67,15],
'Alemania':[80.08,27.15,13],'Japón':[143.33,94.21,13],'Corea del sur':[95.74,94.56,21]}

Fijo_Int=pd.DataFrame.from_dict(fijo_Intdict,orient='index').reset_index()
Fijo_Int=Fijo_Int.rename(columns={'index':'País',0:'Download',1:'Upload',2:'Latency'})
#@st.cache(allow_output_mutation=True)
def gdf_Suramerica():
    gdf_Int = gpd.read_file("https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Suramerica.geo.json")
    gdf_Int=gdf_Int.rename(columns=({'admin':'País'}))
    return gdf_Int
gdf_Int=gdf_Suramerica()
with urllib.request.urlopen("https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Suramerica.geo.json") as url:
    SURAMERICA = json.loads(url.read().decode()) 
Fijo_df=gdf_Int.merge(Fijo_Int, on='País')

dict_coloresPais = {'Estados Unidos':'rgb(51,0,25)','Uruguay':'rgb(255,0,0)','Colombia':'rgb(255,255,0)',
'Venezuela':'rgba(128,255,0,0.3)','Ecuador':'rgb(255,0,255)','Peru':'rgb(0,255,128)','Bolivia':'rgb(255,102,102)',
'Paraguay':'rgb(0,128,255)','Brasil':'rgb(0,51,51)','Chile':'rgb(0,0,255)','Argentina':'rgb(127,0,255)',
'Canadá':'rgb(255,128,0)','México':'rgb(255,128,128)','España':'rgb(192,192,102)','Reino Unido':'rgb(102,102,255)',
'Alemania':'rgb(204,0,0)','Japón':'rgb(255,153,204)','Corea del sur':'rgb(255,204,153)'}

if select_servicio == 'Comparación internacional':
    st.markdown("### Internet fijo",unsafe_allow_html=True)
    fig1Int=make_subplots(rows=1,cols=1)
    for pais in fijos_int['País'].unique().tolist():
        fig1Int.add_trace(go.Scatter(
        x=fijos_int[fijos_int['País']== pais]['Download_speed'].values, y=fijos_int[fijos_int['País']== pais]['Upload_speed'].values, name=pais,
        mode='markers',
        text=fijos_int[fijos_int['País']== pais]['Latency'],
        marker=dict(
            color=dict_coloresPais[pais],
            opacity=1,
            size=2*fijos_int[fijos_int['País']== pais]['Latency']),hovertemplate='<b>País:</b>'+pais+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
    fig1Int.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='tahoma',titlefont_size=18,title_text='Velocidad de descarga (Mbps)',ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
    fig1Int.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='tahoma',titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
    fig1Int.update_traces(textfont_size=16)
    fig1Int.update_layout(height=500,legend_title=None)
    fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    fig1Int.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18)

    fig1Int.update_layout(height=600,   
        title='<b>Diagrama de burbujas de indicadores de desempeño en Internet fijo por país<br>(Junio 2023)',
        title_x=0.5,
        font=dict(
            family="Tahoma",
            color=" black",size=18))
    fig1Int.update_layout(legend=dict(y=1,x=1,font_size=17))
    fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig1Int.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1Int, use_container_width=True) 

