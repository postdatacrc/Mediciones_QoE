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
st.markdown("")
st.markdown("""<p style="text-align:center;"><b>Para hacer uso del tablero interactivo, por favor seleccione el servicio sobre el cual desea conocer la información de los indicadores de calidad</b></p>""", unsafe_allow_html=True)

select_servicio = st.selectbox('Servicio',
                                    ['Información general','Internet fijo','Internet móvil','Comparación internacional'])

if select_servicio=='Información general':
    st.markdown('<p style="text-align:justify;">La Comisión de regulación de comunicaciones presenta la aplicación interactiva que contiene información sobre la calidad de los servicios ofrecidos a través de redes móviles y fijas por los diferentes proveedores en el territorio nacional, para el periodo comprendido entre los años 2018 y 2022. Los valores mostrados en este tablero corresponden a la mediana de las mediciones, debido a que ésta métrica presenta menor sensibilidad frente a valores atípicos de las distribuciones de datos, garantizando la validez de los resultados.</p>',unsafe_allow_html=True)
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
        st.markdown("### Definición indicadores de calidad",unsafe_allow_html=True)
        st.markdown('<p style="text-align:justify;">Los indicadores de calidad pueden ser divididos en 2 categorías: Indicadores de desempeño, e Indicadores de cobertura. A continuación se da paso a las definiciones de cada uno, y su relación con el servicio que experimenta el usuario.</p>',unsafe_allow_html=True)
        select_indicadorDef=st.selectbox('Escoja la categoría',['Indicadores de desempeño','Indicadores de cobertura'])
        if select_indicadorDef=='Indicadores de desempeño': 
            st.markdown("#### Indicadores de desempeño")
            st.markdown('<p style="text-align:justify;">el rendimiento o desempeño del servicio de internet se refiere a los resultados de los indicadores de calidad del servicio de telecomunicaciones desde el punto de vista del usuario. Los más relevantes están relacionados con las velocidades y los tiempos de retardo de las conexiones.</p>',unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["Velocidad de descarga", "Velocidad de carga", "Latencia"])
            with tab1:
                st.markdown('<p style="text-align:justify;">La velocidad de descarga Se entiende como la rapidez con la se pueden descargar contenidos, normalmente desde una página Web. A mayor velocidad obtenida en la medición, mayor rapidez en la descarga, por lo tanto, mejor experiencia del usuario. Es usual medirla en  Megabit por segundo (Mbps)</p>',unsafe_allow_html=True)
            with tab2:
                st.markdown('<p style="text-align:justify;">La velocidad de carga se entiende como la medida de qué tan rápido se envían los datos en dirección desde un dispositivo hacia Internet. Es decir, es la rapidez con la que se pueden subir contenidos a Internet. A mayor velocidad obtenida en la medición, mayor rapidez en la carga, por lo tanto, mejor es la experiencia del usuario. Se mide en Mebagit por segundo (Mbps)</p>',unsafe_allow_html=True)
            with tab3:
                st.markdown('<p style="text-align:justify;">El parámetro de latencia sirve para medir qué tan rápido viajan los datos desde un punto de origen al destino. La experiencia al intentar acceder a audio, video y videojuegos es mejor con latencias más bajas, por lo cual, si el tiempo obtenido en la medición es pequeño, la experiencia del usuario es mejor. La latencia se mide en milisegundos (ms).</p>',unsafe_allow_html=True)
        if select_indicadorDef=='Indicadores de cobertura':
            st.markdown("#### Indicadores de cobertura")
            st.markdown('<p style="text-align:justify;">se refiere a indicadores relacionados con la distribución geográfica de los servicios de un operador móvil</p>',unsafe_allow_html=True)
            with st.expander("Registro en red"):
                st.markdown('<p style="text-align:justify;">Es una métrica que indica la proporción del registro de los dispositivos de los usuarios en la red móvil de acuerdo con la tecnología de esta (para este documento incluye 2G, 3G, 4G y Roaming Automático Nacional - RAN).</p>',unsafe_allow_html=True)
            with st.expander("Registro en red 4G"):
                st.markdown('<p style="text-align:justify;">Este indicador se refiere al porcentaje de usuarios que se registraron en las redes que suministran servicios móviles solamente en la tecnología 4G (incluido el Roaming Automático Nacional - RAN).</p>',unsafe_allow_html=True)






        
#################################Lectura de bases Internet fijo#######################################33
pathFijo2='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2022/Mediana/Internet_fijo/'
#pathFijo=r'C:\Users\santiago.bermudez\COMISION DE REGULACIÓN DE COMUNICACIONES\Mediciones Calidad QoE - Documents\Datos\Internet fijo\Mediana\\'
periodo_tope='2022-12-01'

####Primera sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion1Fijo():
    Colombia1Fijo=pd.read_csv(pathFijo2+"Colombia-histcomp_month_2018-2022(Med).csv", delimiter=';')
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
    df2_1Fijo=pd.read_csv(pathFijo2+'ETBMOVCLA-histcomp_month_2018-2022(Med).csv',delimiter=';',encoding='utf-8-sig').dropna(how='all') 
    df2_2Fijo=pd.read_csv(pathFijo2+'TIGOEMCALI-histcomp_month_2018-2022(Med).csv',delimiter=';',encoding='utf-8-sig').dropna(how='all') 
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


####Tercera sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion3Fijo():
    df3_1Fijo=pd.read_csv(pathFijo2+'Ciud(1-10)histcomp_month_2018-2022(Med).csv',delimiter=';',encoding='utf-8-sig')
    df3_2Fijo=pd.read_csv(pathFijo2+'Ciud(11-17)histcomp_month_2018-2022(Med).csv',delimiter=';',encoding='utf-8-sig')
    df3_3Fijo=pd.read_csv(pathFijo2+'Ciud(18-24)histcomp_month_2018-2022(Med).csv',delimiter=';',encoding='utf-8-sig')
    Ciudades3Fijo=pd.concat([df3_1Fijo,df3_2Fijo,df3_3Fijo])#Unir los dataframes
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


####Cuarta sección - Fijo
#@st.cache(allow_output_mutation=True)
def Seccion4Fijo():
    Operadores4Fijo=pd.read_csv(pathFijo2+'Op-histcomp_month_2018-2022(Med).csv',delimiter=';')
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

Colombia2Fijo=pd.read_csv(pathFijo2+'Allproviders-histcomp_month_2020-2022(Med).csv',delimiter=';')
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




