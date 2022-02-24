
from web3 import Web3
import streamlit as st
import json
from dotenv import load_dotenv
import os
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json, get_CID






load_dotenv()

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

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


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file.getvalue())

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

contract = load_contract()


st.title("Register New Artwork")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
name = st.text_input("What is the name of your car")
vin = st.text_input("What is the VIN of your car")

uploaded_file = st.file_uploader("what is the QR Code?")
st.write(uploaded_file)


if st.button("Register Artwork"):
    artwork_ipfs_hash = pin_artwork(name, uploaded_file)
    artwork_uri = f"ipfs://{artwork_ipfs_hash}"
    cid = get_CID(artwork_ipfs_hash)

    tx_hash = contract.functions.registerCar(
        address,
        name,
        vin,
        artwork_uri
    ).transact({'from': address, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.image(f"https://gateway.pinata.cloud/ipfs/{cid}")

st.markdown("---")


# st.write(pin_artwork(name, uploaded_file))

# token = contract.functions.balanceOf(address).call()

# token_id = st.selectbox("Artwork Tokens", list(range(token)))

# vin = contract.functions.registerCar(address,"elias","3ytrg45trgr","https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&fit=crop").transact({
#     "from":address,
#     "gas":1000000
# })

# receipt = w3.eth.wait_for_transaction_receipt(vin)

# if st.button("Display"):

#     # Use the contract's `ownerOf` function to get the art token owner
#     owner = contract.functions.ownerOf(token_id).call()

#     st.write(f"The token is registered to {owner}")

#     # Use the contract's `tokenURI` function to get the art token's URI
#     # token_uri = contract.functions.tokenURI(token_id).call()

#     # st.write(f"The tokenURI is {token_uri}")
#     # st.image(token_uri)
tokens = contract.functions.balanceOf(address).call()
st.write(f"This address owns {tokens} tokens")

# token_id = st.selectbox("Artwork Tokens", list(range(tokens)))

token_id = list(range(tokens))


# if st.button("Display"):
   

# Use the contract's `ownerOf` function to get the art token owner
owner = contract.functions.ownerOf(token_id[-1]).call()

st.write(f"The token is registered to {owner}")

# Use the contract's `tokenURI` function to get the art token's URI
token_uri = contract.functions.tokenURI().call()
st.write(f"The tokenURI is {token_uri}")
st.image(token_uri)