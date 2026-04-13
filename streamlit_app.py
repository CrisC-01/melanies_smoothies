# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import streamlit as st
import pandas as pd


st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)

cnx = st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')),select(col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:"
    , my_dataframe
    ,max_selections=5
)

if ingredients_list:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen+' '
        #st.write(ingredients_string)

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

        #st.write(my_insert_stmt)
        #st.stop()
        time_ton_insert = st.button('Submit Order')
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")



smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
if smoothiefroot_response.status_code == 200:
    data = smoothiefroot_response.json()
    df = pd.DataFrame([data]) 
    st.dataframe(df)
else:
    st.error(f"Request failed with status code {smoothiefroot_response.status_code}")
