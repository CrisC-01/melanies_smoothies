# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:",name_on_order)

cnx = st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

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

import requests
import streamlit as st
import pandas as pd

# Correct: just the plain URL string
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

if smoothiefroot_response.status_code == 200:
    data = smoothiefroot_response.json()
    
    # Convert JSON into a DataFrame
    df = pd.DataFrame([data])  # wrap in list if it's a single dict
    
    # Display the DataFrame in Streamlit
    st.dataframe(df)
else:
    st.error(f"Request failed with status code {smoothiefroot_response.status_code}")


