from importlib_metadata import metadata
from pyrsistent import v
import qrcode
from faker import Faker
from faker_vehicle import VehicleProvider
import pandas as pd
from faker.providers import automotive
import random
import streamlit as st
import web3 as Web3
import pandas as pd
import path as Path
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table
import Texas_Database as td 
import time
from tqdm import tqdm

st.title( 'Temporary License Plate Verification' )
st.caption('Team Paper Plates -- Azzaldin Assi, Eli Santibanez,  Quentin Reynolds')

# shows progress bar

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'scanning ' )
    bar.progress(i+1)
    time.sleep(0.1)
'100%'

engine = create_engine('sqlite:///database_file.db')
connection = engine.connect()

df = pd.read_sql_table('Texas License Plates', con=engine)

st.dataframe(df['VIN Number'])
# print(engine.table_names)

# sidebar 
st.sidebar.title('Vehicle Information')
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar
# st.sidebar



