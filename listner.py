import json
from web3 import Web3
from data_script import add_to_ping_csv, get_last_entry
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


def get_blockNum_transHash(start_block:int) -> list[tuple]:
    ''' Returns a list of tuples with the blockNumber & transactionHash 
        of all events from the start_block parameter till the latest block
        Prints message if no entries where found '''
    global pingpong_contract
    # event_filter = web3.eth.filter({"address": pingpong_address, 'fromBlock':start_block, 'toBlock':'latest'})
    event_filter = pingpong_contract.events.Ping.createFilter(fromBlock=start_block, toBlock='latest')
    entries = event_filter.get_all_entries()
    if entries:
        return [(entry['blockNumber'], entry['transactionHash'].hex()) for entry in entries]
    else:
        print('Got no entries')


def main():
    
    START_BLOCK = 32885325

    start_entries = get_blockNum_transHash(START_BLOCK)
    for entry1 in start_entries:
        add_to_ping_csv(entry1)    

    while True:
        time.sleep(300) # wait 5 minutes
        last_blockNumber,_,_ = get_last_entry()
        entries = get_blockNum_transHash(int(last_blockNumber))
        for entry in entries:
            add_to_ping_csv(entry)


if __name__ == '__main__':
    
    print('Connected to Infura') if web3.isConnected() else print('Not connected to Infura')
    
    main()


