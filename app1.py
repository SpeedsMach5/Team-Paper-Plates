import os 
os.system('sudo apt-get install libzbar0')


################################################################################
# IMPORTS
################################################################################

from web3 import Web3
import streamlit as st
from dotenv import load_dotenv
import os
from Data.pinata import get_CID
from functions import load_contract, pin_artwork, pin_artwork, make_qr_quote, get_image_from_database, total_token_supply, vin_verification, qr_decoder, register_car,connect_to_db, get_qr_info
load_dotenv()



# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


#################################################################################
#Connect to DB

df = connect_to_db()
#################################################################################

#Input information 

contract = load_contract()

st.title("Register New Artwork")
accounts = w3.eth.accounts
address = st.selectbox("Select Account", options=accounts)
name = st.text_input("What is the person's name")
vin = st.text_input("What is the VIN of your car")
status = st.selectbox("Select the Status",df["License Plate Status"].unique(),index=2)
make = st.selectbox("What is the make of the vehicle?",df.Make.sort_values().unique())
model = st.selectbox("What is the model of the vehicle?",df.Model.sort_values().unique())
year = st.selectbox("What is the year of the vehicle?",df.Year.sort_values().unique())

#################################################################################
# QR CODE STUFF
#################################################################################

# my_bar = st.progress(0)
# import time



if st.button("Register License Plates"):
    with st.spinner('Creating your license plates...'):

        st.title("Mint License Plates")



        # for percent_complete in range(100):
        #     time.sleep(0.1)
        #     my_bar.progress(percent_complete + 1)
        
        #CALL THE QR GENERATOR FUNCTION  WITH ALL INPUT INFORMATION 
        qr_file = make_qr_quote(name, vin, status, make, model, year)
        

        # if uploaded_file is not None:
        file = get_image_from_database(name)
        # pin artwork to pinata
        artwork_ipfs_hash = pin_artwork(name,file)

        # get the uri
        artwork_uri = f"ipfs://{artwork_ipfs_hash}"

        # get the CID
        cid = get_CID(artwork_ipfs_hash)

        # mint NFT through the smart contract function registerCar()
        tx_hash = register_car(
            address,
            name,
            vin,
            status,
            artwork_uri)

        receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        #getting the json recipet for hash
        st.write("Transaction receipt mined:")

        if st.button("View Reciept"):
            st.write(dict(receipt))


        st.download_button("Download your reciept",data=(str(receipt)))
        # st.download_button("elias",)
        #view the link to the artwork - thinking of deleting this and only kepeing the pinata link as a preview - thoughts? 
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        ipfs_link = st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")

        st.image(f"https://gateway.pinata.cloud/ipfs/{cid}")
            #open the Image that was generated as a file
        with open(f"./temp/{name}.jpg","rb") as file:
            #give the user the option to download their QR code
            btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name=f"{name}.jpg",
                    mime="image/jpg")

        st.success('Congratulations, license plate registered!',)

#################################################################################
# NEW SECTION - THIS IS THE VERIFYING PROCESS
#################################################################################


st.markdown("---")
st.container()

st.title("Verify License Plates")
st.container()


qr_verify = st.file_uploader("Please upload your QR Code?")


#################################################################################
# FUNCTIONS TO FULFILL THE VERIFYING PROCESS
#################################################################################
if qr_verify:
    
    qr_decoder_file  = qr_decoder(qr_verify)
    name = qr_decoder_file["name"]
    vin = qr_decoder_file["vin"]
    status = qr_decoder_file["status"]
    make = qr_decoder_file["make"]
    model = qr_decoder_file["model"] 
    year = qr_decoder_file["year"]
    total_supply = total_token_supply()


    with st.spinner('Reading your license plates...'):
            
            
            message = vin_verification(total_supply, vin)            
            st.markdown("---")

            st.markdown("### QR Code Information")
            st.markdown(f"* **Name:** {name} \n * **Vin:** {vin} \n * **Status:** {status} \n * **Make:** {make} \n * **Model:** {model} \n * **Year:** {year}")
            st.markdown("---")
            st.markdown("### License Status")
            if message == "not in system":
                st.error("Your license plate is not in the system")
            else:
                st.success('Your registration has been found')



