#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from connection import OpenWeatherMapConnection
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd


# In[ ]:


def ChangeButtonColour(widget_label, background_color='transparent', font_color = 'white'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)


# In[ ]:


hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
th_props = [
  ('font-weight', 'bold')
  ]
styles = [
  dict(selector="th", props=th_props)]


# In[ ]:


st.set_page_config(layout='wide')
st.subheader('Weather 🌦️ details Extraction using [:blue[OpenWeatherMap]](https://openweathermap.org/)')
st.caption("OpenWeatherMap API key can be obtained from [here](https://openweathermap.org/api)")


# In[ ]:


with st.form("form1"):
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("Enter the City name")
    with col2:
        inp_api_key = st.text_input("Enter your OpenWeatherMap API Key (Optional)")
    submitted = st.form_submit_button("Fetch")
    ChangeButtonColour('Fetch', background_color = '#0ACC0A')
    if submitted:
        # Estabilising Connection to OpenWeatherMap
        conn = st.experimental_connection("open_weather_map", type=OpenWeatherMapConnection, api_key = inp_api_key) 
        # Fetching Weather details
        weather_df = conn.fetch(city)
        st.write(f":blue[**{city}**] Weather details")
        st.write(weather_df.style.hide_index().format().to_html(), unsafe_allow_html=True)

