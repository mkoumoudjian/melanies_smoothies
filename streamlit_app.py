# Import python packages
import streamlit as st
#from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your Smoothiees")
st.write("Choose the fruit you want in your custom smoothie!")

cnx = st.connection("snowflake")
my_dataframe = cnx.query("select FRUIT_NAME from smoothies.public.fruit_options")
ingridents_lists = st.multiselect('choose up to 5 ingrident', my_dataframe, max_selections =6)
ingredients_string = ''
NAME_ON_ORDER = st.text_input("add order name");
my_insert_stmt = ''

if ingridents_lists:
    for fruit_chosen in ingridents_lists:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + NAME_ON_ORDER + """')"""
    
    time_to_insert = st.button('submit_order')
    if ingredients_string and time_to_insert:
        cnx.cursor().execute(my_insert_stmt)
        #session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + NAME_ON_ORDER + '!', icon="✅")
        st.write(my_insert_stmt)
#new for api
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
