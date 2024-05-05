# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import requests

connection_parameters = st.secrets["connections.snowflake"]
session = Session.builder.configs(connection_parameters).create()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Query Snowflake for fruit options
fruit_options_df = session.table("fruit_options").select(col('fruit_name')).to_pandas()

# Allow user to select ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# Construct the order confirmation string
if ingredients_list:
    ingredients_string = ", ".join(ingredients_list)
    st.write(f"Selected ingredients: {ingredients_string}")

    # Dummy API call (Example)
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    if fruityvice_response.ok:
        fv_df = fruityvice_response.json()
        st.dataframe(fv_df, use_container_width=True)

# Insert order into Snowflake
my_insert_stmt = f"""
    INSERT INTO orders(ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
"""
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
