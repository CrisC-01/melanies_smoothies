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

# Correct: just the plain URL string
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# If you want to display the raw response object
st.text(smoothiefroot_response)

# If you want to display the actual JSON data returned by the API
if smoothiefroot_response.status_code == 200:
    data = smoothiefroot_response.json()
    st.json(data)  # nicely formatted JSON in Streamlit
else:
    st.error(f"Request failed with status code {smoothiefroot_response.status_code}")

