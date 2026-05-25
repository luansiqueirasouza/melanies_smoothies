# Import python packages.
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose The Fruits You Want In Your Custom Smoothie!
  """
)
cnx = st.connection("snowflake")
session = cnx.session()
#option = st.selectbox(
#    'What Is Your Favorite Fruit?',
#    ('Banana','Strawberrie', 'Peach')
#)
#st.write('Your Favorite Fruit Is:', option)

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

customer_name = st.text_input('Name on Smoothie:')

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + customer_name + """')"""
    #st.write(customer_name)
    #st.stop()
    #st.write(my_insert_stmt)
  
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {customer_name}!', icon="✅")

smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
st.text(smoothiefroot_response)
