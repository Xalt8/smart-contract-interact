from listner import pingpong_contract, web3, creds
from ping_data_script import get_first_unPonged
import pandas as pd


index, ping_hash = get_first_unPonged()
nonce = 0

build_tx = pingpong_contract.functions.pong(ping_hash).buildTransaction({
        'from':creds['METAMASK_ADDRESS'],
        'nonce':nonce,
        'gas': 23200,
        'gasPrice':web3.eth.gas_price
    })

signed_tx = web3.eth.account.signTransaction(build_tx, creds['PRIVATE_KEY'])

# tx_hash = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(tx_hash)

# Get result
# Update database
# Update nonce
# Wait for result -> if not there replace transaction


# Keep a track of the nonce -> if transaction fails use the same nonce
# Eth.replace_transaction(transaction_hash, new_transaction) -> incase of fail

mm = '0x2c6970cd99cc15cb1db84abd20f45c108670cfae'

















if __name__ == "__main__":
    # print('Connected to Infura') if web3.isConnected() else print('Not connected to Infura')
    pass

