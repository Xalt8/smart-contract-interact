import json
from web3 import Web3
from ping_data_script import add_to_ping_csv, get_last_entry
import time


with open('credentials.txt', 'r') as f:
    file_contents = [f.strip() for f in f.readlines()]
    file_contents = [f.split(" = ") for f in file_contents]
    creds = {lst[0]:lst[1] for lst in file_contents}    

web3 = Web3(Web3.HTTPProvider(creds['ENDPOINT1']))


pingpong_address = '0x7D3a625977bFD7445466439E60C495bdc2855367'
with open('pingpong_abi.json', 'r') as j:
    pingpong_abi= json.loads(j.read())

pingpong_contract = web3.eth.contract(address=pingpong_address, abi=pingpong_abi)

START_BLOCK = 32611135


def get_blockNum_transHash(start_block:int) -> list[tuple]:
    ''' Returns a list of tuples with the blockNumber & transactionHash 
        of all events from the start_block parameter till the latest block
        Prints message if no entries where found '''
    
    event_filter = web3.eth.filter({"address": pingpong_address, 'fromBlock':start_block, 'toBlock':'latest'})
    entries = event_filter.get_all_entries()
    if entries:
        return [(entry['blockNumber'], entry['transactionHash'].hex()) for entry in entries]
    else:
        print('Got no entries')


def main():
    
    start_entries = get_blockNum_transHash(START_BLOCK)
    for entry1 in start_entries:
        add_to_ping_csv(entry1)    

    while True:
        time.sleep(300) # wait 5 minutes
        last_blockNumber,_,_ = get_last_entry()
        entries = get_blockNum_transHash(int(last_blockNumber))
        for entry in entries:
            add_to_ping_csv(entry)



# Get Kovan eth
# Send pong for every ping
# Handle event listner problems
# Handle mining problems -> Pong doesn't get mined -> high gas
    # Re-send the same transaction with the same nonce but higher gas price
# Write to DB and check pings against pongs
    # Create 2 DBs -> One for the pings and another for pongs
    # Save the nonce in the pong DB

if __name__ == '__main__':
    
    print('Connected to Infura') if web3.isConnected() else print('Not connected to Infura')
    
    main()
    # ping_hash = '0x82ea0cc9a3311c74c0b7d8ea896474eb4444d43edd6157d48708f2d62100b2ef'

    # build_tx = pingpong_contract.functions.pong(ping_hash).buildTransaction({
    #     'from':00000,
    #     'nonce':0,
    #     'gas': 100000,
    #     'gasPrice':2000000
    # })

    # print(build_tx)