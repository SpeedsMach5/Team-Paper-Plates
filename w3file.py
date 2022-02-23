#imports
import os
from dotenv import load_dotenv
from mnemonic import Mnemonic
from bip44 import Wallet
import sqlalchemy
import web3 as Web3
import pandas as pd
import pathlib as Path
#from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import middleware, Account
##########################################################################################
connection_string = "sqlite:///database_file.db"
engine = sqlalchemy.create_engine(connection_string)
df = pd.read_sql_table("Texas License Plates", con=engine) 
###########################################################################################
mnemonic = os.getenv("MNEMONIC")
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
wallet = Wallet(mnemonic)
private, public = wallet.derive_account("eth")
private
account = Account.privateKeyToAccount(private)
account_address = account.address
receiver = "0xD8E0962E8b6b805C4Dc4b1842736a98Fa2484AA9"
value = w3.toWei(amount, "ether")
gasEstimate = w3.eth.estimateGas({ 
    "to": receiver, 
    "from": account_address, 
    "value": value 
    })
w3.isConnected()
raw_tx = {
        "to": receiver,
        "from": account_address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account_address)
}

signed_tx = account.signTransaction(raw_tx)

w3.eth.sendRawTransaction(signed_tx.rawTransaction)

