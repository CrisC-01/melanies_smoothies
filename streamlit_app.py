# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON')
)

# Convert Snowpark DataFrame to Pandas
pd_df = my_dataframe.to_pandas()

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Show nutrition info if ingredients selected
ingredients_string = ''
if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        #search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write(f'The search value for {fruit_chosen} is {search_on}.')

        #st.subheader(f'{fruit_chosen} Nutrition Information')
        #fruityvice_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        #st.dataframe(data=fruityvice_response.json(), use_container_width=True)

# Submit button only enabled if name and ingredients are provided
if st.button('Submit Order'):
    if name_on_order and ingredients_list:
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string.strip()}', '{name_on_order}')
        """
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    else:
        st.warning("Please enter your name and select at least one ingredient before submitting.")

