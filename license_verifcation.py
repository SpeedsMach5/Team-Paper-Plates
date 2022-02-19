from importlib_metadata import metadata
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

# st.text( 'Paper License Plate Verification' )

engine = create_engine('sqlite:///database_file.db')
connection = engine.connect()

df = pd.read_sql_table('Texas License Plates', con=engine)

print(df['VIN Number'])
# print(engine.table_names)