if select_servicio == 'Internet fijo':
    select_indicador=st.selectbox('Indicador de desempeño',['Velocidad de descarga','Velocidad de carga','Latencia'])
    
    if select_indicador== 'Velocidad de descarga':
        dimension_Vel_descarga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_descarga_Fijo == 'Histórico Colombia':

            
            Downspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Download Speed Mbps'].mean().round(2).reset_index()
            Downspeed1Fijo['Aggregate Date']=Downspeed1Fijo['Aggregate Date'].astype('str')
            
            fig1Fijo = make_subplots(rows=1, cols=1)
            fig1Fijo.add_trace(go.Scatter(x=Downspeed1Fijo['Aggregate Date'].values, y=Downspeed1Fijo['Download Speed Mbps'].values,
                                     line=dict(color='blue', width=2),name=' ',mode='lines+markers',fill='tonexty', fillcolor='rgba(0,0,255,0.2)'),row=1, col=1)
            fig1Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01','2022-06-01','2022-12-01'])
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
            'text': "<b>Velocidad mensual de descarga de Internet fijo en <br>Colombia (2018-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig1Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig1Fijo, use_container_width=True)
            #st.download_button(label="Descargar CSV",data=convert_df(Downspeed1Fijo),file_name='Historico_descarga_Colombia.csv',mime='text/csv')


            ##
            
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
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
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)
                
        if dimension_Vel_descarga_Fijo == 'Ciudades':    
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]     
            
            df19A3Fijo=pd.DataFrame();df20A3Fijo=pd.DataFrame();df21A3Fijo=pd.DataFrame();df22A3Fijo=pd.DataFrame()
            p19A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p20A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p21A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p22A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            df19A3Fijo['Location']=p19A3Fijo.index;df19A3Fijo['2019']=p19A3Fijo.values;
            df20A3Fijo['Location']=p20A3Fijo.index;df20A3Fijo['2020']=p20A3Fijo.values;
            df21A3Fijo['Location']=p21A3Fijo.index;df21A3Fijo['2021']=p21A3Fijo.values;
            df22A3Fijo['Location']=p22A3Fijo.index;df22A3Fijo['2022']=p22A3Fijo.values;
            from functools import reduce
            DepJoinA3Fijo=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19A3Fijo,df20A3Fijo,df21A3Fijo,df22A3Fijo]).set_index('Location')
            DepJoinA3Fijo=DepJoinA3Fijo.round(2).reset_index()
            DepJoinA3Fijo=DepJoinA3Fijo[DepJoinA3Fijo.Location != 'Colombia']
            DepJoinA3Fijo=DepJoinA3Fijo.sort_values(by=['2022'],ascending=False)
            DepJoinA3Fijo['relatGrow']=100*np.abs(DepJoinA3Fijo['2022']-DepJoinA3Fijo['2021'])/DepJoinA3Fijo['2021']
            DepJoinA3Fijo['absGrow']=DepJoinA3Fijo['2022']-DepJoinA3Fijo['2021']
            DepJoinA3Fijocopy=DepJoinA3Fijo.copy()
            DepJoinA3Fijocopy['2018']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2019'],1).astype(str)]
            DepJoinA3Fijocopy['2019']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2020'],1).astype(str)]
            DepJoinA3Fijocopy['2020']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2021'],1).astype(str)]
            DepJoinA3Fijocopy['2021']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2022'],1).astype(str)]
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
            
            fig2Fijo =go.Figure()
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2019'],
            name=mes_opFijo+' 2019',
            marker_color='rgb(213,3,85)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2020'],
            name=mes_opFijo+' 2020',
            marker_color='rgb(255,152,0)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2021'],
            name=mes_opFijo+' 2021',
            marker_color='rgb(44,198,190)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2022'],
            name=mes_opFijo+' 2022',
            marker_color='rgb(72,68,242)',textposition = "outside"))
            fig2Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig2Fijo.update_yaxes(range=[0,max(DepJoinA3Fijo['2022'].values.tolist())+5],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Velocidad descarga (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig2Fijo.update_traces(textfont_size=18)
            fig2Fijo.update_layout(height=600,width=1200,legend_title=None)
            fig2Fijo.update_layout(legend=dict(orientation="h",yanchor='top',xanchor='center',x=0.5,y=0.8))
            fig2Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig2Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,font=dict(size=14),
            title={
            'text': "<b>Velocidad anual de descarga de Internet fijo por ciudad<br> (2019-2022) </b>",
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
 
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12} 

            col1, col2= st.columns(2)
            with col1:
                Año_opFijoIz = st.selectbox('Escoja el año para el panel de la izquierda',[2018,2019,2020,2021],index=3)
                Mes_opFijoIz = st.selectbox('Escoja el mes para el panel de la izquierda',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],index=11) 
                mesIz=mes_opFijoNombre[Mes_opFijoIz] 
            with col2:
                Mes_opFijoDer = st.selectbox('Escoja el mes de 2022 para el panel de la derecha',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],index=11)           
                mesDer=mes_opFijoNombre[Mes_opFijoDer]
            name_mes2={1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
            DicIz=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==Año_opFijoIz)&(Ciudades3Fijo['month']==mesIz)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            DicDer=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mesDer)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            DicIzList=DicIz['Location'].unique().tolist()
            DicDerList=DicDer['Location'].unique().tolist()
            if 'Colombia' in DicIzList:
                DicIzList.remove('Colombia')
            if 'Colombia' in DicDerList:
                DicDerList.remove('Colombia')            
            dict_coloresFijo={'Bucaramanga':'rgb(255,128,0)','Bogotá':'rgb(255,0,0)','Cali':'rgb(255,255,0)',
                 'Medellín':'rgb(128,255,0)','Barranquilla':'rgb(0,255,0)','Cartagena':'rgb(0,255,128)',
                 'Villavicencio':'rgb(255,102,102)','Ibagué':'rgb(0,128,255)','Manizales':'rgb(0,0,255)',
                 'Tunja':'rgb(127,0,255)','Pasto':'rgb(255,0,255)','Santa Marta':'rgb(255,0,127)',
                 'Sincelejo':'rgb(128,128,128)','Armenia':'rgb(102,0,0)','Montería':'rgb(0,255,255)',
                 'Pereira':'rgb(0,51,51)','Popayán':'rgb(51,0,25)','Cúcuta': 'rgb(0, 204, 102)','Neiva': 'rgb(255, 102, 0)',
                 'Valledupar': 'rgb(102, 102, 255)','Riohacha': 'rgb(255, 153, 204)','Arauca': 'rgb(0, 153, 153)',
                 'Yopal': 'rgb(255, 204, 0)','Florencia': 'rgb(153, 51, 255)'}
            fig4Fijo = make_subplots(rows=1, cols=2,subplot_titles=(Mes_opFijoIz+' '+str(Año_opFijoIz),
            Mes_opFijoDer+" 2022"))

            for location in DicIzList:
                fig4Fijo.add_trace(go.Scatter(
                    x=DicIz[DicIz['Location']==location]['Download Speed Mbps'].values, y=DicIz[DicIz['Location']==location]['Upload Speed Mbps'].values, 
                    mode='markers',
                    marker=dict(
                        color=dict_coloresFijo[location],
                        opacity=0.7,
                        size=DicIz[DicIz['Location']==location]['Latency'].values,
                    ),
                text=DicIz[DicIz['Location']==location]['Latency'].values,showlegend=False,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
                
            for location in DicDerList:
                fig4Fijo.add_trace(go.Scatter(
                    x=DicDer[DicDer['Location']==location]['Download Speed Mbps'].values, y=DicDer[DicDer['Location']==location]['Upload Speed Mbps'].values, name=location,
                    mode='markers',
                    marker=dict(
                        color=dict_coloresFijo[location],
                        opacity=0.7,
                        size=DicDer[DicDer['Location']==location]['Latency'].values,
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
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.16)            
            st.plotly_chart(fig4Fijo, use_container_width=True)
            
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
            'text': "<b>Velocidad mensual de descarga de Internet fijo<br>por proveedor (2018-2022) (en Mbps)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig3Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01',
            '2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01',
            '2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01','2022-03-01','2022-06-01','2022-09-01','2022-12-01'])
            fig3Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
            st.plotly_chart(fig3Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosDescarga4Fijo),file_name='Historico_descarga_Operadores.csv',mime='text/csv')            
            
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
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

           
            etb=Operadores4Fijo[Operadores4Fijo['Provider']=='ETB'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            claro=Operadores4Fijo[Operadores4Fijo['Provider']=='Claro'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            movistar=Operadores4Fijo[Operadores4Fijo['Provider']=='Movistar'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            tigo=Operadores4Fijo[Operadores4Fijo['Provider']=='Tigo'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]     

            dict_color_periodos={2019:'rgb(213,3,85)',2020:'rgb(255,152,0)',2021:'rgb(44,198,190)',2022:'rgb(72,68,242)'}
            fig5Fijo = make_subplots(rows=2, cols=2,subplot_titles=("<b>ETB</b>",
                "<b>CLARO</b>","<b>MOVISTAR</b>","<b>TIGO</b>"),vertical_spacing=0.2)  
            for año in [2019,2020,2021,2022]:  
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
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-1.9)             
            st.plotly_chart(fig5Fijo, use_container_width=True)  

    if select_indicador== 'Velocidad de carga':
        dimension_Vel_carga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_carga_Fijo == 'Histórico Colombia':
            Upspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            Upspeed1Fijo['Aggregate Date']=Upspeed1Fijo['Aggregate Date'].astype('str')
            fig6Fijo = make_subplots(rows=1, cols=1)
            fig6Fijo.add_trace(go.Scatter(x=Upspeed1Fijo['Aggregate Date'].values, y=Upspeed1Fijo['Upload Speed Mbps'].values,
                                     line=dict(color='red', width=2),mode='lines+markers',fill='tonexty', fillcolor='rgba(255,0,0,0.2)'),row=1, col=1)
            fig6Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01',
            '2021-06-01','2021-12-01','2022-06-01','2022-12-01'])
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
            'text': "<b>Velocidad mensual de carga de Internet fijo en Colombia (2018-2022) (en Mbps)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig6Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig6Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Upspeed1Fijo),file_name='Historico_carga_Colombia.csv',mime='text/csv')
            
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
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
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo] 
            
            df19B3=pd.DataFrame();df20B3=pd.DataFrame();df21B3=pd.DataFrame();df22B3=pd.DataFrame()
            p19B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p20B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p21B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p22B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            df19B3['Location']=p19B3.index;df19B3['2019']=p19B3.values;
            df20B3['Location']=p20B3.index;df20B3['2020']=p20B3.values;
            df21B3['Location']=p21B3.index;df21B3['2021']=p21B3.values;
            df22B3['Location']=p22B3.index;df22B3['2022']=p22B3.values;
            from functools import reduce
            DepJoinB3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19B3,df20B3,df21B3,df22B3]).set_index('Location')
            DepJoinB3=DepJoinB3.round(2).reset_index()
            DepJoinB3 = DepJoinB3[DepJoinB3.Location != 'Colombia']
            DepJoinB3 = DepJoinB3.sort_values(by=['2022'],ascending=False)
            DepJoinB3['relatGrow']=100*(DepJoinB3['2022']-DepJoinB3['2021'])/DepJoinB3['2021']
            DepJoinB3['absGrow']=DepJoinB3['2022']-DepJoinB3['2021']
            DepJoinBcopy3=DepJoinB3.copy()
            DepJoinBcopy3['2019']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2019'],1).astype(str)]
            DepJoinBcopy3['2020']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2020'],1).astype(str)]
            DepJoinBcopy3['2021']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2021'],1).astype(str)]
            DepJoinBcopy3['2022']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2022'],1).astype(str)]
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
            
            fig7Fijo = go.Figure()
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2019'],
                name=mes_opFijo+' 2019',
                marker_color='rgb(213,3,85)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2020'],
                name=mes_opFijo+' 2020',
                marker_color='rgb(255,152,0)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2021'],
                name=mes_opFijo+' 2021',
                marker_color='rgb(44,198,190)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2022'],
                name=mes_opFijo+' 2022',
                marker_color='rgb(72,68,242)'))

            fig7Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig7Fijo.update_yaxes(range=[0,max(DepJoinB3['2022'].values.tolist())+5],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Velocidad carga promedio (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig7Fijo.update_traces(textfont_size=22)
            fig7Fijo.update_layout(height=600,width=1200,legend_title=None)
            fig7Fijo.update_layout(legend=dict(orientation="h",y=0.9,xanchor='center',x=0.5))
            fig7Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig7Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,font=dict(size=18),
            title={
            'text': "<b>Velocidad anual de carga de Internet fijo por ciudad<br> (2019-2022)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig7Fijo.update_layout(barmode='group')
            fig7Fijo.update_layout(uniformtext_minsize=22, uniformtext_mode='show')
            fig7Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.1,yref='y domain',y=-0.5)             
            st.plotly_chart(fig7Fijo, use_container_width=True)  
            
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
            'text': "<b>Velocidad mensual de carga de Internet fijo<br>por proveedor (2018-2022) (en Mbps)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig8Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01',
            '2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01',
            '2022-03-01','2022-06-01','2022-09-01','2022-12-01'])
            fig8Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
            st.plotly_chart(fig8Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosCarga4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')            

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
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
            'text': "<b>Latencia mensual de Internet fijo en Colombia<br>(2018-2022)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig9Fijo.update_xaxes(tickvals=['2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01',
            '2022-06-01','2022-12-01'])
            fig9Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig9Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Latency1Fijo),file_name='Historico_latencia_Colombia.csv',mime='text/csv')             

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opFijoNombre[mes_opFijo]    
                
            Servidores=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Fijo/Fij-Servidores_Colombia.csv',encoding='latin-1',delimiter=';')
            Servidores['latitude']=Servidores['latitude'].str.replace(',','.')
            Servidores['longitude']=Servidores['longitude'].str.replace(',','.')
            ColLat2=Colombia2Fijo[(Colombia2Fijo['year']==2022)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Latency'].mean()
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
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes a comparar anualmente',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo] 
            
            df19C3=pd.DataFrame();df20C3=pd.DataFrame();df21C3=pd.DataFrame();df22C3=pd.DataFrame()
            p19C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p20C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p21C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p22C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2022)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            df19C3['Location']=p19C3.index;df19C3['2019']=p19C3.values;
            df20C3['Location']=p20C3.index;df20C3['2020']=p20C3.values;
            df21C3['Location']=p21C3.index;df21C3['2021']=p21C3.values;
            df22C3['Location']=p22C3.index;df22C3['2022']=p22C3.values;
            from functools import reduce
            DepJoinC3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df19C3,df20C3,df21C3,df22C3]).set_index('Location')
            DepJoinC3=DepJoinC3.round(2).reset_index()
            DepJoinC3 = DepJoinC3[DepJoinC3.Location != 'Colombia']
            DepJoinC3 = DepJoinC3.sort_values(by=['2022'],ascending=True)
            DepJoinC3['relatGrow']=100*(DepJoinC3['2022']-DepJoinC3['2021'])/DepJoinC3['2021']
            DepJoinC3['absGrow']=DepJoinC3['2022']-DepJoinC3['2021']
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}            
            fig10Fijo = go.Figure()
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2019'],
                name=mes_opFijo+' 2019',
                marker_color='rgb(213,3,85)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2020'],
                name=mes_opFijo+' 2020',
                marker_color='rgb(255,152,0)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2021'],
                name=mes_opFijo+' 2021',
                marker_color='rgb(44,198,190)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2022'],
                name=mes_opFijo+' 2022',
                marker_color='rgb(72,68,242)'))


            fig10Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig10Fijo.update_yaxes(range=[0,85],tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text="Latencia (ms)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig10Fijo.update_traces(textfont_size=22)
            fig10Fijo.update_layout(height=600,width=1200,legend_title=None)
            fig10Fijo.update_layout(legend=dict(orientation="h",y=1,xanchor='center',x=0.5))
            fig10Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig10Fijo.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,font=dict(size=18),
            title={
            'text': "<b>Latencia anual de Internet fijo por ciudad en ms<br> (2019-2022) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig10Fijo.update_layout(barmode='group')
            fig10Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.1,yref='y domain',y=-0.5)                 
            st.plotly_chart(fig10Fijo, use_container_width=True)  

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
            '2022-03-01','2022-06-01','2022-09-01','2022-12-01'])
            fig11Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.25) 
            st.plotly_chart(fig11Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosLatencia4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')   
            
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opFijoNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opFijo = st.selectbox('Escoja el año',[2020,2021,2022],2) 
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
 

#########################################################Lectura de bases Internet móvil#######################################

pathMovil='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/2022/Mediana/Internet_movil/'
#pathMovil2=r'C:\Users\santiago.bermudez\COMISION DE REGULACIÓN DE COMUNICACIONES\Mediciones Calidad QoE - Documents\Datos\Internet móvil\Mediana'
#### Sección 1 Móvil
#@st.cache(allow_output_mutation=True)
def ColombiaMovil1():
    Colombia1Movil=pd.read_csv(pathMovil+'/Colombia/Colombiahist_comp(2018a2022_Anual-Med).csv',delimiter=',',encoding='utf-8-sig')  
    Colombia1Movil=Colombia1Movil.drop(['Device','Platform','Metric Type'], axis=1) #Eliminar columnas      
    return Colombia1Movil
Colombia1Movil=ColombiaMovil1()
Colombia1Movil['Technology Type']=Colombia1Movil['Technology Type'].replace({'lte':'4g','cellular':'Total'})   
Colombia1Movil=Colombia1Movil.rename(columns={'Minimum Latency':'Latency'}) 

def create_metric_dataframe(df, metric, tech_type):
    filtered_df = df.loc[(df['Technology Type'] == tech_type), ['Aggregate Date', metric]]
    grouped_df = filtered_df.groupby(['Aggregate Date']).agg({metric: 'mean'})
    return grouped_df.rename(columns={metric: tech_type})

download_speed_dfs = [create_metric_dataframe(Colombia1Movil, 'Download Speed Mbps', tech_type) for tech_type in ['3g', '4g', 'Total']]
upload_speed_dfs = [create_metric_dataframe(Colombia1Movil, 'Upload Speed Mbps', tech_type) for tech_type in ['3g', '4g', 'Total']]
latency_dfs = [create_metric_dataframe(Colombia1Movil, 'Latency', tech_type) for tech_type in ['3g','4g', 'Total']]

DepJoinAMovilDown = download_speed_dfs[0].merge(download_speed_dfs[1], on='Aggregate Date', how='outer').merge(download_speed_dfs[2], on='Aggregate Date', how='outer').reset_index().round(2).rename(columns={'Aggregate Date':'year'})
DepJoinAMovilUp = upload_speed_dfs[0].merge(upload_speed_dfs[1], on='Aggregate Date', how='outer').merge(upload_speed_dfs[2], on='Aggregate Date', how='outer').reset_index().round(2).rename(columns={'Aggregate Date':'year'})
DepJoinAMovilLat = latency_dfs[0].merge(latency_dfs[1], on='Aggregate Date', how='outer').merge(latency_dfs[2], on='Aggregate Date', how='outer').reset_index().round(2).rename(columns={'Aggregate Date':'year'})

#### Sección 2 Móvil
#@st.cache(allow_output_mutation=True)
def ColombiaMovil2():
    Colombia2Movil=pd.read_csv(pathMovil+'/Departamentos/Desemphistcomp_Dep_Total(2022Mens-Med).csv',delimiter=';',encoding='latin-1') 
    Colombia2Movil['Location']=Colombia2Movil['Location'].str.split(',',expand=True)[0]#Guardar sólo departamentos
    FeAntig=Colombia2Movil['Aggregate Date'].unique() #Generar las fechas que tenían los datos
    FeCorre=pd.date_range('2022-01-01',periodo_tope, 
                  freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
    diction=dict(zip(FeAntig, FeCorre))
    Colombia2Movil['Aggregate Date'].replace(diction, inplace=True) #Reemplazar fechas antiguas por nuevas
    Colombia2Movil['Aggregate Date'] =pd.to_datetime(Colombia2Movil['Aggregate Date']).dt.floor('d') 
    Colombia2Movil['month']=pd.DatetimeIndex(Colombia2Movil['Aggregate Date']).month
    Colombia2Movil['year']=pd.DatetimeIndex(Colombia2Movil['Aggregate Date']).year
    Colombia2Movil = Colombia2Movil.drop(['Device','Platform','Technology Type','Metric Type'],axis=1)
    Colombia2Movil['Location'] = Colombia2Movil['Location'].str.upper()
    Colombia2Movil['Location'] = Colombia2Movil['Location'].replace({'SANTANDER DEPARTMENT':'SANTANDER','CAUCA DEPARTMENT':'CAUCA', 'SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA','NORTH SANTANDER':'NORTE DE SANTANDER','CAQUETÃ¡':'CAQUETA'})
    Colombia2Movil=Colombia2Movil[Colombia2Movil['Test Count']>30]
    return Colombia2Movil
Colombia2Movil=ColombiaMovil2()
Colombia2Movil=Colombia2Movil.rename(columns={'Minimum Latency':'Latency'})

#### Sección 3 Móvil
#@st.cache(allow_output_mutation=True)
def ColombiaMovil3():
    Colombia3Movil=pd.read_csv(pathMovil+'/Operadores/Desemphistcomp_Operad_(2018a2022_An-Med).csv',delimiter=';',encoding='utf-8-sig')
    Colombia3Movil=Colombia3Movil.drop(['Device','Platform','Metric Type','Location'],axis=1)
    return Colombia3Movil
Colombia3Movil = ColombiaMovil3()
Colombia3Movil['Aggregate Date']=Colombia3Movil['Aggregate Date'].astype('str')
Colombia3Movil=Colombia3Movil.rename(columns={'Minimum Latency':'Latency'}) 
Colombia3Movil=Colombia3Movil[Colombia3Movil['Provider']!='ETB']
DepJoinAMovil3=pd.pivot(Colombia3Movil, index=['Provider'],
        columns='Aggregate Date', values='Download Speed Mbps').fillna(0).reset_index().rename_axis(None, axis=1)        
DepJoinAMovil3Up=pd.pivot(Colombia3Movil[['Provider','Aggregate Date','Upload Speed Mbps']], index=['Provider'],
        columns='Aggregate Date', values='Upload Speed Mbps').fillna(0).reset_index().rename_axis(None, axis=1)
DepJoinAMovil3Lat=pd.pivot(Colombia3Movil[['Provider','Aggregate Date','Latency']], index=['Provider'],
        columns='Aggregate Date', values='Latency').fillna(0).reset_index().rename_axis(None, axis=1)  
#### Sección 4 Móvil
#@st.cache(allow_output_mutation=True)
def OpDepartMovil1():
    df1=pd.read_csv(pathMovil+'/Departamentos/MovETB-hist_comp(2018-2022-Med).csv',delimiter=';',encoding='utf-8-sig')
    df2=pd.read_csv(pathMovil+'/Departamentos/TigoClaroWom-hist_comp(2018-2022-Med).csv',delimiter=';',encoding='utf-8-sig')
    OpCiudMovil1=pd.concat([df1,df2])
    return OpCiudMovil1
OpCiudMovil1=OpDepartMovil1()
OpCiudMovil1['Location']=OpCiudMovil1['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntigMovil1=OpCiudMovil1['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorreMovil1=pd.date_range('2018-01-01',periodo_tope, 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
dictionMovil1=dict(zip(FeAntigMovil1, FeCorreMovil1))
OpCiudMovil1['Aggregate Date'].replace(dictionMovil1, inplace=True) #Reemplazar fechas antiguas por nuevas
OpCiudMovil1['Aggregate Date'] =pd.to_datetime(OpCiudMovil1['Aggregate Date']).dt.floor('d') 
OpCiudMovil1['month']=pd.DatetimeIndex(OpCiudMovil1['Aggregate Date']).month
OpCiudMovil1['year']=pd.DatetimeIndex(OpCiudMovil1['Aggregate Date']).year
OpCiudMovil1 = OpCiudMovil1.drop(['Device','Platform','Technology Type','Metric Type'],axis=1)
OpCiudMovil1['Location'] = OpCiudMovil1['Location'].str.upper()
OpCiudMovil1['Location'] = OpCiudMovil1['Location'].replace({'SANTANDER DEPARTMENT':'SANTANDER','CAUCA DEPARTMENT':'CAUCA','SAN ANDRÉS AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA','NORTH SANTANDER':'NORTE DE SANTANDER','CAQUETÁ':'CAQUETA'})
dataframe_namesMovil1=sorted(OpCiudMovil1.Location.unique().tolist())
OpCiudMovil1=OpCiudMovil1.replace(dict(zip(dataframe_namesMovil1, denominations_json2)))
OpCiudMovil1=OpCiudMovil1[OpCiudMovil1['Test Count']>30]
OpCiudMovil1['Provider']=OpCiudMovil1['Provider'].replace({'ETB (MVNO)':'ETB'})
OpCiudMovil1=OpCiudMovil1.rename(columns={'Minimum Latency':'Latency'})

#### Sección 5 Móvil
#@st.cache(allow_output_mutation=True)
def CiudadMovil1():
    Ciudades=pd.read_csv(pathMovil+'/Ciudades/Desemphistcomp_Ciud_(2018a2022_An-Med).csv',delimiter=';',encoding='utf-8-sig')
    Ciudades['Location']=Ciudades['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
    Ciudades=Ciudades.drop(['Device','Platform','Metric Type','Provider'], axis=1) #Eliminar columnas
    return Ciudades
CiudadMovil1=CiudadMovil1()
CiudadMovil1=CiudadMovil1[CiudadMovil1['Location']!='Colombia'].rename(columns={'Minimum Latency':'Latency'})
CiudadMovil1['Aggregate Date']=CiudadMovil1['Aggregate Date'].astype('str')

DepJoinAMovil4=pd.pivot(CiudadMovil1, index=['Location'],
        columns='Aggregate Date', values='Download Speed Mbps').fillna(0).reset_index().rename_axis(None, axis=1).sort_values(by=['2022'],ascending=False)   
DepJoinAMovil4Up=pd.pivot(CiudadMovil1, index=['Location'],
        columns='Aggregate Date', values='Upload Speed Mbps').fillna(0).reset_index().rename_axis(None, axis=1).sort_values(by=['2022'],ascending=False)  
DepJoinAMovil4Lat=pd.pivot(CiudadMovil1, index=['Location'],
        columns='Aggregate Date', values='Latency').fillna(0).reset_index().rename_axis(None, axis=1).sort_values(by=['2022'],ascending=True)          
#### Sección 6 Móvil
#@st.cache(allow_output_mutation=True)
def ColombiaMovil5():
    Operadores=pd.read_csv(pathMovil+'/Colombia/Colombiahist_comp(2018a2022_Mensual-Med).csv',delimiter=';',encoding='latin-1')
    Operadores=Operadores.rename(columns={'Minimum Latency':'Latency'})
    FeAntig=Operadores['Aggregate Date'].unique() #Generar las fechas que tenían los datos
    FeCorre=pd.date_range('2018-01-01',periodo_tope, 
                  freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
    diction=dict(zip(FeAntig, FeCorre))
    Operadores['Aggregate Date'].replace(diction, inplace=True) #Reemplazar fechas antiguas por nuevas
    Operadores['Aggregate Date'] =pd.to_datetime(Operadores['Aggregate Date']).dt.floor('d') 
    Operadores['month']=pd.DatetimeIndex(Operadores['Aggregate Date']).month
    Operadores['year']=pd.DatetimeIndex(Operadores['Aggregate Date']).year
    Operadores = Operadores.drop(['Location','Device','Platform','Metric Type'],axis=1)
    df3gA=pd.DataFrame();df4gA=pd.DataFrame();dfTotA=pd.DataFrame()
    #Clasificar información por tecnología, y extraer información de interés
    p3gA=(Operadores.loc[(Operadores['Technology Type']=='3g'),['Aggregate Date','Latency']]).groupby(['Aggregate Date'])['Latency'].mean()
    p4gA=(Operadores.loc[(Operadores['Technology Type']=='lte'),['Aggregate Date','Latency']]).groupby(['Aggregate Date'])['Latency'].mean()
    pTotA=(Operadores.loc[(Operadores['Technology Type']=='cellular'),['Aggregate Date','Latency']]).groupby(['Aggregate Date'])['Latency'].mean()
    #Agregar información a los dataframe, con el adecuado formato
    df3gA['Date']=p3gA.index; df3gA['3g']=p3gA.values;
    df4gA['Date']=p4gA.index;df4gA['4g']=p4gA.values;
    dfTotA['Date']=pTotA.index;dfTotA['Total']=pTotA.values;
    #Unir y organizar los dataframe creados
    from functools import reduce
    DepJoinA=reduce(lambda x,y: pd.merge(x,y, on='Date', how='outer'), [df3gA,df4gA,dfTotA]).set_index('Date')
    DepJoinA=DepJoinA.round(2).reset_index()
    return DepJoinA
ColombiaMovil5=ColombiaMovil5()    


#### Sección 7 Móvil
#@st.cache(allow_output_mutation=True)
def ColombiaMovil7():
    Colombia7=pd.read_csv(pathMovil+'/Cobertura/Coberturahistcomp_Colombia_(2018-2022)-Med.csv',delimiter=';',encoding='latin-1')
    Colombia7['4G total'] = Colombia7[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Colombia7['Roaming total'] = Colombia7[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)   
    return Colombia7
Colombia7Movil=ColombiaMovil7()

####  Sección 8 Móvil
#@st.cache(allow_output_mutation=True)
def DepJoinA8Movil():
    Ciudades8=pd.read_csv(pathMovil+'/Cobertura/Coberturahistcomp_Ciud_(2018-2022)-Med.csv',delimiter=';',encoding='utf-8-sig')
    Ciudades8['Location']=Ciudades8['Location'].str.split(',',expand=True)[0]
    Ciudades8['4G total'] = Ciudades8[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Ciudades8['Aggregate Date']=Ciudades8['Aggregate Date'].astype('str')
    Ciudades8['Roaming total'] = Ciudades8[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)   
    DepJoinA_8=Ciudades8.groupby(['Aggregate Date','Location'])['4G total'].mean().reset_index()
    DepJoinA_8=pd.pivot(DepJoinA_8, index=['Location'],
            columns='Aggregate Date', values='4G total').fillna(0).reset_index().rename_axis(None, axis=1).sort_values(by='2022',ascending=False)
    return DepJoinA_8
DepJoinAMovil8=DepJoinA8Movil()

####  Sección 9 Móvil
#@st.cache(allow_output_mutation=True)
def OpJoinA9Movil():
    Operadores9=pd.read_csv(pathMovil+'/Cobertura/Coberturahistcomp_Gnral_(2018-2022)-Med.csv',delimiter=';',encoding='utf-8-sig')
    Operadores9['4G total'] = Operadores9[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Operadores9['Aggregate Date']=Operadores9['Aggregate Date'].astype('str')
    Operadores9['Roaming total'] = Operadores9[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)
    OpJoinA_9=Operadores9.groupby(['Aggregate Date','Provider'])['4G total'].mean().reset_index()
    OpJoinA_9=pd.pivot(OpJoinA_9, index=['Provider'],
            columns='Aggregate Date', values='4G total').fillna(0).reset_index().rename_axis(None, axis=1).sort_values(by='2022',ascending=False)
    return Operadores9
OpJoinAMovil9=OpJoinA9Movil()
OpJoinAMovil9=OpJoinAMovil9[OpJoinAMovil9['Provider']!='ETB']

if select_servicio == 'Internet móvil':
    select_indicador=st.selectbox('Indicador de desempeño y cobertura',['Velocidad de descarga','Velocidad de carga','Latencia','Registro en red'])  
    
    if select_indicador== 'Velocidad de descarga':
        dimension_Vel_descarga_Movil = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_descarga_Movil == 'Histórico Colombia':    
            
            fig1Movil = go.Figure()
            fig1Movil.add_trace(go.Bar(
                x=DepJoinAMovilDown['year'], 
                y=DepJoinAMovilDown['3g'],
                name='3G',
                marker_color='rgb(242,61,76)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.add_trace(go.Bar(
                x=DepJoinAMovilDown['year'],
                y=DepJoinAMovilDown['4g'],
                name='4G',
                marker_color='rgb(1,10,38)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.add_trace(go.Bar(
                x=DepJoinAMovilDown['year'],
                y=DepJoinAMovilDown['Total'],
                name='Total',
                marker_color='rgb(2,94,115)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig1Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad descarga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig1Movil.update_traces(textfont_size=18)
            fig1Movil.update_layout(height=500,legend_title=None)
            fig1Movil.update_layout(legend=dict(orientation="h",y=1.05,x=0.4))
            fig1Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig1Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad anual de descarga de Internet móvil en <br>Colombia (2018-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig1Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)    
            st.plotly_chart(fig1Movil, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(DepJoinAMovilDown),file_name='MovilAnno_descarga_Colombia.csv',mime='text/csv')
            
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2022',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil]  
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==año_opMovil)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Download Speed Mbps'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)

            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')                
            if departamentos_dfMovil1.empty==True:
                st.markdown('No se presentan datos para el mes seleccionado.')                
            else:
                colombia_map1Movil = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                   scrollWheelZoom=True,
                   dragging=True)            
                tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                for tile in tiles:
                    folium.TileLayer(tile).add_to(colombia_map1Movil)
                choropleth=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=departamentos_dfMovil1,
                    columns=['Location', 'Download Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de descarga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(colombia_map1Movil)
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth.geojson.add_child(
                    folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
                folium.LayerControl().add_to(colombia_map1Movil)

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
                    data = departamentos_dfMovil1,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Download Speed Mbps'],
                        aliases=['Departamento','Velocidad descarga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                colombia_map1Movil.add_child(NIL)
                colombia_map1Movil.keep_in_front(NIL)
                for key in choropleth._children:
                    if key.startswith('color_map'):
                        del(choropleth._children[key])            
                        
                col1b, col2b ,col3b= st.columns([1,4,1])
                with col2b:
                    st.markdown("<center><b> Velocidad de descarga de Internet móvil en Colombia<br>por departamento (en Mbps)</b></center>",unsafe_allow_html=True)
                    folium_static(colombia_map1Movil,width=480) 
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_descarga_Movil == 'Operadores':
            
            fig2Movil = go.Figure()
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))
            fig2Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig2Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad descarga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig2Movil.update_traces(textfont_size=18)
            fig2Movil.update_layout(height=500,legend_title=None)
            fig2Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig2Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig2Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad anual de descarga de Internet móvil <br>Por operador (2019-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig2Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.2) 
            st.plotly_chart(fig2Movil, use_container_width=True)                   

 
            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil] 
            
            providers = ['Claro', 'ETB', 'Movistar', 'Tigo', 'WOM']
            
            final_dfAncMovil=gdf2.merge(OpCiudMovil1.groupby(['Location'])['Download Speed Mbps'].median().reset_index(), on='Location')
            final_dfAncMovil['Download Speed Mbps']=np.nan
            
            final_dfMovil_dict = {}
            for provider in providers:
                if OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty:
                    final_dfMovil_dict[provider]=final_dfAncMovil
                else:
                    ProveedorMovil = OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                    ProveedorMovil['Download Speed Mbps'] = round(ProveedorMovil['Download Speed Mbps'], 2)
                    final_dfMovil_dict[provider] = gdf2.merge(ProveedorMovil, on='Location')
            
            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth3=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Claro'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m1)
            #######
            choropleth4=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Movistar'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth3.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth4.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m2)
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
                data = final_dfMovil_dict['Claro'],
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
                data = final_dfMovil_dict['Movistar'],
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

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth5=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Tigo'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m1)
            #######
            choropleth6=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['WOM'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth5.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth6.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m2)
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
                data = final_dfMovil_dict['Tigo'],
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
                data = final_dfMovil_dict['WOM'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Download Speed Mbps'],
                    aliases=['Departamento','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth5._children:
                if key.startswith('color_map'):
                    del(choropleth5._children[key])
            for key in choropleth6._children:
                if key.startswith('color_map'):
                    del(choropleth6._children[key])

            dualmap1_3Movil.m1.add_child(NIL1)
            dualmap1_3Movil.m1.keep_in_front(NIL1)
            dualmap1_3Movil.m2.add_child(NIL2)
            dualmap1_3Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/wom.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_3Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_3Movil.m2)

            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Velocidad de descarga de Internet móvil por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_descarga_Movil == 'Ciudades':
            fig3Movil=go.Figure()
            
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))

            fig3Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig3Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad descarga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig3Movil.update_traces(textfont_size=18)
            fig3Movil.update_layout(height=600,legend_title=None)
            fig3Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig3Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig3Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad anual de descarga de Internet móvil <br>por ciudad (2018-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig3Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.51)               
            st.plotly_chart(fig3Movil, use_container_width=True) 

            col1, col2= st.columns(2)
            with col1:
                Año_opMovilIz = st.selectbox('Escoja el año para el panel de la izquierda',['2018','2019','2020','2021'],index=3)          
            
            
            DicIz=CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']==Año_opMovilIz)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            DicDer=CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']=='2022')][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            DicIzList=DicIz['Location'].unique().tolist()
            DicDerList=DicDer['Location'].unique().tolist()

            if 'Colombia' in DicIzList:
                DicIzList.remove('Colombia')
            if 'Colombia' in DicDerList:
                DicDerList.remove('Colombia')    

            dict_coloresMovil={'Bucaramanga':'rgb(255,128,0)','Bogotá':'rgb(255,0,0)','Cali':'rgb(255,255,0)',
                 'Medellín':'rgb(128,255,0)','Barranquilla':'rgb(0,255,0)','Cartagena':'rgb(0,255,128)',
                 'Villavicencio':'rgb(255,102,102)','Ibagué':'rgb(0,128,255)','Manizales':'rgb(0,0,255)',
                 'Tunja':'rgb(127,0,255)','Pasto':'rgb(255,0,255)','Santa Marta':'rgb(255,0,127)',
                 'Sincelejo':'rgb(128,128,128)','Armenia':'rgb(102,0,0)','Montería':'rgb(0,255,255)',
                 'Pereira':'rgb(0,51,51)','Popayán':'rgb(51,0,25)','Cúcuta': 'rgb(0, 204, 102)','Neiva': 'rgb(255, 102, 0)',
                 'Valledupar': 'rgb(102, 102, 255)','Riohacha': 'rgb(255, 153, 204)','Arauca': 'rgb(0, 153, 153)',
                 'Yopal': 'rgb(255, 204, 0)','Florencia': 'rgb(153, 51, 255)'}
            figCiudMov = make_subplots(rows=1, cols=2,subplot_titles=(Año_opMovilIz,"2022"),horizontal_spacing = 0.05)
            for location in DicIzList:
                figCiudMov.add_trace(go.Scatter(
                    x=DicIz[DicIz['Location']==location]['Download Speed Mbps'].values, y=DicIz[DicIz['Location']==location]['Upload Speed Mbps'].values, 
                    mode='markers',
                    marker=dict(
                        color=dict_coloresMovil[location],
                        opacity=0.7,
                        size=0.8*DicIz[DicIz['Location']==location]['Latency'].values,
                    ),
                text=DicIz[DicIz['Location']==location]['Latency'].values,showlegend=False,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)

            for location in DicDerList:
                figCiudMov.add_trace(go.Scatter(
                    x=DicDer[DicDer['Location']==location]['Download Speed Mbps'].values, y=DicDer[DicDer['Location']==location]['Upload Speed Mbps'].values, name=location,
                    mode='markers',
                    marker=dict(
                        color=dict_coloresMovil[location],
                        opacity=0.7,
                        size=0.8*DicDer[DicDer['Location']==location]['Latency'].values,
                    ),
                text=DicDer[DicDer['Location']==location]['Latency'].values,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=2)


            figCiudMov.update_xaxes(tickangle=0,range=[0,max(DicDer['Download Speed Mbps'].values.tolist())+5],title_font=dict(family="Tahoma"),titlefont_size=18,tickfont=dict(family='Tahoma', color='black', size=18),ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            figCiudMov.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18,ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            figCiudMov.update_annotations(font_size=18)
            figCiudMov.update_layout(height=700,legend_title=None)
            figCiudMov.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            figCiudMov.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16)  
            figCiudMov.update_xaxes(showspikes=True,title_text='Velocidad de descarga (Mbps)')
            figCiudMov.update_yaxes(showspikes=True,range=[4,12],title_text="Velocidad de carga (Mbps)", row=1, col=1)
            figCiudMov.update_yaxes(showspikes=True,range=[4,12],title_text=None, row=1, col=2)
            figCiudMov.update_layout(legend=dict(y=1.1,x=1,orientation='v',font_family='tahoma',font_size=18))          
            figCiudMov.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',x=0.5,yref='y domain',y=-0.16)            
            st.plotly_chart(figCiudMov, use_container_width=True)
              
    if select_indicador== 'Velocidad de carga':
        dimension_Vel_carga_Movil = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Vel_carga_Movil == 'Histórico Colombia':    
            fig4Movil = go.Figure()
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'], 
                y=DepJoinAMovilUp['3g'],
                name='3G',
                marker_color='rgb(242,61,76)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'],
                y=DepJoinAMovilUp['4g'],
                name='4G',
                marker_color='rgb(1,10,38)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'],
                y=DepJoinAMovilUp['Total'],
                name='Total',
                marker_color='rgb(2,94,115)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig4Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig4Movil.update_traces(textfont_size=18)
            fig4Movil.update_layout(height=500,legend_title=None)
            fig4Movil.update_layout(legend=dict(orientation="h",y=1.05,x=0.4))
            fig4Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig4Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad anual de carga de Internet móvil en <br>Colombia (2018-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig4Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)  
                
            st.plotly_chart(fig4Movil, use_container_width=True)
            #st.download_button(label="Descargar CSV",data=convert_df(DepJoinAMovilUp),file_name='MovilAnno_descarga_Colombia.csv',mime='text/csv')            

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil]   
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==año_opMovil)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Upload Speed Mbps'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)
            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')    
            
            if departamentos_dfMovil1.empty==True:
                st.markdown('No se presentan datos para el mes seleccionado.')
            else:        
                colombia_map1Movi2 = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                   scrollWheelZoom=True,
                   dragging=True)            
                tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                for tile in tiles:
                    folium.TileLayer(tile).add_to(colombia_map1Movi2)
                choropleth=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=departamentos_dfMovil1,
                    columns=['Location', 'Upload Speed Mbps'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Velocidad de carga (Mbps)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(colombia_map1Movi2)
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth.geojson.add_child(
                    folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
                folium.LayerControl().add_to(colombia_map1Movi2)

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
                    data = departamentos_dfMovil1,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Upload Speed Mbps'],
                        aliases=['Departamento','Velocidad de carga'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                colombia_map1Movi2.add_child(NIL)
                colombia_map1Movi2.keep_in_front(NIL)
                for key in choropleth._children:
                    if key.startswith('color_map'):
                        del(choropleth._children[key])   
                        
                col1b, col2b ,col3b= st.columns([1,4,1])
                with col2b:
                    st.markdown("<center><b> Velocidad de carga de Internet móvil<br>por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
                    folium_static(colombia_map1Movi2,width=480) 
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)
                
        if dimension_Vel_carga_Movil == 'Operadores':  
  
            fig6Movil = go.Figure()
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))
            fig6Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig6Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig6Movil.update_traces(textfont_size=18)
            fig6Movil.update_layout(height=500,legend_title=None)
            fig6Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig6Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig6Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
            title={
            'text': "<b>Velocidad anual de carga de Internet móvil <br>Por operador (2019-2022) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig6Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.2) 
            st.plotly_chart(fig6Movil, use_container_width=True)                   

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil] 
            
            providers = ['Claro', 'ETB', 'Movistar', 'Tigo', 'WOM']
            
            final_dfAncMovil=gdf2.merge(OpCiudMovil1.groupby(['Location'])['Upload Speed Mbps'].median().reset_index(), on='Location')
            final_dfAncMovil['Upload Speed Mbps']=np.nan
            
            final_dfMovil_dict = {}
            for provider in providers:
                if OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty:
                    final_dfMovil_dict[provider]=final_dfAncMovil
                else:
                    ProveedorMovil = OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                    ProveedorMovil['Upload Speed Mbps'] = round(ProveedorMovil['Upload Speed Mbps'], 2)
                    final_dfMovil_dict[provider] = gdf2.merge(ProveedorMovil, on='Location')
            

            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth3=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Claro'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m1)
            #######
            choropleth4=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Movistar'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth3.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth4.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m2)
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
                data = final_dfMovil_dict['Claro'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Upload Speed Mbps'],
                    aliases=['Departamento','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            NIL2 = folium.features.GeoJson(
                data = final_dfMovil_dict['Movistar'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Upload Speed Mbps'],
                    aliases=['Departamento','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth3._children:
                if key.startswith('color_map'):
                    del(choropleth3._children[key])
            for key in choropleth4._children:
                if key.startswith('color_map'):
                    del(choropleth4._children[key])

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth5=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Tigo'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m1)
            #######
            choropleth6=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['WOM'],
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth5.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth6.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m2)
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
                data = final_dfMovil_dict['Tigo'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Upload Speed Mbps'],
                    aliases=['Departamento','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            NIL2 = folium.features.GeoJson(
                data = final_dfMovil_dict['WOM'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Upload Speed Mbps'],
                    aliases=['Departamento','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth5._children:
                if key.startswith('color_map'):
                    del(choropleth5._children[key])
            for key in choropleth6._children:
                if key.startswith('color_map'):
                    del(choropleth6._children[key])

            dualmap1_3Movil.m1.add_child(NIL1)
            dualmap1_3Movil.m1.keep_in_front(NIL1)
            dualmap1_3Movil.m2.add_child(NIL2)
            dualmap1_3Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/wom.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_3Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_3Movil.m2)

            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Velocidad de carga de Internet móvil por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Movil == 'Ciudades':
            
            fig8Movil=go.Figure()
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))

            fig8Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig8Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig8Movil.update_traces(textfont_size=18)
            fig8Movil.update_layout(height=600,legend_title=None)
            fig8Movil.update_layout(legend=dict(orientation="h",y=0.99,xanchor='center',x=0.5))
            fig8Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig8Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
            title={
            'text': "<b>Velocidad anual de carga de Internet móvil <br>por ciudad (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig8Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.4)             
            st.plotly_chart(fig8Movil, use_container_width=True) 

    if select_indicador== 'Latencia':
        dimension_Vel_carga_Movil = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True) 
        
        if dimension_Vel_carga_Movil == 'Histórico Colombia':    
            fig5Movil = make_subplots(rows=1,cols=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['Total'],line=dict(color='rgb(2,94,115)', width=1.5),marker=dict(
                        color='white',line=dict(color='rgb(2,94,115)',width=1),size=5),mode='lines+markers',name='Total'),row=1, col=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['3g'],
                                     line=dict(color='rgb(242,61,76)', width=1.5),marker=dict(
                        color='white',line=dict(color='rgb(242,61,76)',width=1),size=5),mode='lines+markers',name='3G'),row=1, col=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['4g'],
                         line=dict(color='rgb(1,10,38)', width=1.5),marker=dict(
                         color='white',line=dict(color='rgb(1,10,38)',width=1),size=5),mode='lines+markers',name='4G'),row=1, col=1)
                         
            fig5Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig5Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=14, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig5Movil.update_traces(textfont_size=18)
            fig5Movil.update_layout(height=500,legend_title=None,font=dict(size=18))
            fig5Movil.update_layout(legend=dict(orientation="h",yanchor='top',xanchor='center',x=0.5,y=0.99),showlegend=True)
            fig5Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig5Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=14,
            title={
            'text': "<b>Latencia mensual de Internet móvil en<br> Colombia (2018-2022) (en ms)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig5Movil.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01','2020-12-01',
            '2021-03-01','2021-06-01','2021-09-01','2021-12-01','2022-03-01','2022-06-01','2022-09-01','2022-12-01'])
            fig5Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25) 
                
            st.plotly_chart(fig5Movil, use_container_width=True)    

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil]                      
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==año_opMovil)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Latency'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)

            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')    
            
            if departamentos_dfMovil1.empty==True:
                st.markdown('No se presentan datos para el mes seleccionado.')
            else:                
                colombia_map1Movi2 = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
                   scrollWheelZoom=True,
                   dragging=True)            
                tiles = ['stamenwatercolor', 'cartodbpositron', 'openstreetmap', 'stamenterrain']
                for tile in tiles:
                    folium.TileLayer(tile).add_to(colombia_map1Movi2)
                choropleth=folium.Choropleth(
                    geo_data=Colombian_DPTO2,
                    data=departamentos_dfMovil1,
                    columns=['Location', 'Latency'],
                    key_on='feature.properties.NOMBRE_DPT',
                    fill_color='YlGnBu', 
                    fill_opacity=0.9, 
                    line_opacity=0.9,
                    legend_name='Latencia (ms)',
                    nan_fill_color = "black",
                    smooth_factor=0).add_to(colombia_map1Movi2)
                # Adicionar nombres del departamento
                style_function = "font-size: 15px; font-weight: bold"
                choropleth.geojson.add_child(
                    folium.features.GeoJsonTooltip(['NOMBRE_DPT'], style=style_function, labels=False))
                folium.LayerControl().add_to(colombia_map1Movi2)

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
                    data = departamentos_dfMovil1,
                    style_function=style_function, 
                    control=False,
                    highlight_function=highlight_function, 
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['Location','Latency'],
                        aliases=['Departamento','Latencia'],
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                    )
                )
                colombia_map1Movi2.add_child(NIL)
                colombia_map1Movi2.keep_in_front(NIL)
                
                for key in choropleth._children:
                    if key.startswith('color_map'):
                        del(choropleth._children[key])            
                                  
                col1b, col2b ,col3b= st.columns([1,4,1])
                with col2b:
                    st.markdown("<center><b> Latencia de Internet móvil por departamento (en ms)</b></center>",unsafe_allow_html=True) 
                    folium_static(colombia_map1Movi2,width=480) 
                    st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Movil == 'Operadores':  
  
            fig7Movil = go.Figure()
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))
            fig7Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig7Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig7Movil.update_traces(textfont_size=18)
            fig7Movil.update_layout(height=500,legend_title=None)
            fig7Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig7Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig7Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Latencia de Internet móvil <br>Por operador (2019-2022) (en ms) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig7Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.2) 
            st.plotly_chart(fig7Movil, use_container_width=True)                   

            col1,col2,col3,col4= st.columns([2,1,1,2])
            mes_opMovilNombre={'Enero':1,'Febrero':2,'Marzo':3,'Abril':4,'Mayo':5,'Junio':6,'Julio':7,'Agosto':8,'Septiembre':9,'Octubre':10,'Noviembre':11,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes',['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],11) 
            with col3:    
                año_opMovil = st.selectbox('Escoja el año',[2020,2021,2022],2) 
            mes=mes_opMovilNombre[mes_opMovil] 
            
            providers = ['Claro', 'ETB', 'Movistar', 'Tigo', 'WOM']
            
            final_dfAncMovil=gdf2.merge(OpCiudMovil1.groupby(['Location'])['Latency'].median().reset_index(), on='Location')
            final_dfAncMovil['Latency']=np.nan
            
            final_dfMovil_dict = {}
            for provider in providers:
                if OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty:
                    final_dfMovil_dict[provider]=final_dfAncMovil
                else:
                    ProveedorMovil = OpCiudMovil1.loc[(OpCiudMovil1['Provider']==provider)&(OpCiudMovil1['year']==año_opMovil)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                    ProveedorMovil['Latency'] = round(ProveedorMovil['Latency'], 2)
                    final_dfMovil_dict[provider] = gdf2.merge(ProveedorMovil, on='Location')
            
            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth3=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Claro'],
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m1)
            #######
            choropleth4=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Movistar'],
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth3.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth4.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m2)
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
                data = final_dfMovil_dict['Claro'],
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
                data = final_dfMovil_dict['Movistar'],
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

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=True,
               scrollWheelZoom=True,
               dragging=True)
            ########
            choropleth5=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['Tigo'],
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m1)
            #######
            choropleth6=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_dfMovil_dict['WOM'],
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth5.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth6.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m2)
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
                data = final_dfMovil_dict['Tigo'],
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
                data = final_dfMovil_dict['WOM'],
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth5._children:
                if key.startswith('color_map'):
                    del(choropleth5._children[key])
            for key in choropleth6._children:
                if key.startswith('color_map'):
                    del(choropleth6._children[key])

            dualmap1_3Movil.m1.add_child(NIL1)
            dualmap1_3Movil.m1.keep_in_front(NIL1)
            dualmap1_3Movil.m2.add_child(NIL2)
            dualmap1_3Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/tigo.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/wom.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_3Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_3Movil.m2)

            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Latencia de Internet móvil por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2022</i></p> """,unsafe_allow_html=True)
  
        if dimension_Vel_carga_Movil == 'Ciudades':         

            fig9Movil=go.Figure()
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))

            fig9Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig9Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Latencia (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig9Movil.update_traces(textfont_size=18)
            fig9Movil.update_layout(height=600,legend_title=None)
            fig9Movil.update_layout(legend=dict(orientation="h",y=0.99,xanchor='center',x=0.5))
            fig9Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig9Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
            title={
            'text': "<b>Latencia de Internet móvil <br>por ciudad (2019-2022) (en ms) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig9Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2019 - 2022. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='paper',yref='y domain',y=-0.4)             
            st.plotly_chart(fig9Movil, use_container_width=True) 
            
    if select_indicador== 'Registro en red':
        st.markdown("### Registro en Red", unsafe_allow_html=True)
        
        fig10Movil = go.Figure()
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021','2022'],
            y=Colombia7Movil['2G (%)'],
            name='2G (%)',
            marker_color='rgb(17,200,164)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021','2022'],
            y=Colombia7Movil['3G (%)'],
            name='3G (%)',
            marker_color='rgb(242,61,76)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021','2022'],
            y=Colombia7Movil['4G (%)'],
            name='4G (%)',
            marker_color='rgb(1,10,38)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021','2022'],
            y=Colombia7Movil['Roaming total'],
            name='Roaming total (%)',
            marker_color='rgb(179,0,94)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021','2022'],
            y=Colombia7Movil['No Coverage (%)'],
            name='No Cobertura (%)',
            marker_color='rgb(254,184,52)',
            width=0.7))
        fig10Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),titlefont_size=18,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
        fig10Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
        fig10Movil.update_layout(height=500,legend_title=None)
        fig10Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16)
        fig10Movil.update_layout(height=600,   
            title="<b>Promedio anual del porcentaje de registro en red en Colombia<br>(2018-2022)</b>",
            title_x=0.5)
        fig10Movil.update_layout(uniformtext_minsize=12, barmode='stack', showlegend=True,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
           orientation="v",
            y=1.05,
            x=1,
            font_size=12))
        fig10Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)     
        st.plotly_chart(fig10Movil, use_container_width=True) 
        
        st.markdown("### Registro en Red 4G", unsafe_allow_html=True)
        dimension_Cober4G_Movil = st.radio("Seleccione la dimensión del análisis",('Colombia','Ciudades','Operadores'),horizontal=True)
        
        if dimension_Cober4G_Movil=='Colombia':
            fig11Movil = go.Figure()
            fig11Movil.add_trace(go.Bar(
                x=['2018','2019','2020','2021','2022'],
                y=Colombia7Movil['4G total'].round(1),
                name='4G (%)',
                marker_color='rgb(1,10,38)', 
                width=0.7))

            fig11Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),titlefont_size=18,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig11Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig11Movil.update_traces(textfont_size=18)
            fig11Movil.update_layout(height=500,legend_title=None)
            fig11Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig11Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18)
            fig11Movil.update_layout(height=600,   
                title="<b>Promedio anual del porcentaje de registro en red 4G en Colombia<br>(2018-2022)</b>",
                title_x=0.5)
            fig11Movil.update_traces()
            fig11Movil.update_layout(uniformtext_minsize=18, barmode='stack', uniformtext_mode='hide')
            fig11Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            fig11Movil.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig11Movil.update_layout(legend=dict(
               orientation="h",
                y=0.99,
                xanchor='center',
                x=0.5,
                font_size=18))
            fig11Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)     
            st.plotly_chart(fig11Movil,use_container_width=True)   
            
        if dimension_Cober4G_Movil=='Ciudades':
            fig12Movil = go.Figure()
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2019'],
                name='2019',
                marker_color='rgb(213,3,85)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2020'],
                name='2020',
                marker_color='rgb(255,152,0)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2021'],
                name='2021',
                marker_color='rgb(44,198,190)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2022'],
                name='2022',
                marker_color='rgb(72,68,242)'))

            fig12Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Tahoma', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig12Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),title_font=dict(family="Tahoma"),titlefont_size=18, title_text='Registro en red 4G (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig12Movil.update_traces(textfont_size=18)
            fig12Movil.update_layout(height=600,legend_title=None)
            fig12Movil.update_layout(legend=dict(orientation="h",y=0.99,xanchor='center',x=0.5))
            fig12Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig12Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18,
            title={
            'text': "<b>Promedio anual registro en red móvil por ciudad <br>(2019-2022)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}) 
            fig12Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2019 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.4)             
            st.plotly_chart(fig12Movil,use_container_width=True)

        if dimension_Cober4G_Movil=='Operadores':
        
            OpJoinAMovil92=OpJoinAMovil9[['Aggregate Date','Provider','4G (%)', '4G Roaming (%)']]
            OpJoinAMovil92['4G total']=OpJoinAMovil92['4G (%)']+OpJoinAMovil92['4G Roaming (%)']
            OpJoinAMovil92[OpJoinAMovil92['Aggregate Date']>'2018'].round(1)

            color4g=['rgb(213,3,85)','rgb(255,152,0)','rgb(44,198,190)','rgb(72,68,242)']
            color4gRoaming=['rgba(213,3,85,0.5)','rgba(255,152,0,0.5)','rgba(44,198,190,0.5)','rgba(72,68,242,0.5)']
            fig13Movil = px.bar(OpJoinAMovil92[OpJoinAMovil92['Aggregate Date']>'2018'], x='Provider', y=['4G (%)','4G Roaming (%)'],
                         color='Aggregate Date', barmode='group',color_discrete_sequence=color4g)

            fig13Movil.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=25),title_font=dict(family="Tahoma"),titlefont_size=25,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig13Movil.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=25),title_font=dict(family="Tahoma"),titlefont_size=25, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig13Movil.update_traces(textfont_size=20)
            fig13Movil.update_layout(height=500,legend_title=None)
            fig13Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig13Movil.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=16)
            fig13Movil.update_layout(height=600)
            fig13Movil.update_layout(barmode='group', uniformtext_mode='hide',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
               orientation="h",
                y=1.05,
                xanchor='center',
                x=0.5,font_size=18))
            fig13Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2019 - 2022.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)                 
            st.plotly_chart(fig13Movil,use_container_width=True)    

######################################################### Comparación Internacional #######################################        
#Diciembre de 2022
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

movil_Intdict = {'Estados Unidos':[78.86,9.28,31],'Uruguay':[35.68,11.11,26],'Colombia':[12.15,9.49,35],
'Venezuela':[5.95,3.64,36],'Ecuador':[19.88,10.61,31],'Peru':[16.67,11.97,28],'Bolivia':[9.98,9.45,24],
'Paraguay':[17.45,7.77,32],'Brasil':[36.07,11.12,27],'Chile':[27.86,12.62,24],'Argentina':[22.55,6.75,29],
'Canadá':[87.48,11.57,23],'México':[25.92,10.51,32],'España':[35.1,9.68,34],'Reino Unido':[49.13,7.48,35],
'Alemania':[58.83,11.52,28],'Japón':[42.83,7.88,38],'Corea del sur':[122.55,16.26,41]}

Movil__Int=pd.DataFrame.from_dict(movil_Intdict,orient='index').reset_index()
Movil__Int=Movil__Int.rename(columns={'index':'País',0:'Download',1:'Upload',2:'Latency'})
Movil_df=gdf_Int.merge(Movil__Int, on='País')

dict_coloresPais = {'Estados Unidos':'rgb(51,0,25)','Uruguay':'rgb(255,0,0)','Colombia':'rgb(255,255,0)',
'Venezuela':'rgba(128,255,0,0.3)','Ecuador':'rgb(255,0,255)','Peru':'rgb(0,255,128)','Bolivia':'rgb(255,102,102)',
'Paraguay':'rgb(0,128,255)','Brasil':'rgb(0,51,51)','Chile':'rgb(0,0,255)','Argentina':'rgb(127,0,255)',
'Canadá':'rgb(255,128,0)','México':'rgb(255,128,128)','España':'rgb(192,192,102)','Reino Unido':'rgb(102,102,255)',
'Alemania':'rgb(204,0,0)','Japón':'rgb(255,153,204)','Corea del sur':'rgb(255,204,153)'}

if select_servicio == 'Comparación internacional':
    st.markdown("### Internet fijo",unsafe_allow_html=True)
    fig1Int=make_subplots(rows=1,cols=1)
    for pais in Fijo_Int['País'].unique().tolist():
        fig1Int.add_trace(go.Scatter(
        x=Fijo_Int[Fijo_Int['País']== pais]['Download'].values, y=Fijo_Int[Fijo_Int['País']== pais]['Upload'].values, name=pais,
        mode='markers',
        text=Fijo_Int[Fijo_Int['País']== pais]['Latency'],
        marker=dict(
            color=dict_coloresPais[pais],
            opacity=1,
            size=2*Fijo_Int[Fijo_Int['País']== pais]['Latency']),hovertemplate='<b>País:</b>'+pais+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
    fig1Int.update_xaxes(tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='tahoma',titlefont_size=18,title_text='Velocidad de descarga (Mbps)',ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
    fig1Int.update_yaxes(tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='tahoma',titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
    fig1Int.update_traces(textfont_size=16)
    fig1Int.update_layout(height=500,legend_title=None)
    fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    fig1Int.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18)

    fig1Int.update_layout(height=600,   
        title='<b>Diagrama de burbujas de indicadores de desempeño en Internet fijo por país<br>(Diciembre 2022)',
        title_x=0.5,
        font=dict(
            family="Tahoma",
            color=" black",size=18))
    fig1Int.update_layout(legend=dict(y=1,x=1,font_size=17))
    fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig1Int.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1Int, use_container_width=True) 

    st.markdown("### Internet móvil",unsafe_allow_html=True)

    fig2Int=make_subplots(rows=1,cols=1)
    for pais in Movil__Int['País'].unique().tolist():
        fig2Int.add_trace(go.Scatter(
        x=Movil__Int[Movil__Int['País']== pais]['Download'].values, y=Movil__Int[Movil__Int['País']== pais]['Upload'].values, name=pais,
        mode='markers',
        text=Movil__Int[Movil__Int['País']== pais]['Latency'],
        marker=dict(
            color=dict_coloresPais[pais],
            opacity=1,
            size=Movil__Int[Movil__Int['País']== pais]['Latency']),hovertemplate='<b>País:</b>'+pais+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad carga:</b>%{y:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
    fig2Int.update_xaxes(range=[0,130],tickangle=0, tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='tahoma',titlefont_size=18,title_text='Velocidad de descarga (Mbps)',ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
    fig2Int.update_yaxes(range=[0,20],tickfont=dict(family='Tahoma', color='black', size=18),titlefont_family='Tahoma',titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
    zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
    fig2Int.update_traces(textfont_size=18)
    fig2Int.update_layout(height=500,legend_title=None)
    fig2Int.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
    fig2Int.update_layout(font_color="Black",title_font_family="Tahoma",title_font_color="Black",titlefont_size=18)

    fig2Int.update_layout(height=600,   
        title='<b>Diagrama de burbujas de indicadores de desempeño en Internet móvil por país<br>(Diciembre 2022)',
        title_x=0.5,
        font=dict(
            family="Tahoma",
            color=" black",size=16))
    fig2Int.update_layout(legend=dict(y=0.1,x=0.8,font_size=17))
    fig2Int.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    fig2Int.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2Int, use_container_width=True) 