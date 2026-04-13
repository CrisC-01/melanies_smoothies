import requests
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    # --- NEW: Fetch nutrition data for chosen fruits ---
    nutrition_data = []
    for fruit_chosen in ingredients_list:
        url = f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            nutrition_data.append(data)
        else:
            st.error(f"Failed to fetch data for {fruit_chosen}")

    if nutrition_data:
        df = pd.DataFrame(nutrition_data)
        st.subheader("Nutrition Data for Your Fruits")
        st.dataframe(df, use_container_width=True)

