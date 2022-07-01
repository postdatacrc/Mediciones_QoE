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

# st.markdown("""
# <div class="barra-superior">
    # <div class="imagen-flotar" style="height: 80px; left: 10px; padding:15px">
        # <a class="imagen-flotar" style="float:left;" href="https://www.crcom.gov.co" title="CRC">
            # <img src="https://postdata.gov.co/sites/all/themes/nuboot_radix/logo-crc-blanco.png" alt="CRC" style="height:40px">
        # </a>
        # <a class="imagen-flotar" style="padding-left:10px;" href="https://postdata.gov.co" title="Postdata">
            # <img src="https://postdata.gov.co/sites/default/files/postdata-logo.png" alt="Inicio" style="height:40px">
        # </a>
    # </div>
    # <div class="imagen-flotar" style="height: 90px; left: 10px; padding:5px">
        # <a class="imagen-flotar" href="https://www.crcom.gov.co" title="CRC">
            # <img src="https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Banner_StreamLit.png" alt="CRC" style="">
        # </a>
    # </div>
# </div>""",unsafe_allow_html=True)
st.markdown("""<style type="text/css">
    h1{ 
        background: #ffde00;
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
        border-left: 10px solid #27348b;
        background: #fffdf7;
        font-size:10px,
        padding: 0px;
        color: black;}
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

st.markdown("""<b>1. Seleccione el servicio sobre el cual desea conocer la información de los indicadores de desempeño</b>""", unsafe_allow_html=True)

select_servicio = st.selectbox('Servicio',
                                    ['Información general','Internet fijo','Internet móvil','Comparación internacional'])

if select_servicio=='Información general':
    st.markdown('La Comisión de regulación de comunicaciones presenta la aplicación interactiva que contiene información sobre la calidad de los servicios ofrecidos a través de redes móviles y fijas por los diferentes proveedores en el territorio nacional, para el periodo comprendido entre los años 2018 y 2021.')
    st.markdown('Las mediciones de calidad que soportan las gráficas de la aplicación están basadas en la metodología crowdsourcing, utilizando para ellos los datos proporcionados por la aplicación Speedtest®, desarrollada por la empresa Ookla®. A través de esta metodología se recopila información directamente desde los dispositivos que los usuarios utilizan para acceder a los servicios de Internet móvil e Internet fijo, suministrados por los proveedores de redes y servicios de telecomunicaciones.')
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
     fill_color=dict_serv_colores[Servidores.iloc[i]['server_name']],
     fill_opacity=0.2
       ).add_to(Sevidores_map) 
       
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### <b>Distribución de servidores de pruebas en Colombia</b>",unsafe_allow_html=True)
        st.markdown('Las mediciones de los indicadores de calidad se soportan en el uso de una red que para 2021 incorporaba 38 servidores de prueba dispersos en el territorio nacional. Estas se muestran en el mapa a continuación.')    
        st.markdown("")
        folium_static(Sevidores_map,width=350)  
        st.markdown(r"""<p style=font-size:10px>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021. 
        Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.</p>""",unsafe_allow_html=True)
    with col2:
        st.markdown("### Definición indicadores de calidad",unsafe_allow_html=True)
        st.markdown("Los indicadores de calidad pueden ser divididos en 2 categorías: Indicadores de desempeño, e Indicadores de cobertura. A continuación se da paso a las definiciones de cada uno, y su relación con el servicio que experimenta el usuario.")
        select_indicadorDef=st.selectbox('Escoja la categoría',['Indicadores de desempeño','Indicadores de cobertura'])
        if select_indicadorDef=='Indicadores de desempeño': 
            st.markdown("#### Indicadores de desempeño")
            st.markdown("el rendimiento o desempeño del servicio de internet se refiere a los resultados de los indicadores de calidad del servicio de telecomunicaciones desde el punto de vista del usuario. Los más relevantes están relacionados con las velocidades y los tiempos de retardo de las conexiones.")
            with st.expander("Velocidad de descarga"):
                st.markdown("La velocidad de descarga Se entiende como la rapidez con la se pueden descargar contenidos, normalmente desde una página Web. A mayor velocidad obtenida en la medición, mayor rapidez en la descarga, por lo tanto, mejor experiencia del usuario. Es usual medirla en  Megabit por segundo (Mbps)")
            with st.expander("Velocidad de carga"):
                st.markdown("La velocidad de carga se entiende como la medida de qué tan rápido se envían los datos en dirección desde un dispositivo hacia Internet. Es decir, es la rapidez con la que se pueden subir contenidos a Internet. A mayor velocidad obtenida en la medición, mayor rapidez en la carga, por lo tanto, mejor es la experiencia del usuario. Se mide en Mebagit por segundo (Mbps)")
            with st.expander("Latencia"):
                st.markdown("El parámetro de latencia sirve para medir qué tan rápido viajan los datos desde un punto de origen al destino. La experiencia al intentar acceder a audio, video y videojuegos es mejor con latencias más bajas, por lo cual, si el tiempo obtenido en la medición es pequeño, la experiencia del usuario es mejor. La latencia se mide en milisegundos (ms).")
        if select_indicadorDef=='Indicadores de cobertura':
            st.markdown("#### Indicadores de cobertura")
            st.markdown("se refiere a indicadores relacionados con la distribución geográfica de los servicios de un operador móvil")
            with st.expander("Registro en red"):
                st.markdown("Es una métrica que indica la proporción del registro de los dispositivos de los usuarios en la red móvil de acuerdo con la tecnología de esta (para este documento incluye 2G, 3G, 4G y Roaming Automático Nacional - RAN).")
            with st.expander("Registro en red 4G"):
                st.markdown("Este indicador se refiere al porcentaje de usuarios que se registraron en las redes que suministran servicios móviles solamente en la tecnología 4G (incluido el Roaming Automático Nacional - RAN).")






        
#################################Lectura de bases Internet fijo#######################################33
pathFijo='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Fijo/'

####Primera sección - Fijo
@st.cache(allow_output_mutation=True)
def Seccion1Fijo():
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
    return Colombia1Fijo
Colombia1Fijo=Seccion1Fijo()

####Segunda sección - Fijo
@st.cache(allow_output_mutation=True)
def Seccion2Fijo():
    df2_1Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2018-12-01.csv',delimiter=';')
    df2_2Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2019-12-01.csv',delimiter=';')
    df2_3Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2020-12-01.csv',delimiter=';')
    df2_4Fijo=pd.read_csv(pathFijo+'Fij-ETBMOVCLA-historical_2022-01-01.csv',delimiter=';')
    df2_5Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2018-12-01.csv',delimiter=';')
    df2_6Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2019-12-01.csv',delimiter=';')
    df2_7Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2020-12-01.csv',delimiter=';')
    df2_8Fijo=pd.read_csv(pathFijo+'Fij-TIGOEMCALI-historical_2022-01-01.csv',delimiter=';').dropna(how='all') 
    OpCiud2Fijo=pd.concat([df2_1Fijo,df2_2Fijo,df2_3Fijo,df2_4Fijo,df2_5Fijo,df2_6Fijo,df2_7Fijo,df2_8Fijo])
    return OpCiud2Fijo
OpCiud2Fijo=Seccion2Fijo()    
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
@st.cache(allow_output_mutation=True)
def Seccion3Fijo():
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
    Ciudades3Fijo=pd.concat([df3_1Fijo,df3_2Fijo,df3_3Fijo,df3_4Fijo,df3_5Fijo,df3_6Fijo,df3_7Fijo,df3_8Fijo,df3_9Fijo,df3_10Fijo])#Unir los dataframes
    return Ciudades3Fijo
Ciudades3Fijo=Seccion3Fijo()
Ciudades3Fijo['Aggregate Date']=Ciudades3Fijo['Aggregate Date'].astype('str')    
Ciudades3Fijo['Aggregate Date']=Ciudades3Fijo['Aggregate Date'].replace(" ", "-").str.title() #Unir espacios blancos 
Ciudades3Fijo['Location']=Ciudades3Fijo['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntig3Fijo=Ciudades3Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre3Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction3Fijo=dict(zip(FeAntig3Fijo, FeCorre3Fijo))
Ciudades3Fijo['Aggregate Date'].replace(diction3Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Ciudades3Fijo['Aggregate Date'] = pd.to_datetime(Ciudades3Fijo['Aggregate Date'],errors='coerce')
Ciudades3Fijo['year']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).year
Ciudades3Fijo['month']=pd.DatetimeIndex(Ciudades3Fijo['Aggregate Date']).month
Ciudades3Fijo=Ciudades3Fijo.drop(['Device','Platform','Technology Type','Metric Type','Provider'], axis=1)


####Cuarta sección - Fijo
@st.cache(allow_output_mutation=True)
def Seccion4Fijo():
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
    return Operadores4Fijo
Operadores4Fijo=Seccion4Fijo()    
FeAntig4Fijo=Operadores4Fijo['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorre4Fijo=pd.date_range('2018-01-01','2022-01-01', 
              freq='MS').strftime("%d-%b-%y").tolist() #lista de fechas en el periodo seleccionado
diction4Fijo=dict(zip(FeAntig4Fijo, FeCorre4Fijo))
Operadores4Fijo['Aggregate Date'].replace(diction4Fijo, inplace=True) #Reemplazar fechas antiguas por nuevas
Operadores4Fijo['Aggregate Date'] =pd.to_datetime(Operadores4Fijo['Aggregate Date']).dt.floor('d') 
Operadores4Fijo['month']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).month
Operadores4Fijo['year']=pd.DatetimeIndex(Operadores4Fijo['Aggregate Date']).year
Operadores4Fijo=Operadores4Fijo.drop(['Location','Device','Platform','Technology Type','Metric Type'],axis=1)

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




if select_servicio == 'Internet fijo':
    select_indicador=st.selectbox('Indicador de desempeño',['Velocidad de descarga','Velocidad de carga','Latencia'])
    
    if select_indicador== 'Velocidad de descarga':
        dimension_Vel_descarga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        if dimension_Vel_descarga_Fijo == 'Histórico Colombia':

            Downspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Download Speed Mbps'].mean().round(2).reset_index()
            Downspeed1Fijo=Downspeed1Fijo[Downspeed1Fijo['Aggregate Date']<'2022-01-01']
            Downspeed1Fijo['Aggregate Date']=Downspeed1Fijo['Aggregate Date'].astype('str')
            
            fig1Fijo = make_subplots(rows=1, cols=1)
            fig1Fijo.add_trace(go.Scatter(x=Downspeed1Fijo['Aggregate Date'].values, y=Downspeed1Fijo['Download Speed Mbps'].values,
                                     line=dict(color='blue', width=2),name=' ',mode='lines+markers',fill='tonexty', fillcolor='rgba(0,0,255,0.2)'),row=1, col=1)
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
            'text': "<b>Velocidad promedio mensual de descarga de internet fijo en <br>Colombia (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig1Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig1Fijo, use_container_width=True)
            #st.download_button(label="Descargar CSV",data=convert_df(Downspeed1Fijo),file_name='Historico_descarga_Colombia.csv',mime='text/csv')


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
            
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]    
            Col2Fijo=Colombia2Fijo[(Colombia2Fijo['year']==2021)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Download Speed Mbps'].mean()
            Col2Fijo=round(Col2Fijo,2)
            departamentos_df2Fijo=gdf2.merge(Col2Fijo, on='Location')
            departamentos_df2Fijo=departamentos_df2Fijo.sort_values(by='Download Speed Mbps')

            # create a plain world map
            colombia_map1Fijo = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
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
            
            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Velocidad promedio de descarga de internet fijo en Colombia por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
#            with col2b:
            folium_static(colombia_map1Fijo,width=480) 
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
                
        if dimension_Vel_descarga_Fijo == 'Ciudades':    

            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]     
            
            df18A3Fijo=pd.DataFrame();df19A3Fijo=pd.DataFrame();df20A3Fijo=pd.DataFrame();df21A3Fijo=pd.DataFrame()
            p18A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2018)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p19A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p20A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            p21A3Fijo=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Download Speed Mbps']]).groupby(['Location'])['Download Speed Mbps'].mean()
            df18A3Fijo['Location']=p18A3Fijo.index;df18A3Fijo['2018']=p18A3Fijo.values;
            df19A3Fijo['Location']=p19A3Fijo.index;df19A3Fijo['2019']=p19A3Fijo.values;
            df20A3Fijo['Location']=p20A3Fijo.index;df20A3Fijo['2020']=p20A3Fijo.values;
            df21A3Fijo['Location']=p21A3Fijo.index;df21A3Fijo['2021']=p21A3Fijo.values;
            from functools import reduce
            DepJoinA3Fijo=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18A3Fijo,df19A3Fijo,df20A3Fijo,df21A3Fijo]).set_index('Location')
            DepJoinA3Fijo=DepJoinA3Fijo.round(2).reset_index()
            DepJoinA3Fijo=DepJoinA3Fijo[DepJoinA3Fijo.Location != 'Colombia']
            DepJoinA3Fijo=DepJoinA3Fijo.sort_values(by=['2021'],ascending=False)
            DepJoinA3Fijo['relatGrow']=100*np.abs(DepJoinA3Fijo['2021']-DepJoinA3Fijo['2020'])/DepJoinA3Fijo['2020']
            DepJoinA3Fijo['absGrow']=DepJoinA3Fijo['2021']-DepJoinA3Fijo['2020']
            DepJoinA3Fijocopy=DepJoinA3Fijo.copy()
            DepJoinA3Fijocopy['2018']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2018'],1).astype(str)]
            DepJoinA3Fijocopy['2019']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2019'],1).astype(str)]
            DepJoinA3Fijocopy['2020']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2020'],1).astype(str)]
            DepJoinA3Fijocopy['2021']=[x.replace('.', ',') for x in round(DepJoinA3Fijocopy['2021'],1).astype(str)]
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
            fig2Fijo =go.Figure()
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2018'],
            name=mes_opFijo+' 2018',
            marker_color='rgb(213,3,85)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2019'],
            name=mes_opFijo+' 2019',
            marker_color='rgb(255,152,0)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2020'],
            name=mes_opFijo+' 2020',
            marker_color='rgb(44,198,190)',textposition = "inside"))
            fig2Fijo.add_trace(go.Bar(
            x=DepJoinA3Fijo['Location'],
            y=DepJoinA3Fijo['2021'],
            name=mes_opFijo+' 2021',
            marker_color='rgb(72,68,242)',textposition = "outside"))
            fig2Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig2Fijo.update_yaxes(range=[0,max(DepJoinA3Fijo['2021'].values.tolist())+5],tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text="Velocidad descarga promedio (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig2Fijo.update_traces(textfont_size=14)
            fig2Fijo.update_layout(height=500,width=1200,legend_title=None)
            fig2Fijo.update_layout(legend=dict(orientation="h",yanchor='top',xanchor='center',x=0.5,y=1))
            fig2Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig2Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,font=dict(size=14),
            title={
            'text': "<b>Velocidad promedio anual de descarga de internet fijo por ciudad<br> (2018-2021) </b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig2Fijo.update_layout(barmode='group')
            fig2Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.4)
            st.plotly_chart(fig2Fijo, use_container_width=True)  
            
            col1, col2 = st.columns(2)
            with col1:
                Año_opFijo20 = st.selectbox('Escoja el año',[2018,2019,2020],index=2)
            with col2:
                mes_opFijo21 = st.slider('Escoja mes del 2021',1,12,12)             
            name_mes2={1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
            Dic20=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==Año_opFijo20)&(Ciudades3Fijo['month']==12)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            Dic21=Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes_opFijo21)][['Location','Latency','Download Speed Mbps', 'Upload Speed Mbps']]
            Dic20List=Dic20['Location'].unique().tolist()
            Dic21List=Dic21['Location'].unique().tolist()
            if 'Colombia' in Dic20List:
                Dic20List.remove('Colombia')
            if 'Colombia' in Dic21List:
                Dic21List.remove('Colombia')            
            dict_coloresFijo={'Bucaramanga':'rgb(255,128,0)','Bogotá':'rgb(255,0,0)','Cali':'rgb(255,255,0)',
                 'Medellín':'rgb(128,255,0)','Barranquilla':'rgb(0,255,0)','Cartagena':'rgb(0,255,128)',
                 'Villavicencio':'rgb(255,102,102)','Ibagué':'rgb(0,128,255)','Manizales':'rgb(0,0,255)',
                 'Tunja':'rgb(127,0,255)','Pasto':'rgb(255,0,255)','Santa Marta':'rgb(255,0,127)',
                 'Sincelejo':'rgb(128,128,128)','Armenia':'rgb(102,0,0)','Montería':'rgb(0,255,255)',
                 'Pereira':'rgb(0,51,51)','Popayán':'rgb(51,0,25)'}
            fig4Fijo = make_subplots(rows=1, cols=2,subplot_titles=('Diciembre '+str(Año_opFijo20),
            name_mes2[mes_opFijo21]+" 2021"))

            for location in Dic20List:
                fig4Fijo.add_trace(go.Scatter(
                    x=Dic20[Dic20['Location']==location]['Download Speed Mbps'].values, y=Dic20[Dic20['Location']==location]['Upload Speed Mbps'].values, 
                    mode='markers',
                    marker=dict(
                        color=dict_coloresFijo[location],
                        opacity=0.7,
                        size=Dic20[Dic20['Location']==location]['Latency'].values,
                    ),
                text=Dic20[Dic20['Location']==location]['Latency'].values,showlegend=False,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
                
            for location in Dic21List:
                fig4Fijo.add_trace(go.Scatter(
                    x=Dic21[Dic21['Location']==location]['Download Speed Mbps'].values, y=Dic21[Dic21['Location']==location]['Upload Speed Mbps'].values, name=location,
                    mode='markers',
                    marker=dict(
                        color=dict_coloresFijo[location],
                        opacity=0.7,
                        size=Dic21[Dic21['Location']==location]['Latency'].values,
                    ),
                text=Dic21[Dic21['Location']==location]['Latency'].values,hovertemplate='<b>Ciudad:</b>'+location+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=2)


            fig4Fijo.update_xaxes(tickangle=0,range=[0,max(Dic21['Download Speed Mbps'].values.tolist())+10],tickfont=dict(family='Arial', color='black', size=16),ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig4Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=16,ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig4Fijo.update_traces(textfont_size=14)
            fig4Fijo.update_layout(height=700,legend_title=None)
            fig4Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig4Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b> Diagrama de burbujas para velocidad de descarga, carga y latencia <br> en el internet fijo por ciudad</b>",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  

            fig4Fijo.update_xaxes(showspikes=True,title_text='Velocidad de descarga (Mbps)')
            fig4Fijo.update_yaxes(showspikes=True,range=[0,max(Dic21['Upload Speed Mbps'].values.tolist())+10],title_text="Velocidad de carga (Mbps)", row=1, col=1)
            fig4Fijo.update_yaxes(showspikes=True,range=[0,max(Dic21['Upload Speed Mbps'].values.tolist())+10],title_text=None, row=1, col=2)
            fig4Fijo.update_layout(legend=dict(y=0.95,x=1,orientation='v'))
            fig4Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.15)            
            st.plotly_chart(fig4Fijo, use_container_width=True)
            
        if dimension_Vel_descarga_Fijo == 'Operadores': 
            TodosDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            TodosDescarga4Fijo=TodosDescarga4Fijo[TodosDescarga4Fijo['Aggregate Date']<'2022-01-01']
            TodosDescarga4Fijo['Aggregate Date']=TodosDescarga4Fijo['Aggregate Date'].astype('str')
            ETBDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            ETBDescarga4Fijo=ETBDescarga4Fijo[ETBDescarga4Fijo['Aggregate Date']<'2022-01-01']
            ETBDescarga4Fijo['Aggregate Date']=ETBDescarga4Fijo['Aggregate Date'].astype('str')
            MOVISTARDescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            MOVISTARDescarga4Fijo=MOVISTARDescarga4Fijo[MOVISTARDescarga4Fijo['Aggregate Date']<'2022-01-01']
            MOVISTARDescarga4Fijo['Aggregate Date']=MOVISTARDescarga4Fijo['Aggregate Date'].astype('str')
            CLARODescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            CLARODescarga4Fijo=CLARODescarga4Fijo[CLARODescarga4Fijo['Aggregate Date']<'2022-01-01']
            CLARODescarga4Fijo['Aggregate Date']=CLARODescarga4Fijo['Aggregate Date'].astype('str')
            TIGODescarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Download Speed Mbps'].mean().reset_index()
            TIGODescarga4Fijo=TIGODescarga4Fijo[TIGODescarga4Fijo['Aggregate Date']<'2022-01-01']
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

            fig3Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=12),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig3Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Velocidad descarga promedio<br>(Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig3Fijo.update_traces(textfont_size=14)
            fig3Fijo.update_layout(height=500,legend_title=None,font=dict(size=14))
            fig3Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.01),showlegend=True)
            fig3Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig3Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,
            title={
            'text': "<b>Velocidad promedio mensual de descarga de Internet fijo<br>por proveedor (2018-2021) (en Mbps)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig3Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01'])
            fig3Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig3Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosDescarga4Fijo),file_name='Historico_descarga_Operadores.csv',mime='text/csv')            
            
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo] 
            
            Proveedor1Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
            Proveedor1Fijo['Download Speed Mbps'] =round(Proveedor1Fijo['Download Speed Mbps'], 2)
            final_df1Fijo=gdf2.merge(Proveedor1Fijo, on='Location')
            final_df1Fijo=final_df1Fijo[final_df1Fijo['Location'].isin(['GUAVIARE','SAN ANDRES Y PROVIDENCIA'])==False]

            ##
            Proveedor2Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
            Proveedor2Fijo['Download Speed Mbps'] =round(Proveedor2Fijo['Download Speed Mbps'], 2)
            final_df2Fijo=gdf2.merge(Proveedor2Fijo, on='Location')
            ##
            Proveedor3Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
            Proveedor3Fijo['Download Speed Mbps'] =round(Proveedor3Fijo['Download Speed Mbps'], 2)
            final_df3Fijo=gdf2.merge(Proveedor3Fijo, on='Location')
            ##
            Proveedor4Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
            Proveedor4Fijo['Download Speed Mbps'] =round(Proveedor4Fijo['Download Speed Mbps'], 2)
            final_df4Fijo=gdf2.merge(Proveedor4Fijo, on='Location')
            

            dualmap1_1Fijo=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

            dualmap1_1Fijo.m1.add_child(NIL1)
            dualmap1_1Fijo.m1.keep_in_front(NIL1)
            dualmap1_1Fijo.m2.add_child(NIL2)
            dualmap1_1Fijo.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_1Fijo.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_1Fijo.m2)

            dualmap1_2Fijo=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
                st.markdown("<center><b> Velocidad promedio de descarga de internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
#            with col2b:
            folium_static(dualmap1_1Fijo,width=800) 
            folium_static(dualmap1_2Fijo,width=800)  
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

           
            etb=Operadores4Fijo[Operadores4Fijo['Provider']=='ETB'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            claro=Operadores4Fijo[Operadores4Fijo['Provider']=='Claro'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            movistar=Operadores4Fijo[Operadores4Fijo['Provider']=='Movistar'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]
            tigo=Operadores4Fijo[Operadores4Fijo['Provider']=='Tigo'][['Latency','Download Speed Mbps','Upload Speed Mbps','year']]     

            dict_color_periodos={2018:'rgb(213,3,85)',2019:'rgb(255,152,0)',2020:'rgb(44,198,190)',2021:'rgb(72,68,242)'}
            fig5Fijo = make_subplots(rows=2, cols=2,subplot_titles=("<b>ETB</b>",
                "<b>CLARO</b>","<b>MOVISTAR</b>","<b>TIGO</b>"),vertical_spacing=0.1)  
            for año in [2018,2019,2020,2021]:  
                fig5Fijo.add_trace(go.Scatter(
                x=etb[etb['year']==año]['Download Speed Mbps'].values, y=etb[etb['year']==año]['Upload Speed Mbps'].values,showlegend=True, name=año,
                mode='markers',
                marker=dict(
                    color=dict_color_periodos[año],
                    opacity=0.7,
                    size=0.5*etb[etb['year']==año]['Latency'].values,
                ),legendgroup = '1',
                text=0.5*etb[etb['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)

                fig5Fijo.add_trace(go.Scatter(
                x=claro[claro['year']==año]['Download Speed Mbps'].values, y=claro[claro['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                mode='markers',
                marker=dict(
                    color=dict_color_periodos[año],
                    opacity=0.7,
                    size=0.5*claro[claro['year']==año]['Latency'].values,
                ),legendgroup = '1',
                text=0.5*claro[claro['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=2)

                fig5Fijo.add_trace(go.Scatter(
                x=movistar[movistar['year']==año]['Download Speed Mbps'].values, y=movistar[movistar['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                mode='markers',
                marker=dict(
                    color=dict_color_periodos[año],
                    opacity=0.7,
                    size=0.5*movistar[movistar['year']==año]['Latency'].values,
                ),legendgroup = '1',
                text=0.5*movistar[movistar['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=2, col=1)
                
                fig5Fijo.add_trace(go.Scatter(
                x=tigo[tigo['year']==año]['Download Speed Mbps'].values, y=tigo[tigo['year']==año]['Upload Speed Mbps'].values,showlegend=False, name=año,
                mode='markers',
                marker=dict(
                    color=dict_color_periodos[año],
                    opacity=0.7,
                    size=0.5*tigo[tigo['year']==año]['Latency'].values,
                ),legendgroup = '1',
                text=0.5*tigo[tigo['year']==año]['Latency'].values,hovertemplate='<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=2, col=2)    
                
            fig5Fijo.add_shape(type="line",
                x0=0, y0=0, x1=135, y1=135,
                line=dict(
                    color="indianred",
                    width=4,
                    dash="dot",
                ),row=1,col=1)
            fig5Fijo.add_shape(type="line",
                x0=0, y0=0, x1=135, y1=135,
                line=dict(
                    color="indianred",
                    width=4,
                    dash="dot",
                ),row=1,col=2)
            fig5Fijo.add_shape(type="line",
                x0=0, y0=0, x1=135, y1=135,
                line=dict(
                    color="indianred",
                    width=4,
                    dash="dot",
                ),row=2,col=1)
            fig5Fijo.add_shape(type="line",
                x0=0, y0=0, x1=135, y1=135,
                line=dict(
                    color="indianred",
                    width=4,
                    dash="dot",
                ),row=2,col=2)
            ###################################


            fig5Fijo.update_xaxes(range=[0,135],tickangle=0,tickfont=dict(family='Arial', color='black', size=16),ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig5Fijo.update_yaxes(range=[0,135],tickfont=dict(family='Arial', color='black', size=16),titlefont_size=16,ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig5Fijo.update_traces(textfont_size=14)
            fig5Fijo.update_layout(height=700,legend_title=None)
            fig5Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig5Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b> Diagrama de burbujas para velocidad de descarga, carga y latencia <br> en el internet fijo por operador</b>",
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
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-1.55)             
            st.plotly_chart(fig5Fijo, use_container_width=True)  

    if select_indicador== 'Velocidad de carga':
        dimension_Vel_carga_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        if dimension_Vel_carga_Fijo == 'Histórico Colombia':
            Upspeed1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            Upspeed1Fijo=Upspeed1Fijo[Upspeed1Fijo['Aggregate Date']<'2022-01-01']
            Upspeed1Fijo['Aggregate Date']=Upspeed1Fijo['Aggregate Date'].astype('str')
            fig6Fijo = make_subplots(rows=1, cols=1)
            fig6Fijo.add_trace(go.Scatter(x=Upspeed1Fijo['Aggregate Date'].values, y=Upspeed1Fijo['Upload Speed Mbps'].values,
                                     line=dict(color='red', width=2),mode='lines+markers',fill='tonexty', fillcolor='rgba(255,0,0,0.2)'),row=1, col=1)
            fig6Fijo.update_xaxes(tickvals=['2018-01-01','2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01'])
            fig6Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig6Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad carga<br>(Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig6Fijo.update_traces(textfont_size=18)
            fig6Fijo.update_layout(height=500,legend_title=None)
            #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            fig6Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            fig6Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio mensual de carga de Internet fijo<br>en Colombia (2018-2021) (en Mbps)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig6Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig6Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Upspeed1Fijo),file_name='Historico_carga_Colombia.csv',mime='text/csv')
            
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]    

            Col2bFijo=Colombia2Fijo[(Colombia2Fijo['year']==2021)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Upload Speed Mbps'].mean()
            Col2bFijo=round(Col2bFijo,2)
            departamentos_df2bFijo=gdf2.merge(Col2bFijo, on='Location')
            departamentos_df2bFijo=departamentos_df2bFijo.sort_values(by='Upload Speed Mbps')  

            colombia_map2Fijo = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
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
            colombia_map2Fijo.add_child(NIL)
            colombia_map2Fijo.keep_in_front(NIL)

            with col2:
                st.markdown("<center><b> Velocidad promedio de carga de internet fijo en Colombia por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([2,4,1])
#            with col2b:
            folium_static(colombia_map2Fijo,width=480) 
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Fijo == 'Ciudades':    
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]  
            
            df18B3=pd.DataFrame();df19B3=pd.DataFrame();df20B3=pd.DataFrame();df21B3=pd.DataFrame()
            p18B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2018)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p19B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p20B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            p21B3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Upload Speed Mbps']]).groupby(['Location'])['Upload Speed Mbps'].mean()
            df18B3['Location']=p18B3.index;df18B3['2018']=p18B3.values;
            df19B3['Location']=p19B3.index;df19B3['2019']=p19B3.values;
            df20B3['Location']=p20B3.index;df20B3['2020']=p20B3.values;
            df21B3['Location']=p21B3.index;df21B3['2021']=p21B3.values;
            from functools import reduce
            DepJoinB3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18B3,df19B3,df20B3,df21B3]).set_index('Location')
            DepJoinB3=DepJoinB3.round(2).reset_index()
            DepJoinB3 = DepJoinB3[DepJoinB3.Location != 'Colombia']
            DepJoinB3 = DepJoinB3.sort_values(by=['2021'],ascending=False)
            DepJoinB3['relatGrow']=100*(DepJoinB3['2021']-DepJoinB3['2020'])/DepJoinB3['2020']
            DepJoinB3['absGrow']=DepJoinB3['2021']-DepJoinB3['2020']
            DepJoinBcopy3=DepJoinB3.copy()
            DepJoinBcopy3['2018']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2018'],1).astype(str)]
            DepJoinBcopy3['2019']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2019'],1).astype(str)]
            DepJoinBcopy3['2020']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2020'],1).astype(str)]
            DepJoinBcopy3['2021']=[x.replace('.', ',') for x in round(DepJoinBcopy3['2021'],1).astype(str)]
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}
            fig7Fijo = go.Figure()
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2018'],
                name=mes_opFijo+' 2018',
                marker_color='rgb(213,3,85)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2019'],
                name=mes_opFijo+' 2019',
                marker_color='rgb(255,152,0)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2020'],
                name=mes_opFijo+' 2020',
                marker_color='rgb(44,198,190)'))
            fig7Fijo.add_trace(go.Bar(
                x=DepJoinB3['Location'],
                y=DepJoinB3['2021'],
                name=mes_opFijo+' 2021',
                marker_color='rgb(72,68,242)'))

            fig7Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig7Fijo.update_yaxes(range=[0,max(DepJoinB3['2021'].values.tolist())+5],tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text="Velocidad carga promedio (Mbps)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig7Fijo.update_traces(textfont_size=22)
            fig7Fijo.update_layout(height=500,width=1200,legend_title=None)
            fig7Fijo.update_layout(legend=dict(orientation="h",y=1,xanchor='center',x=0.5))
            fig7Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig7Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,font=dict(size=14),
            title={
            'text': "<b>Velocidad promedio anual de carga de internet fijo por ciudad<br> (2018-2021)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig7Fijo.update_layout(barmode='group')
            fig7Fijo.update_layout(uniformtext_minsize=22, uniformtext_mode='show')
            fig7Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.4)             
            st.plotly_chart(fig7Fijo, use_container_width=True)  
            
        if dimension_Vel_carga_Fijo == 'Operadores':   
            TodosCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            TodosCarga4Fijo=TodosCarga4Fijo[TodosCarga4Fijo['Aggregate Date']<'2022-01-01']
            TodosCarga4Fijo['Aggregate Date']=TodosCarga4Fijo['Aggregate Date'].astype('str')
            ETBCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            ETBCarga4Fijo=ETBCarga4Fijo[ETBCarga4Fijo['Aggregate Date']<'2022-01-01']
            ETBCarga4Fijo['Aggregate Date']=ETBCarga4Fijo['Aggregate Date'].astype('str')
            MOVISTARCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            MOVISTARCarga4Fijo=MOVISTARCarga4Fijo[MOVISTARCarga4Fijo['Aggregate Date']<'2022-01-01']
            MOVISTARCarga4Fijo['Aggregate Date']=MOVISTARCarga4Fijo['Aggregate Date'].astype('str')
            CLAROCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            CLAROCarga4Fijo=CLAROCarga4Fijo[CLAROCarga4Fijo['Aggregate Date']<'2022-01-01']
            CLAROCarga4Fijo['Aggregate Date']=CLAROCarga4Fijo['Aggregate Date'].astype('str')
            TIGOCarga4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Upload Speed Mbps'].mean().reset_index()
            TIGOCarga4Fijo=TIGOCarga4Fijo[TIGOCarga4Fijo['Aggregate Date']<'2022-01-01']  
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

            fig8Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=12),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig8Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Velocidad de carga promedio<br>(Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig8Fijo.update_traces(textfont_size=14)
            fig8Fijo.update_layout(height=500,legend_title=None,font=dict(size=14))
            fig8Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.01),showlegend=True)
            fig8Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig8Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,
            title={
            'text': "<b>Velocidad promedio mensual de carga de Internet fijo<br>por proveedor (2018-2021) (en Mbps)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig8Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01'])
            fig8Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig8Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosCarga4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')            

            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo] 

            Proveedor1bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
            Proveedor1bFijo['Upload Speed Mbps'] =round(Proveedor1bFijo['Upload Speed Mbps'], 2)
            final_df1bFijo=gdf2.merge(Proveedor1bFijo, on='Location')
            final_df1bFijo=final_df1bFijo[final_df1bFijo['Location'].isin(['GUAVIARE','SAN ANDRES Y PROVIDENCIA'])==False]
            ##
            Proveedor2bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
            Proveedor2bFijo['Upload Speed Mbps'] =round(Proveedor2bFijo['Upload Speed Mbps'], 2)
            final_df2bFijo=gdf2.merge(Proveedor2bFijo, on='Location')
            ##
            Proveedor3bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
            Proveedor3bFijo['Upload Speed Mbps'] =round(Proveedor3bFijo['Upload Speed Mbps'], 2)
            final_df3bFijo=gdf2.merge(Proveedor3bFijo, on='Location')
            ##
            Proveedor4bFijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
            Proveedor4bFijo['Upload Speed Mbps'] =round(Proveedor4bFijo['Upload Speed Mbps'], 2)
            final_df4bFijo=gdf2.merge(Proveedor4bFijo, on='Location') 


            dualmap1_3Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
            ########
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_4Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
                st.markdown("<center><b> Velocidad promedio de carga de internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_3Fijo,width=800) 
                folium_static(dualmap1_4Fijo,width=800)  
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
         
            
    if select_indicador== 'Latencia':            
        dimension_Latencia_Fijo = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)
        if dimension_Latencia_Fijo == 'Histórico Colombia':    
            Latency1Fijo=Colombia1Fijo.groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            Latency1Fijo=Latency1Fijo[Latency1Fijo['Aggregate Date']<'2022-01-01']
            Latency1Fijo['Aggregate Date']=Latency1Fijo['Aggregate Date'].astype('str')
            fig9Fijo = make_subplots(rows=1, cols=1)
            fig9Fijo.add_trace(go.Scatter(x=Latency1Fijo['Aggregate Date'].values, y=Latency1Fijo['Latency'].values,
                         line=dict(color='purple', width=2),mode='lines+markers',fill='tonexty', fillcolor='rgba(153,0,153,0.2)'),row=1, col=1)
            fig9Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig9Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=16, title_text='Latencia promedio<br>(ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig9Fijo.update_traces(textfont_size=16)
            fig9Fijo.update_layout(height=500,legend_title=None)
            #fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            fig9Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            fig9Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Latencia promedio mensual de Internet fijo en Colombia<br>(2018-2021)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig9Fijo.update_xaxes(tickvals=['2018-06-01','2018-12-01','2019-06-01','2019-12-01','2020-06-01','2020-12-01','2021-06-01','2021-12-01'])
            fig9Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.25)
            st.plotly_chart(fig9Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(Latency1Fijo),file_name='Historico_latencia_Colombia.csv',mime='text/csv')             

            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]    
                
            Servidores=pd.read_csv(pathFijo+'Fij-Servidores_Colombia.csv',encoding='latin-1',delimiter=';')
            Servidores['latitude']=Servidores['latitude'].str.replace(',','.')
            Servidores['longitude']=Servidores['longitude'].str.replace(',','.')
            ColLat2=Colombia2Fijo[(Colombia2Fijo['year']==2021)&(Colombia2Fijo['month']==mes)].groupby(['Location'])['Latency'].mean()
            ColLat2=round(ColLat2,2)
            departamentosLat_df2Fijo=gdf2.merge(ColLat2, on='Location')
            departamentosLat_df2Fijo=departamentosLat_df2Fijo.sort_values(by='Latency')
            
            colombia_map3Fijo = folium.Map(height=600,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
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

            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b>Latencia promedio internet fijo en Colombia por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([2,4,1])
            with col2b:
                folium_static(colombia_map3Fijo,width=480) 
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Latencia_Fijo == 'Ciudades':    
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]  
            
            df18C3=pd.DataFrame();df19C3=pd.DataFrame();df20C3=pd.DataFrame();df21C3=pd.DataFrame()
            p18C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2018)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p19C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2019)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p20C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2020)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            p21C3=(Ciudades3Fijo.loc[(Ciudades3Fijo['year']==2021)&(Ciudades3Fijo['month']==mes),['Location','Latency']]).groupby(['Location'])['Latency'].mean()
            df18C3['Location']=p18C3.index;df18C3['2018']=p18C3.values;
            df19C3['Location']=p19C3.index;df19C3['2019']=p19C3.values;
            df20C3['Location']=p20C3.index;df20C3['2020']=p20C3.values;
            df21C3['Location']=p21C3.index;df21C3['2021']=p21C3.values;
            from functools import reduce
            DepJoinC3=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18C3,df19C3,df20C3,df21C3]).set_index('Location')
            DepJoinC3=DepJoinC3.round(2).reset_index()
            DepJoinC3 = DepJoinC3[DepJoinC3.Location != 'Colombia']
            DepJoinC3 = DepJoinC3.sort_values(by=['2021'],ascending=True)
            DepJoinC3['relatGrow']=100*(DepJoinC3['2021']-DepJoinC3['2020'])/DepJoinC3['2020']
            DepJoinC3['absGrow']=DepJoinC3['2021']-DepJoinC3['2020']
            name_mes={1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}            
            fig10Fijo = go.Figure()
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2018'],
                name=mes_opFijo+' 2018',
                marker_color='rgb(213,3,85)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2019'],
                name=mes_opFijo+' 2019',
                marker_color='rgb(255,152,0)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2020'],
                name=mes_opFijo+' 2020',
                marker_color='rgb(44,198,190)'))
            fig10Fijo.add_trace(go.Bar(
                x=DepJoinC3['Location'],
                y=DepJoinC3['2021'],
                name=mes_opFijo+' 2021',
                marker_color='rgb(72,68,242)'))


            fig10Fijo.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig10Fijo.update_yaxes(range=[0,85],tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text="Latencia promedio (ms)",ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig10Fijo.update_traces(textfont_size=22)
            fig10Fijo.update_layout(height=500,width=1200,legend_title=None)
            fig10Fijo.update_layout(legend=dict(orientation="h",y=1.1,xanchor='center',x=0.5))
            fig10Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig10Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,font=dict(size=14),
            title={
            'text': "<b>Latencia promedio anual de internet fijo por ciudad en ms<br> (2018-2021) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig10Fijo.update_layout(barmode='group')
            fig10Fijo.update_layout(uniformtext_minsize=14, uniformtext_mode='show')
            fig10Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.4)                 
            st.plotly_chart(fig10Fijo, use_container_width=True)  

        if dimension_Latencia_Fijo == 'Operadores':  
            TodosLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='All Providers Combined'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            TodosLatencia4Fijo=TodosLatencia4Fijo[TodosLatencia4Fijo['Aggregate Date']<'2022-01-01']
            TodosLatencia4Fijo['Aggregate Date']=TodosLatencia4Fijo['Aggregate Date'].astype('str')
            ETBLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='ETB'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            ETBLatencia4Fijo=ETBLatencia4Fijo[ETBLatencia4Fijo['Aggregate Date']<'2022-01-01']
            ETBLatencia4Fijo['Aggregate Date']=ETBLatencia4Fijo['Aggregate Date'].astype('str')
            MOVISTARLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Movistar'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            MOVISTARLatencia4Fijo=MOVISTARLatencia4Fijo[MOVISTARLatencia4Fijo['Aggregate Date']<'2022-01-01']
            MOVISTARLatencia4Fijo['Aggregate Date']=MOVISTARLatencia4Fijo['Aggregate Date'].astype('str')
            CLAROLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Claro'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            CLAROLatencia4Fijo=CLAROLatencia4Fijo[CLAROLatencia4Fijo['Aggregate Date']<'2022-01-01']
            CLAROLatencia4Fijo['Aggregate Date']=CLAROLatencia4Fijo['Aggregate Date'].astype('str')
            TIGOLatencia4Fijo=Operadores4Fijo.loc[Operadores4Fijo['Provider']=='Tigo'].groupby(['Aggregate Date'])['Latency'].mean().reset_index()
            TIGOLatencia4Fijo=TIGOLatencia4Fijo[TIGOLatencia4Fijo['Aggregate Date']<'2022-01-01']
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

            fig11Fijo.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=12),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig11Fijo.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Latencia promedio<br>(ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig11Fijo.update_traces(textfont_size=14)
            fig11Fijo.update_layout(height=500,legend_title=None,font=dict(size=14))
            fig11Fijo.update_layout(legend=dict(orientation="v",y=1.02,x=0.87),showlegend=True)
            fig11Fijo.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig11Fijo.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,
            title={
            'text': "<b>Latencia promedio mensual de carga de internet fijo en <br> Colombia (2018-2021)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig11Fijo.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01'])
            fig11Fijo.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig11Fijo, use_container_width=True)  
            #st.download_button(label="Descargar CSV",data=convert_df(JuntosLatencia4Fijo),file_name='Historico_dcarga_Operadores.csv',mime='text/csv')   
            
            col1, col2,col3= st.columns(3)
            mes_opFijoNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opFijo = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opFijoNombre[mes_opFijo]  

            ProveedorLat1Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Claro')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
            ProveedorLat1Fijo['Latency'] =round(ProveedorLat1Fijo['Latency'], 2)
            final_dfLat1Fijo=gdf2.merge(ProveedorLat1Fijo, on='Location')
            final_dfLat1Fijo=final_dfLat1Fijo[final_dfLat1Fijo['Location'].isin(['GUAVIARE','SAN ANDRES Y PROVIDENCIA'])==False]
            ##
            ProveedorLat2Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Movistar')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
            ProveedorLat2Fijo['Latency'] =round(ProveedorLat2Fijo['Latency'], 2)
            final_dfLat2Fijo=gdf2.merge(ProveedorLat2Fijo, on='Location')
            ##
            ProveedorLat3Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='Tigo')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
            ProveedorLat3Fijo['Latency'] =round(ProveedorLat3Fijo['Latency'], 2)
            final_dfLat3Fijo=gdf2.merge(ProveedorLat3Fijo, on='Location')
            ##
            ProveedorLat4Fijo=OpCiud2Fijo.loc[(OpCiud2Fijo['Provider']=='ETB')&(OpCiud2Fijo['year']==2021)&(OpCiud2Fijo['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
            ProveedorLat4Fijo['Latency'] =round(ProveedorLat4Fijo['Latency'], 2)
            final_dfLat4Fijo=gdf2.merge(ProveedorLat4Fijo, on='Location')
            
            dualmap1_5Fijo=folium.plugins.DualMap(heigth=500,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron')
            ########
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_5Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
            choropleth=folium.Choropleth(
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
            choropleth=folium.Choropleth(
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_6Fijo.m1)
            choropleth.geojson.add_child(
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
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
                st.markdown("<center><b> Latencia promedio de internet fijo en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_5Fijo,width=800) 
                folium_static(dualmap1_6Fijo,width=800)  
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
 

#########################################################Lectura de bases Internet móvil#######################################

pathMovil='https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/'
#### Sección 1 Móvil
@st.cache(allow_output_mutation=True)
def ColombiaMovil1():
    Colombia1Movil=pd.read_csv(pathMovil+'Colombia/IndDesempe%C3%B1oMov_3G4G_(2018a2021_An).csv',encoding='latin1',error_bad_lines=False)  
    Colombia1Movil=Colombia1Movil.drop(['Device','Platform','Metric Type'], axis=1) #Eliminar columnas      
    return Colombia1Movil
Colombia1Movil=ColombiaMovil1()    
df3gAMovilDown=pd.DataFrame();df3gAMovilUp=pd.DataFrame();df3gAMovilLat=pd.DataFrame();
df4gAMovilDown=pd.DataFrame();df4gAMovilUp=pd.DataFrame();df4gAMovilLat=pd.DataFrame();
dfTotAMovilDown=pd.DataFrame();dfTotAMovilUp=pd.DataFrame();dfTotAMovilLat=pd.DataFrame()     
p3gAMovil=(Colombia1Movil.loc[(Colombia1Movil['Technology Type']=='3g'),['Aggregate Date','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Aggregate Date']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p4gAMovil=(Colombia1Movil.loc[(Colombia1Movil['Technology Type']=='lte'),['Aggregate Date','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Aggregate Date']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
pTotAMovil=(Colombia1Movil.loc[(Colombia1Movil['Technology Type']=='cellular'),['Aggregate Date','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Aggregate Date']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
df3gAMovilDown['year']=p3gAMovil.index; df3gAMovilDown['3g']=p3gAMovil['Download Speed Mbps'].values;
df4gAMovilDown['year']=p4gAMovil.index;df4gAMovilDown['4g']=p4gAMovil['Download Speed Mbps'].values;
dfTotAMovilDown['year']=pTotAMovil.index;dfTotAMovilDown['Total']=pTotAMovil['Download Speed Mbps'].values;
df3gAMovilUp['year']=p3gAMovil.index; df3gAMovilUp['3g']=p3gAMovil['Upload Speed Mbps'].values;
df4gAMovilUp['year']=p4gAMovil.index;df4gAMovilUp['4g']=p4gAMovil['Upload Speed Mbps'].values;
dfTotAMovilUp['year']=pTotAMovil.index;dfTotAMovilUp['Total']=pTotAMovil['Upload Speed Mbps'].values;
df3gAMovilLat['year']=p3gAMovil.index; df3gAMovilLat['3g']=p3gAMovil['Latency'].values;
df4gAMovilLat['year']=p4gAMovil.index;df4gAMovilLat['4g']=p4gAMovil['Latency'].values;
dfTotAMovilLat['year']=pTotAMovil.index;dfTotAMovilLat['Total']=pTotAMovil['Latency'].values;
DepJoinAMovilDown=reduce(lambda x,y: pd.merge(x,y, on='year', how='outer'), [df3gAMovilDown,df4gAMovilDown,dfTotAMovilDown]).round(2).reset_index()
DepJoinAMovilUp=reduce(lambda x,y: pd.merge(x,y, on='year', how='outer'), [df3gAMovilUp,df4gAMovilUp,dfTotAMovilUp]).round(2).reset_index()
DepJoinAMovilLat=reduce(lambda x,y: pd.merge(x,y, on='year', how='outer'), [df3gAMovilLat,df4gAMovilLat,dfTotAMovilLat]).round(2).reset_index()      
   

#### Sección 2 Móvil
@st.cache(allow_output_mutation=True)
def ColombiaMovil2():
    Colombia2Movil=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_Total(2021Mens).csv',encoding='latin-1') 
    Colombia2Movil['Location']=Colombia2Movil['Location'].str.split(',',expand=True)[0]#Guardar sólo departamentos
    FeAntig=Colombia2Movil['Aggregate Date'].unique() #Generar las fechas que tenían los datos
    FeCorre=pd.date_range('2021-01-01','2021-12-01', 
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

#### Sección 3 Móvil
@st.cache(allow_output_mutation=True)
def ColombiaMovil3():
    Colombia3Movil=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Operadores/IndDesempe%C3%B1oMov_Operad_(2018a2021_An).csv')
    Colombia3Movil=Colombia3Movil.drop(['Device','Platform','Metric Type','Location'],axis=1)
    #Colombia3Movil=Colombia3Movil.rename(columns={'ï»¿Provider':'Provider'})
    return Colombia3Movil
Colombia3Movil = ColombiaMovil3()
df18AMovil3=pd.DataFrame();df18AMovil3Up=pd.DataFrame();df18AMovil3Lat=pd.DataFrame();
df19AMovil3=pd.DataFrame();df19AMovil3Up=pd.DataFrame();df19AMovil3Lat=pd.DataFrame();
df20AMovil3=pd.DataFrame();df20AMovil3Up=pd.DataFrame();df20AMovil3Lat=pd.DataFrame();
df21AMovil3=pd.DataFrame();df21AMovil3Up=pd.DataFrame();df21AMovil3Lat=pd.DataFrame();
p18AMovil3=(Colombia3Movil.loc[(Colombia3Movil['Aggregate Date']==2018),['Provider','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Provider']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p19AMovil3=(Colombia3Movil.loc[(Colombia3Movil['Aggregate Date']==2019),['Provider','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Provider']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p20AMovil3=(Colombia3Movil.loc[(Colombia3Movil['Aggregate Date']==2020),['Provider','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Provider']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p21AMovil3=(Colombia3Movil.loc[(Colombia3Movil['Aggregate Date']==2021),['Provider','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Provider']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
df18AMovil3['Provider']=p18AMovil3.index; df18AMovil3['2018']=p18AMovil3['Download Speed Mbps'].values;
df19AMovil3['Provider']=p19AMovil3.index; df19AMovil3['2019']=p19AMovil3['Download Speed Mbps'].values;
df20AMovil3['Provider']=p20AMovil3.index; df20AMovil3['2020']=p20AMovil3['Download Speed Mbps'].values;
df21AMovil3['Provider']=p21AMovil3.index; df21AMovil3['2021']=p21AMovil3['Download Speed Mbps'].values;
df18AMovil3Up['Provider']=p18AMovil3.index; df18AMovil3Up['2018']=p18AMovil3['Upload Speed Mbps'].values;
df19AMovil3Up['Provider']=p19AMovil3.index; df19AMovil3Up['2019']=p19AMovil3['Upload Speed Mbps'].values;
df20AMovil3Up['Provider']=p20AMovil3.index; df20AMovil3Up['2020']=p20AMovil3['Upload Speed Mbps'].values;
df21AMovil3Up['Provider']=p21AMovil3.index; df21AMovil3Up['2021']=p21AMovil3['Upload Speed Mbps'].values;
df18AMovil3Lat['Provider']=p18AMovil3.index; df18AMovil3Lat['2018']=p18AMovil3['Latency'].values;
df19AMovil3Lat['Provider']=p19AMovil3.index; df19AMovil3Lat['2019']=p19AMovil3['Latency'].values;
df20AMovil3Lat['Provider']=p20AMovil3.index; df20AMovil3Lat['2020']=p20AMovil3['Latency'].values;
df21AMovil3Lat['Provider']=p21AMovil3.index; df21AMovil3Lat['2021']=p21AMovil3['Latency'].values;
DepJoinAMovil3=pd.concat([df18AMovil3,df19AMovil3,df20AMovil3,df21AMovil3]).round(2).reset_index()
DepJoinAMovil3Up=pd.concat([df18AMovil3Up,df19AMovil3Up,df20AMovil3Up,df21AMovil3Up]).round(2).reset_index()
DepJoinAMovil3Lat=pd.concat([df18AMovil3Lat,df19AMovil3Lat,df20AMovil3Lat,df21AMovil3Lat]).round(2).reset_index()
#### Sección 4 Móvil
@st.cache(allow_output_mutation=True)
def OpDepartMovil1():
    df1=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_MovAvanETB(2018).csv')
    df2=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_MovAvanETB(2019).csv')
    df3=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_MovAvanETB(2020).csv')
    df4=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_MovAvanETB(2021).csv')
    df5=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_TigWomCla(2018).csv')
    df6=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_TigWomCla(2019).csv')
    df7=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_TigWomCla(2020).csv')
    df8=pd.read_csv(pathMovil+'Departamentos/IndDesempe%C3%B1oMov_Dep_TigWomCla(2021).csv')
    OpCiudMovil1=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8])
    return OpCiudMovil1
OpCiudMovil1=OpDepartMovil1()
OpCiudMovil1['Location']=OpCiudMovil1['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
FeAntigMovil1=OpCiudMovil1['Aggregate Date'].unique() #Generar las fechas que tenían los datos
FeCorreMovil1=pd.date_range('2018-01-01','2021-12-01', 
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
#### Sección 5 Móvil
@st.cache(allow_output_mutation=True)
def CiudadMovil1():
    Ciudades=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Ciudades/IndDesempe%C3%B1oMov_Ciud_(2018a2021_An).csv')
    Ciudades['Location']=Ciudades['Location'].str.split(',',expand=True)[0]#Guardar sólo las ciudades
    Ciudades=Ciudades.drop(['Device','Platform','Metric Type','Provider'], axis=1) #Eliminar columnas
    return Ciudades
CiudadMovil1=CiudadMovil1()
df18A=pd.DataFrame();df18AUp=pd.DataFrame();df18ALat=pd.DataFrame();
df19A=pd.DataFrame();df19AUp=pd.DataFrame();df19ALat=pd.DataFrame();
df20A=pd.DataFrame();df20AUp=pd.DataFrame();df20ALat=pd.DataFrame();
df21A=pd.DataFrame();df21AUp=pd.DataFrame();df21ALat=pd.DataFrame();
p18A=(CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']==2018),['Location','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Location']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p19A=(CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']==2019),['Location','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Location']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p20A=(CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']==2020),['Location','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Location']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
p21A=(CiudadMovil1.loc[(CiudadMovil1['Aggregate Date']==2021),['Location','Download Speed Mbps','Upload Speed Mbps','Latency']]).groupby(['Location']).agg({'Download Speed Mbps':'mean','Upload Speed Mbps':'mean','Latency':'mean'})
df18A['Location']=p18A.index; df18A['2018']=p18A['Download Speed Mbps'].values;
df19A['Location']=p19A.index; df19A['2019']=p19A['Download Speed Mbps'].values;
df20A['Location']=p20A.index; df20A['2020']=p20A['Download Speed Mbps'].values;
df21A['Location']=p21A.index; df21A['2021']=p21A['Download Speed Mbps'].values;
df18AUp['Location']=p18A.index; df18AUp['2018']=p18A['Upload Speed Mbps'].values;
df19AUp['Location']=p19A.index; df19AUp['2019']=p19A['Upload Speed Mbps'].values;
df20AUp['Location']=p20A.index; df20AUp['2020']=p20A['Upload Speed Mbps'].values;
df21AUp['Location']=p21A.index; df21AUp['2021']=p21A['Upload Speed Mbps'].values;
df18ALat['Location']=p18A.index; df18ALat['2018']=p18A['Latency'].values;
df19ALat['Location']=p19A.index; df19ALat['2019']=p19A['Latency'].values;
df20ALat['Location']=p20A.index; df20ALat['2020']=p20A['Latency'].values;
df21ALat['Location']=p21A.index; df21ALat['2021']=p21A['Latency'].values;
DepJoinAMovil4=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18A,df19A,df20A,df21A]).round(2).reset_index()
DepJoinAMovil4 = DepJoinAMovil4[DepJoinAMovil4.Location != 'Colombia']
DepJoinAMovil4 = DepJoinAMovil4.sort_values(by=['2021'],ascending=True)
DepJoinAMovil4Up=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18AUp,df19AUp,df20AUp,df21AUp]).round(2).reset_index()
DepJoinAMovil4Up = DepJoinAMovil4Up[DepJoinAMovil4Up.Location != 'Colombia']
DepJoinAMovil4Up = DepJoinAMovil4Up.sort_values(by=['2021'],ascending=True)
DepJoinAMovil4Lat=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18ALat,df19ALat,df20ALat,df21ALat]).round(2).reset_index()
DepJoinAMovil4Lat = DepJoinAMovil4Lat[DepJoinAMovil4Lat.Location != 'Colombia']
DepJoinAMovil4Lat = DepJoinAMovil4Lat.sort_values(by=['2021'],ascending=True)    

#### Sección 5 Móvil
@st.cache(allow_output_mutation=True)
def ColombiaMovil5():
    df1=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Colombia/IndDesempe%C3%B1oMov_3G4G_(2018mens).csv')
    df2=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Colombia/IndDesempe%C3%B1oMov_3G4G_(2019mens).csv')
    df3=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Colombia/IndDesempe%C3%B1oMov_3G4G_(2020mens).csv')
    df4=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Colombia/IndDesempe%C3%B1oMov_3G4G_(2021mens).csv')
    Operadores=pd.concat([df1,df2,df3,df4])
    FeAntig=Operadores['Aggregate Date'].unique() #Generar las fechas que tenían los datos
    FeCorre=pd.date_range('2018-01-01','2021-12-01', 
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
@st.cache(allow_output_mutation=True)
def ColombiaMovil7():
    Colombia7=pd.read_csv(pathMovil+'Cobertura/IndCoberturaMov_Colombia_(2018-2021).csv',delimiter=',')
    Colombia7['4G total'] = Colombia7[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Colombia7['Roaming total'] = Colombia7[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)   
    return Colombia7
Colombia7Movil=ColombiaMovil7()

####  Sección 8 Móvil
@st.cache(allow_output_mutation=True)
def DepJoinA8Movil():
    Ciudades8=pd.read_csv(pathMovil+'Cobertura/IndCoberturaMov_Ciud_(2018-2021).csv',delimiter=',')
    Ciudades8['Location']=Ciudades8['Location'].str.split(',',1,expand=True)[0]
    Ciudades8['4G total'] = Ciudades8[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Ciudades8['Roaming total'] = Ciudades8[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)
    p18A_8=(Ciudades8.loc[(Ciudades8['Aggregate Date']==2018),['Location','4G total']]).groupby(['Location'])['4G total'].mean()
    p19A_8=(Ciudades8.loc[(Ciudades8['Aggregate Date']==2019),['Location','4G total']]).groupby(['Location'])['4G total'].mean()
    p20A_8=(Ciudades8.loc[(Ciudades8['Aggregate Date']==2020),['Location','4G total']]).groupby(['Location'])['4G total'].mean()
    p21A_8=(Ciudades8.loc[(Ciudades8['Aggregate Date']==2021),['Location','4G total']]).groupby(['Location'])['4G total'].mean()
    df18A_8=pd.DataFrame();df19A_8=pd.DataFrame();df20A_8=pd.DataFrame();df21A_8=pd.DataFrame()
    df18A_8['Location']=p18A_8.index;df18A_8['2018']=p18A_8.values;
    df19A_8['Location']=p19A_8.index;df19A_8['2019']=p19A_8.values;
    df20A_8['Location']=p20A_8.index;df20A_8['2020']=p20A_8.values;
    df21A_8['Location']=p21A_8.index;df21A_8['2021']=p21A_8.values;
    DepJoinA_8=reduce(lambda x,y: pd.merge(x,y, on='Location', how='outer'), [df18A_8,df19A_8,df20A_8,df21A_8]).set_index('Location')
    DepJoinA_8=DepJoinA_8.round(2).reset_index()
    DepJoinA_8 = DepJoinA_8[DepJoinA_8.Location != 'Colombia']
    DepJoinA_8 = DepJoinA_8.sort_values(by=['2021'],ascending=False)    
    return DepJoinA_8
DepJoinAMovil8=DepJoinA8Movil()

####  Sección 9 Móvil
@st.cache(allow_output_mutation=True)
def OpJoinA9Movil():
    Operadores9=pd.read_csv('https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Bases_Movil/Cobertura/IndCoberturaMov_Gnral%20(2018-2021).csv',delimiter=',')
    Operadores9['4G total'] = Operadores9[['4G (%)', '4G Roaming (%)']].sum(axis=1)
    Operadores9['Roaming total'] = Operadores9[['4G Roaming (%)', '3G Roaming (%)', '2G Roaming (%)']].sum(axis=1)
    df18A_9=pd.DataFrame();df19A_9=pd.DataFrame();df20A_9=pd.DataFrame();df21A_9=pd.DataFrame()
    p18A_9=(Operadores9.loc[(Operadores9['Aggregate Date']==2018),['Provider','4G total']]).groupby(['Provider'])['4G total'].mean()
    p19A_9=(Operadores9.loc[(Operadores9['Aggregate Date']==2019),['Provider','4G total']]).groupby(['Provider'])['4G total'].mean()
    p20A_9=(Operadores9.loc[(Operadores9['Aggregate Date']==2020),['Provider','4G total']]).groupby(['Provider'])['4G total'].mean()
    p21A_9=(Operadores9.loc[(Operadores9['Aggregate Date']==2021),['Provider','4G total']]).groupby(['Provider'])['4G total'].mean()
    df18A_9['Provider']=p18A_9.index;df18A_9['2018']=p18A_9.values;
    df19A_9['Provider']=p19A_9.index;df19A_9['2019']=p19A_9.values;
    df20A_9['Provider']=p20A_9.index;df20A_9['2020']=p20A_9.values;
    df21A_9['Provider']=p21A_9.index;df21A_9['2021']=p21A_9.values;
    from functools import reduce
    OpJoinA_9=reduce(lambda x,y: pd.merge(x,y, on='Provider', how='outer'), [df18A_9,df19A_9,df20A_9,df21A_9]).set_index('Provider')
    OpJoinA_9=OpJoinA_9.round(2).reset_index()
    OpJoinA_9 = OpJoinA_9.sort_values(by=['2021'],ascending=False)
    return OpJoinA_9
OpJoinAMovil9=OpJoinA9Movil()

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
                marker_color='rgb(143,170,220)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.add_trace(go.Bar(
                x=DepJoinAMovilDown['year'],
                y=DepJoinAMovilDown['4g'],
                name='4G',
                marker_color='rgb(244,177,131)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.add_trace(go.Bar(
                x=DepJoinAMovilDown['year'],
                y=DepJoinAMovilDown['Total'],
                name='Total',
                marker_color='rgb(255,217,102)',width=[0.25,0.25,0.25,0.25]))
            fig1Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig1Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad descarga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig1Movil.update_traces(textfont_size=18)
            fig1Movil.update_layout(height=500,legend_title=None)
            fig1Movil.update_layout(legend=dict(orientation="h",y=1.05,x=0.4))
            fig1Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig1Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de descarga de internet móvil en <br>Colombia (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig1Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)    
            st.plotly_chart(fig1Movil, use_container_width=True)    

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil] 
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==2021)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Download Speed Mbps'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)
            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')                
            
            colombia_map1Movil = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
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
            
            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Velocidad promedio de descarga de Internet móvil en Colombia por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([2,4,1])
            with col2b:
                folium_static(colombia_map1Movil,width=480) 
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_descarga_Movil == 'Operadores':
            
            fig2Movil = go.Figure()
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig2Movil.add_trace(go.Bar(
                x=DepJoinAMovil3['Provider'],
                y=DepJoinAMovil3['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))
            fig2Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig2Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad descarga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig2Movil.update_traces(textfont_size=18)
            fig2Movil.update_layout(height=500,legend_title=None)
            fig2Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig2Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig2Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de descarga de internet móvil <br>Por operador (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig2Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig2Movil, use_container_width=True)                   

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil]  
                
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                pass
            else:    
                Proveedor1Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor1Movil['Download Speed Mbps'] =round(Proveedor1Movil['Download Speed Mbps'], 2)
                final_df1Movil=gdf2.merge(Proveedor1Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor2Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor2Movil['Download Speed Mbps'] =round(Proveedor2Movil['Download Speed Mbps'], 2)
                final_df2Movil=gdf2.merge(Proveedor2Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor3Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor3Movil['Download Speed Mbps'] =round(Proveedor3Movil['Download Speed Mbps'], 2)
                final_df3Movil=gdf2.merge(Proveedor3Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor4Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor4Movil['Download Speed Mbps'] =round(Proveedor4Movil['Download Speed Mbps'], 2)
                final_df4Movil=gdf2.merge(Proveedor4Movil, on='Location')   
            ##       
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor5Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor5Movil['Download Speed Mbps'] =round(Proveedor5Movil['Download Speed Mbps'], 2)
                final_df5Movil=gdf2.merge(Proveedor5Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].empty==True:
                final_df6Movil=gdf2
                final_df6Movil['Download Speed Mbps']=np.nan
            else:                
                Proveedor6Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Download Speed Mbps']].groupby(['Location'])[['Download Speed Mbps']].mean().reset_index()
                Proveedor6Movil['Download Speed Mbps'] =round(Proveedor6Movil['Download Speed Mbps'], 2)
                final_df6Movil=gdf2.merge(Proveedor6Movil, on='Location')              

            dualmap1_1Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df1Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m1)
            #######
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df2Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Download Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de descarga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m1)
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m2)
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
                data = final_df1Movil,
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
                data = final_df2Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Download Speed Mbps'],
                    aliases=['Departamento','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

            dualmap1_1Movil.m1.add_child(NIL1)
            dualmap1_1Movil.m1.keep_in_front(NIL1)
            dualmap1_1Movil.m2.add_child(NIL2)
            dualmap1_1Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/avantel.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_1Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_1Movil.m2)

            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df3Movil,
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
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df4Movil,
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df3Movil,
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
                data = final_df4Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Download Speed Mbps'],
                    aliases=['Departamento','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df5Movil,
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
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df6Movil,
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df5Movil,
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
                data = final_df6Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Download Speed Mbps'],
                    aliases=['Departamento','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
                st.markdown("<center><b> Velocidad de descarga promedio de internet móvil en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_1Movil,width=800) 
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_descarga_Movil == 'Ciudades':
            fig3Movil=go.Figure()
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig3Movil.add_trace(go.Bar(
                x=DepJoinAMovil4['Location'],
                y=DepJoinAMovil4['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))

            fig3Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig3Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Velocidad descarga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig3Movil.update_traces(textfont_size=18)
            fig3Movil.update_layout(height=500,legend_title=None)
            fig3Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig3Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig3Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de descarga de internet móvil <br>por ciudad (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig3Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.4)               
            st.plotly_chart(fig3Movil, use_container_width=True) 
            
    if select_indicador== 'Velocidad de carga':
        dimension_Vel_carga_Movil = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)            
        if dimension_Vel_carga_Movil == 'Histórico Colombia':    
            fig4Movil = go.Figure()
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'], 
                y=DepJoinAMovilUp['3g'],
                name='3G',
                marker_color='rgb(143,170,220)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'],
                y=DepJoinAMovilUp['4g'],
                name='4G',
                marker_color='rgb(244,177,131)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.add_trace(go.Bar(
                x=DepJoinAMovilUp['year'],
                y=DepJoinAMovilUp['Total'],
                name='Total',
                marker_color='rgb(255,217,102)',width=[0.25,0.25,0.25,0.25]))
            fig4Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig4Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad de carga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig4Movil.update_traces(textfont_size=18)
            fig4Movil.update_layout(height=500,legend_title=None)
            fig4Movil.update_layout(legend=dict(orientation="h",y=1.05,x=0.4))
            fig4Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig4Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de carga de internet móvil en <br>Colombia (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig4Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)  
                
            st.plotly_chart(fig4Movil, use_container_width=True)    

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil] 
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==2021)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Upload Speed Mbps'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)
            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')    
            
            colombia_map1Movi2 = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
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

            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Velocidad promedio de carga de internet móvil en Colombia por departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([2,4,1])
            with col2b:
                folium_static(colombia_map1Movi2,width=480) 
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
                
        if dimension_Vel_carga_Movil == 'Operadores':  
  
            fig6Movil = go.Figure()
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig6Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Up['Provider'],
                y=DepJoinAMovil3Up['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))
            fig6Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig6Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Velocidad de carga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig6Movil.update_traces(textfont_size=18)
            fig6Movil.update_layout(height=500,legend_title=None)
            fig6Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig6Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig6Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de carga de Internet móvil <br>Por operador (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig6Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig6Movil, use_container_width=True)                   

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil]                   

            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                pass
            else:    
                Proveedor1Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor1Movil['Upload Speed Mbps'] =round(Proveedor1Movil['Upload Speed Mbps'], 2)
                final_df1Movil=gdf2.merge(Proveedor1Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor2Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor2Movil['Upload Speed Mbps'] =round(Proveedor2Movil['Upload Speed Mbps'], 2)
                final_df2Movil=gdf2.merge(Proveedor2Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor3Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor3Movil['Upload Speed Mbps'] =round(Proveedor3Movil['Upload Speed Mbps'], 2)
                final_df3Movil=gdf2.merge(Proveedor3Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor4Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor4Movil['Upload Speed Mbps'] =round(Proveedor4Movil['Upload Speed Mbps'], 2)
                final_df4Movil=gdf2.merge(Proveedor4Movil, on='Location')   
            ##       
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                pass
            else:                
                Proveedor5Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor5Movil['Upload Speed Mbps'] =round(Proveedor5Movil['Upload Speed Mbps'], 2)
                final_df5Movil=gdf2.merge(Proveedor5Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].empty==True:
                final_df6Movil=gdf2
                final_df6Movil['Upload Speed Mbps']=np.nan
            else:                
                Proveedor6Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Upload Speed Mbps']].groupby(['Location'])[['Upload Speed Mbps']].mean().reset_index()
                Proveedor6Movil['Upload Speed Mbps'] =round(Proveedor6Movil['Upload Speed Mbps'], 2)
                final_df6Movil=gdf2.merge(Proveedor6Movil, on='Location')              

            dualmap1_1Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df1Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m1)
            #######
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df2Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m1)
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m2)
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
                data = final_df1Movil,
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
                data = final_df2Movil,
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

            dualmap1_1Movil.m1.add_child(NIL1)
            dualmap1_1Movil.m1.keep_in_front(NIL1)
            dualmap1_1Movil.m2.add_child(NIL2)
            dualmap1_1Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/avantel.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_1Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_1Movil.m2)

            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df3Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_2Movil.m1)
            #######
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df4Movil,
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df3Movil,
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
                data = final_df4Movil,
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

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df5Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m1)
            #######
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df6Movil,
                bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Upload Speed Mbps'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Velocidad de de carga (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_3Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df5Movil,
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
                data = final_df6Movil,
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
                st.markdown("<center><b> Velocidad de carga promedio de internet móvil en Colombia por operador y departamento (en Mbps)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_1Movil,width=800) 
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Movil == 'Ciudades':
            
            fig8Movil=go.Figure()
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig8Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Up['Location'],
                y=DepJoinAMovil4Up['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))

            fig8Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig8Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Velocidad de carga promedio (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig8Movil.update_traces(textfont_size=18)
            fig8Movil.update_layout(height=500,legend_title=None)
            fig8Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig8Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig8Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Velocidad promedio anual de carga de internet móvil <br>por ciudad (2018-2021) (en Mbps) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig8Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.4)             
            st.plotly_chart(fig8Movil, use_container_width=True) 

    if select_indicador== 'Latencia':
        dimension_Vel_carga_Movil = st.radio("Seleccione la dimensión del análisis",('Histórico Colombia','Ciudades','Operadores'),horizontal=True)            
        if dimension_Vel_carga_Movil == 'Histórico Colombia':    
            fig5Movil = make_subplots(rows=1,cols=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['Total'],line=dict(color='rgb(255,192,0)', width=1.5),marker=dict(
                        color='white',line=dict(color='rgb(255,192,0)',width=1),size=5),mode='lines+markers',name='Total'),row=1, col=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['3g'],
                                     line=dict(color='rgb(68,114,196)', width=1.5),marker=dict(
                        color='white',line=dict(color='rgb(68,114,196)',width=1),size=5),mode='lines+markers',name='3G'),row=1, col=1)
            fig5Movil.add_trace(go.Scatter(x=ColombiaMovil5['Date'], y=ColombiaMovil5['4g'],
                         line=dict(color='rgb(237,125,49)', width=1.5),marker=dict(
                         color='white',line=dict(color='rgb(237,125,49)',width=1),size=5),mode='lines+markers',name='4G'),row=1, col=1)
                         
            fig5Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=12),title_text=None,ticks="outside", tickformat="%m<br>20%y",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig5Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Latencia promedio<br>(ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig5Movil.update_traces(textfont_size=14)
            fig5Movil.update_layout(height=500,legend_title=None,font=dict(size=14))
            fig5Movil.update_layout(legend=dict(orientation="h",yanchor='top',xanchor='center',x=0.5,y=1.02),showlegend=True)
            fig5Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
            fig5Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=14,
            title={
            'text': "<b>Latencia promedio mensual de Internet móvil en<br> Colomia (2018-2021) (en ms)</b>",
            'y':0.85,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig5Movil.update_xaxes(tickvals=['2018-03-01','2018-06-01','2018-09-01','2018-12-01','2019-03-01','2019-06-01','2019-09-01','2019-12-01','2020-03-01','2020-06-01','2020-09-01','2020-12-01','2021-03-01','2021-06-01','2021-09-01','2021-12-01'])
            fig5Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.2) 
                
            st.plotly_chart(fig5Movil, use_container_width=True)    

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil]                     
            
            ColMovil1=Colombia2Movil[(Colombia2Movil['year']==2021)&(Colombia2Movil['month']==mes)].groupby(['Location'])['Latency'].mean().reset_index()
            ColMovil1=round(ColMovil1,2)
            ColMovil1['Location']=ColMovil1['Location'].replace({'CAQUETÃ¡':'CAQUETA','SAN ANDRÃ©S AND PROVIDENCIA':'SAN ANDRES Y PROVIDENCIA'})
            departamentos_dfMovil1=gdf2.merge(ColMovil1, on='Location')    
            
            colombia_map1Movi2 = folium.Map(location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
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
            
            col1, col2 ,col3= st.columns([1,4,1])
        
            col1, col2 ,col3= st.columns(3)
            with col2:
                st.markdown("<center><b> Latencia promedio de internet móvil en Colombia por departamento (en ms)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([2,4,1])
            with col2b:
                folium_static(colombia_map1Movi2,width=480) 
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

        if dimension_Vel_carga_Movil == 'Operadores':  
  
            fig7Movil = go.Figure()
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig7Movil.add_trace(go.Bar(
                x=DepJoinAMovil3Lat['Provider'],
                y=DepJoinAMovil3Lat['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))
            fig7Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=18),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig7Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=18),titlefont_size=18, title_text='Latencia promedio (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig7Movil.update_traces(textfont_size=18)
            fig7Movil.update_layout(height=500,legend_title=None)
            fig7Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig7Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig7Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Latencia promedio de Internet móvil <br>Por operador (2018-2021) (en ms) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})          
            fig7Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.2) 
            st.plotly_chart(fig7Movil, use_container_width=True)                   

            col1, col2,col3= st.columns(3)
            mes_opMovilNombre={'Junio':6,'Diciembre':12}
            with col2:
                mes_opMovil = st.selectbox('Escoja el mes de 2021',['Junio','Diciembre']) 
            mes=mes_opMovilNombre[mes_opMovil]                      

            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                pass
            else:    
                Proveedor1Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Avantel')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor1Movil['Latency'] =round(Proveedor1Movil['Latency'], 2)
                final_df1Movil=gdf2.merge(Proveedor1Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                pass
            else:                
                Proveedor2Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Claro')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor2Movil['Latency'] =round(Proveedor2Movil['Latency'], 2)
                final_df2Movil=gdf2.merge(Proveedor2Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                pass
            else:                
                Proveedor3Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='ETB')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor3Movil['Latency'] =round(Proveedor3Movil['Latency'], 2)
                final_df3Movil=gdf2.merge(Proveedor3Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                pass
            else:                
                Proveedor4Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Movistar')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor4Movil['Latency'] =round(Proveedor4Movil['Latency'], 2)
                final_df4Movil=gdf2.merge(Proveedor4Movil, on='Location')   
            ##       
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                pass
            else:                
                Proveedor5Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='Tigo')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor5Movil['Latency'] =round(Proveedor5Movil['Latency'], 2)
                final_df5Movil=gdf2.merge(Proveedor5Movil, on='Location')  
            ##
            if OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].empty==True:
                final_df6Movil=gdf2
                final_df6Movil['Latency']=np.nan
            else:                
                Proveedor6Movil=OpCiudMovil1.loc[(OpCiudMovil1['Provider']=='WOM')&(OpCiudMovil1['year']==2021)&(OpCiudMovil1['month']==mes),['Location','Latency']].groupby(['Location'])[['Latency']].mean().reset_index()
                Proveedor6Movil['Latency'] =round(Proveedor6Movil['Latency'], 2)
                final_df6Movil=gdf2.merge(Proveedor6Movil, on='Location')              

            dualmap1_1Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df1Movil,
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m1)
            #######
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df2Movil,
                #bins=[0,5,10,15,20,40,60],
                columns=['Location', 'Latency'],
                key_on='feature.properties.NOMBRE_DPT',
                fill_color='YlGnBu', 
                fill_opacity=0.9, 
                line_opacity=0.9,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(dualmap1_1Movil.m2)
            #######
            # Adicionar nombres del departamento
            style_function = "font-size: 15px; font-weight: bold"
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m1)
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_1Movil.m2)
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
                data = final_df1Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            NIL2 = folium.features.GeoJson(
                data = final_df2Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

            dualmap1_1Movil.m1.add_child(NIL1)
            dualmap1_1Movil.m1.keep_in_front(NIL1)
            dualmap1_1Movil.m2.add_child(NIL2)
            dualmap1_1Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/avantel.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/claro.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_1Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_1Movil.m2)

            dualmap1_2Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df3Movil,
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
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df4Movil,
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_2Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df3Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            NIL2 = folium.features.GeoJson(
                data = final_df4Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

            dualmap1_2Movil.m1.add_child(NIL1)
            dualmap1_2Movil.m1.keep_in_front(NIL1)
            dualmap1_2Movil.m2.add_child(NIL2)
            dualmap1_2Movil.m2.keep_in_front(NIL2)

            url1 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/etb.png")
            url2 = ("https://www.postdata.gov.co/sites/default/files/dataflash/2021-027/movistar.png")

            FloatImage(url1, bottom=5, left=1).add_to(dualmap1_2Movil.m1)
            FloatImage(url2, bottom=5, left=53).add_to(dualmap1_2Movil.m2)
            
            dualmap1_3Movil=folium.plugins.DualMap(heigth=1000,location=[4.570868, -74.297333], zoom_start=5,tiles='cartodbpositron',zoom_control=False,
               scrollWheelZoom=False,
               dragging=False)
            ########
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df5Movil,
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
            choropleth=folium.Choropleth(
                geo_data=Colombian_DPTO2,
                data=final_df6Movil,
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
            choropleth.geojson.add_child(
                folium.features.GeoJsonTooltip(['DPTO'], style=style_function, labels=False))
            folium.LayerControl().add_to(dualmap1_3Movil.m1)
            choropleth.geojson.add_child(
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
                data = final_df5Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            NIL2 = folium.features.GeoJson(
                data = final_df6Movil,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['Location','Latency'],
                    aliases=['Departamento','Latencia (ms)'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            for key in choropleth._children:
                if key.startswith('color_map'):
                    del(choropleth._children[key])

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
                st.markdown("<center><b> Latencia promedio de internet móvil en Colombia por operador y departamento (en ms)</b></center>",unsafe_allow_html=True)                        
            col1b, col2b ,col3b= st.columns([1,4,1])
            with col2b:
                folium_static(dualmap1_1Movil,width=800) 
                folium_static(dualmap1_2Movil,width=800)
                folium_static(dualmap1_3Movil,width=800)    
                st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
  

        if dimension_Vel_carga_Movil == 'Ciudades':         

            fig9Movil=go.Figure()
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig9Movil.add_trace(go.Bar(
                x=DepJoinAMovil4Lat['Location'],
                y=DepJoinAMovil4Lat['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))

            fig9Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig9Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Latencia promedio (ms)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig9Movil.update_traces(textfont_size=18)
            fig9Movil.update_layout(height=500,legend_title=None)
            fig9Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig9Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig9Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Latencia promedio de Internet móvil <br>por ciudad (2018-2021) (en ms) </b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})  
            fig9Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2018 - 2021. Las marcas registradas de Ookla se usan bajo licencia y se reimprimen con permiso.',
            font=dict(size=10), xref='x domain',x=0.2,yref='y domain',y=-0.4)             
            st.plotly_chart(fig9Movil, use_container_width=True) 
        
    
    if select_indicador== 'Registro en red':
        st.markdown("### Registro en Red", unsafe_allow_html=True)
        
        fig10Movil = go.Figure()
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021'],
            y=Colombia7Movil['2G (%)'],
            name='2G (%)',
            marker_color='rgb(17,200,164)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021'],
            y=Colombia7Movil['3G (%)'],
            name='3G (%)',
            marker_color='rgb(55,70,73)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021'],
            y=Colombia7Movil['4G (%)'],
            name='4G (%)',
            marker_color='rgb(72,68,242)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021'],
            y=Colombia7Movil['Roaming total'],
            name='Roaming total (%)',
            marker_color='rgb(253,98,94)',
            width=0.7))
        fig10Movil.add_trace(go.Bar(
            x=['2018','2019','2020','2021'],
            y=Colombia7Movil['No Coverage (%)'],
            name='No Cobertura (%)',
            marker_color='rgb(254,184,52)',
            width=0.7))
        fig10Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
        fig10Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
        fig10Movil.update_layout(height=500,legend_title=None)
        fig10Movil.update_layout(font_color="Black",title_font_family="Arial",title_font_color="Black",titlefont_size=16)
        fig10Movil.update_layout(height=600,   
            title="<b>Promedio anual del porcentaje de registro en red en Colombia<br>(2018-2021)</b>",
            title_x=0.5)
        fig10Movil.update_layout(uniformtext_minsize=12, barmode='stack', showlegend=True,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
           orientation="v",
            y=1.05,
            x=1,
            font_size=12))
        fig10Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)     
        st.plotly_chart(fig10Movil, use_container_width=True) 
        
        st.markdown("### Registro en Red 4G", unsafe_allow_html=True)
        dimension_Cober4G_Movil = st.radio("Seleccione la dimensión del análisis",('Colombia','Ciudades','Operadores'),horizontal=True)
        if dimension_Cober4G_Movil=='Colombia':
            fig11Movil = go.Figure()
            fig11Movil.add_trace(go.Bar(
                x=['2018','2019','2020','2021'],
                y=Colombia7Movil['4G total'].round(1),
                name='4G (%)',
                marker_color='rgb(72,68,242)', 
                width=0.7))

            fig11Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig11Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig11Movil.update_traces(textfont_size=14)
            fig11Movil.update_layout(height=500,legend_title=None)
            fig11Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig11Movil.update_layout(font_color="Black",title_font_family="Arial",title_font_color="Black",titlefont_size=16)
            fig11Movil.update_layout(height=600,   
                title="<b>Promedio anual del porcentaje de registro en red 4G en Colombia<br>(2018-2021)</b>",
                title_x=0.5)
            fig11Movil.update_traces()
            fig11Movil.update_layout(uniformtext_minsize=12, barmode='stack', uniformtext_mode='hide')
            fig11Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            fig11Movil.update_layout(plot_bgcolor='rgba(0,0,0,0)')
            fig11Movil.update_layout(legend=dict(
               orientation="h",
                y=1.05,
                xanchor='center',
                x=0.5,
                font_size=12))
            fig11Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)     
            st.plotly_chart(fig11Movil,use_container_width=True)   
            
        if dimension_Cober4G_Movil=='Ciudades':
            fig12Movil = go.Figure()
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig12Movil.add_trace(go.Bar(
                x=DepJoinAMovil8['Location'],
                y=DepJoinAMovil8['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))

            fig12Movil.update_xaxes(tickangle=-90, tickfont=dict(family='Arial', color='black', size=14),title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig12Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=14),titlefont_size=14, title_text='Registro en red 4G (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig12Movil.update_traces(textfont_size=18)
            fig12Movil.update_layout(height=500,legend_title=None)
            fig12Movil.update_layout(legend=dict(orientation="h",y=1.05,xanchor='center',x=0.5))
            fig12Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig12Movil.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16,
            title={
            'text': "<b>Promedio anual registro en red móvil por ciudad <br>(2018-2021)</b>",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'}) 
            fig12Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.4)             
            st.plotly_chart(fig12Movil,use_container_width=True)

        if dimension_Cober4G_Movil=='Operadores':
            fig13Movil = go.Figure()
            fig13Movil.add_trace(go.Bar(
                x=OpJoinAMovil9['Provider'],
                y=OpJoinAMovil9['2018'],
                name='2018',
                marker_color='rgb(213,3,85)'))
            fig13Movil.add_trace(go.Bar(
                x=OpJoinAMovil9['Provider'],
                y=OpJoinAMovil9['2019'],
                name='2019',
                marker_color='rgb(255,152,0)'))
            fig13Movil.add_trace(go.Bar(
                x=OpJoinAMovil9['Provider'],
                y=OpJoinAMovil9['2020'],
                name='2020',
                marker_color='rgb(44,198,190)'))
            fig13Movil.add_trace(go.Bar(
                x=OpJoinAMovil9['Provider'],
                y=OpJoinAMovil9['2021'],
                name='2021',
                marker_color='rgb(72,68,242)'))

            fig13Movil.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18,title_text=None,ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
            fig13Movil.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18, title_text='Registro en red (%)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
            zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
            fig13Movil.update_traces(textfont_size=14)
            fig13Movil.update_layout(height=500,legend_title=None)
            fig13Movil.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
            fig13Movil.update_layout(font_color="Black",title_font_family="Arial",title_font_color="Black",titlefont_size=16)
            fig13Movil.update_layout(height=600,   
                title="<b>Promedio anual del porcentaje de registro en red 4G por operador<br>(2018-2021)</b>",
                title_x=0.5)
            fig13Movil.update_layout(barmode='group', uniformtext_mode='hide',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
               orientation="h",
                y=1.05,
                xanchor='center',
                x=0.5,
                font_size=15))
            fig13Movil.add_annotation(
            showarrow=False,
            text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
            font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.15)                 
            st.plotly_chart(fig13Movil,use_container_width=True)    

######################################################### Comparación Internacional #######################################        
fijo_Intdict = {'Suriname': [16.48, 8.8, 26],
        'Uruguay': [176.74, 35.42, 13],
        'Brazil': [128.31, 73.26, 12],
        'Argentina': [62.58, 25.75, 25],
        'Ecuador': [41.2, 35.81, 14],
        'Peru': [63.75, 36.47, 20],
        'Bolivia': [30.54, 14.06, 19],
        'Chile': [253.61, 192.85, 13],
        'Paraguay': [75.09,23.78, 15],
        'Colombia': [84.82, 46.58, 22],
        'Venezuela': [28.21, 22.75, 51],
        'Guyana':[68.25,28.44,19]}
Fijo_Int=pd.DataFrame.from_dict(fijo_Intdict,orient='index').reset_index()
Fijo_Int=Fijo_Int.rename(columns={'index':'País',0:'Download',1:'Upload',2:'Latency'})
@st.cache()
def gdf_Suramerica(allow_output_mutation=True):
    gdf_Int = gpd.read_file("https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Suramerica.geo.json")
    gdf_Int=gdf_Int.rename(columns=({'admin':'País'}))
    return gdf_Int
gdf_Int=gdf_Suramerica()
@st.cache(allow_output_mutation=True)
def data_Suramerica():    
    with urllib.request.urlopen("https://raw.githubusercontent.com/postdatacrc/Mediciones_QoE/main/Suramerica.geo.json") as url:
        SURAMERICA = json.loads(url.read().decode())
    return SURAMERICA
SURAMERICA=data_Suramerica()    
Fijo_df=gdf_Int.merge(Fijo_Int, on='País')

movil_Intdict = {'Suriname': [42.66, 18.38, 25],
        'Uruguay': [51.33, 15.05, 32],
        'Brazil': [36.56, 11.24, 38],
        'Argentina': [30.73, 9.71, 38],
        'Ecuador': [24.76, 10.93, 35],
        'Peru': [27.52, 13.46, 36],
        'Bolivia': [22.65, 12.54, 31],
        'Chile': [31.32, 13.06, 33],
        'Paraguay': [21.46,10.34, 41],
        'Colombia': [20.01, 11.03, 47],
        'Venezuela': [9.18, 5.33, 48]}
Movil__Int=pd.DataFrame.from_dict(movil_Intdict,orient='index').reset_index()
Movil__Int=Movil__Int.rename(columns={'index':'País',0:'Download',1:'Upload',2:'Latency'})
Movil_df=gdf_Int.merge(Movil__Int, on='País')

dict_coloresPais={'Suriname':'rgb(51,0,25)','Uruguay':'rgb(255,0,0)','Colombia':'rgb(255,255,0)',
                 'Venezuela':'rgba(128,255,0,0.3)','Ecuador':'rgb(255,0,255)','Peru':'rgb(0,255,128)',
                 'Bolivia':'rgb(255,102,102)','Paraguay':'rgb(0,128,255)','Brazil':'rgb(0,51,51)',
                 'Chile':'rgb(0,0,255)','Argentina':'rgb(127,0,255)','Guyana':'rgb(255,128,0)'}

if select_servicio == 'Comparación internacional':
    select_servicio=st.selectbox('Indicador de desempeño',['Velocidad de descarga','Velocidad de carga','Latencia','Resumen'])
    if select_servicio=='Velocidad de descarga':
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Internet fijo",unsafe_allow_html=True)
            st.markdown("")
            suramerica_map4 = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Fijo_df,
                columns=['País', 'Download'],
                key_on='feature.properties.name',
                fill_color='Greens', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Velocidad de descarga fijo (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map4)

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
                data = Fijo_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Download'],
                    aliases=['País','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map4.add_child(NIL)
            suramerica_map4.keep_in_front(NIL)
            st.markdown("<b> Velocidad promedio de descarga de <br> Internet fijo en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map4,width=400,height=550)      
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)
    
            
        with col2:
            st.markdown("### Internet móvil",unsafe_allow_html=True)        
            st.markdown("")
            suramerica_map5 = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Movil_df,
                columns=['País', 'Download'],
                key_on='feature.properties.name',
                fill_color='Greens', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Velocidad de descarga fijo (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map5)

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
                data = Movil_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Download'],
                    aliases=['País','Velocidad descarga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map5.add_child(NIL)
            suramerica_map5.keep_in_front(NIL)
            st.markdown("<b> Velocidad promedio de descarga de <br> Internet móvil en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map5,width=400,height=550)      
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)


    if select_servicio=='Velocidad de carga':
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Internet fijo",unsafe_allow_html=True)
            st.markdown("")
            suramerica_map4_b = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Fijo_df,
                columns=['País', 'Upload'],
                key_on='feature.properties.name',
                fill_color='Greens', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Velocidad de carga fijo (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map4_b)

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
                data = Fijo_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Upload'],
                    aliases=['País','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map4_b.add_child(NIL)
            suramerica_map4_b.keep_in_front(NIL)
            st.markdown("<b> Velocidad promedio de carga de <br> Internet fijo en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map4_b,width=400,height=550)      
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

            
        with col2:
            st.markdown("### Internet móvil",unsafe_allow_html=True)        
            st.markdown("")
            suramerica_map5_b = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Movil_df,
                columns=['País', 'Upload'],
                key_on='feature.properties.name',
                fill_color='Greens', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Velocidad de carga fijo (Mbps)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map5_b)

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
                data = Movil_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Upload'],
                    aliases=['País','Velocidad de carga'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map5_b.add_child(NIL)
            suramerica_map5_b.keep_in_front(NIL)
            st.markdown("<b> Velocidad promedio de carga de <br> Internet móvil en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map5_b,width=400,height=550)    
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)


    if select_servicio=='Latencia':
    
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Internet fijo",unsafe_allow_html=True)
            st.markdown("")
            suramerica_map4_c = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Fijo_df,
                columns=['País', 'Latency'],
                key_on='feature.properties.name',
                fill_color='Reds', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map4_c)

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
                data = Fijo_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Latency'],
                    aliases=['País','Latencia'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map4_c.add_child(NIL)
            suramerica_map4_c.keep_in_front(NIL)
            st.markdown("<b> Latencia promedio de <br> Internet fijo en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map4_c,width=400,height=550)      
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

            
        with col2:
            st.markdown("### Internet móvil",unsafe_allow_html=True)        
            st.markdown("")
            suramerica_map5_c = folium.Map(location=[-24, -60], zoom_start=3,tiles='cartodbpositron')
            choropleth=folium.Choropleth(
                geo_data=SURAMERICA,
                data=Movil_df,
                columns=['País', 'Latency'],
                key_on='feature.properties.name',
                fill_color='Reds', 
                fill_opacity=1, 
                line_opacity=0.9,
                reversescale=True,
                legend_name='Latencia (ms)',
                nan_fill_color = "black",
                smooth_factor=0).add_to(suramerica_map5_c)

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
                data = Movil_df,
                style_function=style_function, 
                control=False,
                highlight_function=highlight_function, 
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['País','Latency'],
                    aliases=['País','Latencia'],
                    style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                )
            )
            suramerica_map5_c.add_child(NIL)
            suramerica_map5_c.keep_in_front(NIL)
            st.markdown("<b> Latencia promedio de <br> Internet móvil en Suramerica (Mbps)</b>",
            unsafe_allow_html=True)
            folium_static(suramerica_map5_c,width=400,height=550)      
            st.markdown(r"""<p style=font-size:10px><i>Fuente: Basado en el análisis realizado por CRC de los datos de Speedtest Intelligence® para 2021</i></p> """,unsafe_allow_html=True)

    if select_servicio=='Resumen':
        st.markdown("### Resumen Internet fijo", unsafe_allow_html=True)
        fig1Int=make_subplots(rows=1,cols=1)
        for pais in Fijo_Int['País'].unique().tolist():
            fig1Int.add_trace(go.Scatter(
            x=Fijo_Int[Fijo_Int['País']== pais]['Download'].values, y=Fijo_Int[Fijo_Int['País']== pais]['Upload'].values, name=pais,
            mode='markers',
            text=Fijo_Int[Fijo_Int['País']== pais]['Latency'],
            marker=dict(
                color=dict_coloresPais[pais],
                opacity=1,
                size=Fijo_Int[Fijo_Int['País']== pais]['Latency']),hovertemplate='<b>País:</b>'+pais+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
        fig1Int.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18,title_text='Velocidad de descarga (Mbps)',ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
        fig1Int.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
        fig1Int.update_traces(textfont_size=14)
        fig1Int.update_layout(height=500,legend_title=None)
        fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
        fig1Int.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16)

        fig1Int.update_layout(height=600,   
            title="<b>Diagrama de burbujas con la distribución de velocidades y latencia<br>de Suramérica por país para Internet fijo - Diciembre 2021</b>",
            title_x=0.5,
            titlefont_size=15,
            font=dict(
                family="Arial",
                color=" black",size=16))
        fig1Int.update_layout(legend=dict(y=1.02,x=0.01))
        fig1Int.add_shape(type="line",
            x0=0, y0=0, x1=250, y1=250,
            line=dict(
                color="indianred",
                width=4,
                dash="dot",
            ),row=1,col=1)
        fig1Int.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        fig1Int.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        fig1Int.add_annotation(
        showarrow=False,
        text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
        font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.2)             
        st.plotly_chart(fig1Int, use_container_width=True)    
        
        ##
        
        st.markdown("### Resumen Internet móvil", unsafe_allow_html=True)
        fig2Int=make_subplots(rows=1,cols=1)
        for pais in Movil__Int['País'].unique().tolist():
            fig2Int.add_trace(go.Scatter(
            x=Movil__Int[Movil__Int['País']== pais]['Download'].values, y=Movil__Int[Movil__Int['País']== pais]['Upload'].values, name=pais,
            mode='markers',
            text=Movil__Int[Movil__Int['País']== pais]['Latency'],
            marker=dict(
                color=dict_coloresPais[pais],
                opacity=1,
                size=Movil__Int[Movil__Int['País']== pais]['Latency']),hovertemplate='<b>País:</b>'+pais+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps<extra></extra>'+'<br>'+'<b>Velocidad descarga:</b>%{x:.2f} Mbps'+'<br>'+'<b>Latencia:</b>%{text} ms'),row=1, col=1)
        fig2Int.update_xaxes(tickangle=0, tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18,title_text='Velocidad de descarga (Mbps)',ticks="outside",tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True)
        fig2Int.update_yaxes(tickfont=dict(family='Arial', color='black', size=16),titlefont_size=18, title_text='Velocidad de carga (Mbps)',ticks="outside", tickwidth=1, tickcolor='black', ticklen=5,
        zeroline=True,linecolor = "#000000",zerolinewidth=2,showticklabels=True) 
        fig2Int.update_traces(textfont_size=14)
        fig2Int.update_layout(height=500,legend_title=None)
        fig2Int.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
        fig2Int.update_layout(font_color="Black",title_font_family="NexaBlack",title_font_color="Black",titlefont_size=16)

        fig2Int.update_layout(height=600,   
            title="<b>Diagrama de burbujas con la distribución de velocidades y latencia<br>de Suramérica por país para Internet móvil - Diciembre 2021</b>",
            title_x=0.5,
            titlefont_size=15,
            font=dict(
                family="Arial",
                color=" black",size=16))
        fig2Int.update_layout(legend=dict(y=1.02,x=0.01))
        fig2Int.add_shape(type="line",
            x0=0, y0=0, x1=60, y1=60,
            line=dict(
                color="indianred",
                width=4,
                dash="dot",
            ),row=1,col=1)
        fig2Int.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        fig2Int.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        fig2Int.add_annotation(
        showarrow=False,
        text='Fuente: Basado en los datos de Ookla® Speedtest Intelligence® para 2018 - 2021.',
        font=dict(size=10), xref='x domain',x=0.5,yref='y domain',y=-0.2) 
        st.plotly_chart(fig2Int, use_container_width=True)            