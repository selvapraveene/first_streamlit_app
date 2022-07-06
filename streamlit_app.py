import streamlit
import pandas
import snowflake
from snowflake import connector
import requests

#import snowflake.connector

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Favorites')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale ,Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('Build your own Fruit Smoothie')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)


streamlit.header("Fruityvice Fruit Advice!")


fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json()) # writes data to the screen


fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# draws a table for the results
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
#streamlit.text("The Fruit Load List Contains:")
streamlit.header("Fruityvice Fruit Advice!")
streamlit.dataframe(my_data_rows)

add_fruit = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('The user entered ', add_fruit)


add_fruit_response = requests.get("https://fruityvice.com/api/fruit/"+add_fruit)
#streamlit.text(add_fruit_response.json()) # writes data to the screen
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" +add_fruit + "')")

fruit_normalized = pandas.json_normalize(add_fruit_response.json())
# draws a table for the results
streamlit.dataframe(fruit_normalized)

