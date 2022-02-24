#################################################################################################################

# this is a testing page not to be included in the production final. This will need to be deleted.

#################################################################################################################
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
import os
load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

@st.cache(allow_output_mutation=True)
def load_contract():
    # TODO: Load the contract’s ABI details next

    with open(Path('../contracts/compiled/abi.json')) as f:
        artwork_abi = json.load(f)

        contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

        contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
)
        return contract

contract = load_contract()

st.title("Register New Artwork")
accounts = w3.eth.accounts
address = st.selectbox("Select Artwork Owner", options=accounts)
artwork_uri = st.text_input("The URI to the artwork")

if st.button("Register Artwork"):
    #  Web3 code goes here

    tx_hash = contract.functions.registerArtwork(address, artwork_uri).transact({
    "from": address,
    "gas": 1000000
})

receipt = w3.eth.waitForTransactionReceipt(tx_hash)
st.write("Transaction receipt mined:")
st.write(dict(receipt))



