from web3 import Web3
import streamlit as st
import json
from dotenv import load_dotenv
import os
from Data.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
from Data.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json, get_CID
import qrcode
import sqlalchemy as sql
import pandas as pd
import io
from pyzbar.pyzbar import decode
import numpy as np
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

from PIL import Image




################################################################################
# Contract Helper function:
################################################################################
# @st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open('abi.json') as f:
        artwork_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )
    return contract

contract = load_contract()


def register_car(address, name, vin, status, artwork_uri):
    return contract.functions.registerCar(
        address,
        name,
        vin,
        status,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)
    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)
    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)
    return json_ipfs_hash

def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash

def make_qr_quote(name, vin, status, make, model, year):
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4)
    qr.add_data(
        {"name":f"{name}", 
        "vin":f"{vin}",
        "status":f"{status}",
        "make":f"{make}",
        "model":f"{model}",
        "year":f"{year}"})
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"./temp/{name}.jpg")
    # return img.get_image()

def get_image_from_database(name):
        with open(f"./temp/{name}.jpg", "rb") as image:
                f = image.read()
                b = bytearray(f)
                return b

def total_token_supply():
    return contract.functions.totalSupply().call()


def vin_verification(number_of_tokens, vin_to_verify):
    for number in range(0,number_of_tokens):
        if contract.functions.vehicleCollection(number).call()[1] == vin_to_verify:
            return "IN SYSTEM"
        else:
            continue 
    return "not in system"

# def qr_decoder(file):    

#     file_bytes = file.getvalue()

#     img_arr = np.frombuffer(file_bytes,np.uint8)
   
#     img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
   
#     data = decode(img)[0].data

#     decode_data = data.decode("utf-8")

#     replace_string = decode_data.replace("'",'"')
    
#     json_format_data = json.loads(replace_string)

#     return json_format_data

def connect_to_db():
    connection_string = "sqlite:///database_file.db"
    engine = sql.create_engine(connection_string)
    df = pd.read_sql("Texas License Plates",con=engine)
    return df


def get_qr_info(file):
    name = file["name"]
    vin = file["vin"]
    status = file["status"]
    make = file["make"]
    model = file["model"] 
    year = file["year"]
    results = f"* Name: {name} \n * Vin: {vin} \n * Status: {status} \n * Make: {make} \n * Model: {model} \n * Year: {year}"

    
    



def qr_decoder(file):    

    file_bytes = file.getvalue()
    
    image = Image.open(io.BytesIO(file_bytes))

    
    data = decode(image)[0].data

    decode_data = data.decode("utf-8")

    replace_string = decode_data.replace("'",'"')
    
    json_format_data = json.loads(replace_string)

    return json_format_data
    # st.write(data[0])