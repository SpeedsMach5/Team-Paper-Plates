from distutils.command.upload import upload
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import qrcode
load_dotenv()
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json
# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
################################################################################


#@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('abi.json')) as f:
        artwork_abi = json.load(f)

    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Load the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract

contract = load_contract()

qr_img= st.file_uploader("upload your QR")
################################################################################
# Register New Artwork
################################################################################
st.title("Verify License PLate Status")
accounts = w3.eth.accounts
# Use a streamlit component to get the address of the artwork owner from the user
address = st.selectbox("Vehicle Information", options=accounts)

# Use a streamlit component to get the artwork's URI
artwork_uri = st.text_input("Register VIN")

if st.button("Register Vin-number"):

    # Use the contract to send a transaction to the registerArtwork function
    tx_hash = contract.functions.registerArtwork(
        address,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))

st.markdown("---")

################################################################################
# Display a Token
################################################################################
st.markdown("## Display the QR code")

selected_address = st.selectbox("Select Account", options=accounts)

tokens = contract.functions.balanceOf(selected_address).call()

st.write(f"This address owns {tokens} tokens")

token_id = st.selectbox("Artwork Tokens", list(range(tokens)))

if st.button("Display"):

    # Use the contract's `ownerOf` function to get the art token owner
    
    owner = contract.functions.ownerOf(token_id).call()

    st.write(f"The token is registered to {owner}")

    # Use the contract's `tokenURI` function to get the art token's URI
    token_uri = contract.functions.tokenURI(token_id).call()

    st.write(f"The tokenURI is {token_uri}")
    st.image(token_uri)
#################################################################################
#QR code section 

import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data("API CALL")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
st.write(img)
#img.save("QR_Code_Image.jpg")