    # Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your Smoothiees")
st.write("Choose the fruit you want in your custom smoothie!")

cnx = st.connection("snowflake")
#my_dataframe = cnx.query("select FRUIT_NAME, SEARCH_ON from smoothies.public.fruit_options")
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
st.stop()
ingridents_lists = st.multiselect('choose up to 5 ingrident', my_dataframe, max_selections =6)
ingredients_string = ''
NAME_ON_ORDER = st.text_input("add order name");
my_insert_stmt = ''


if ingridents_lists:
    for fruit_chosen in ingridents_lists:
        ingredients_string += fruit_chosen + ' '
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """', '""" + NAME_ON_ORDER + """')"""
    
    time_to_insert = st.button('submit_order')
    if ingredients_string and time_to_insert:
        cnx.cursor().execute(my_insert_stmt)
        #session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,' + NAME_ON_ORDER + '!', icon="✅")
        st.write(my_insert_stmt)      
            
