from listner import pingpong_contract, web3, creds
from data_script import get_first_unPonged, update_pongStatus, get_last_ponged
import time
import threading


def build_transaction(nonce:int,  pingHash:str) -> dict:
    ''' Helper function that returns a trsnaction dictionary'''
    global pingpong_contract, creds, web3

    build_tx = pingpong_contract.functions.pong(pingHash).buildTransaction({
            'from':creds['METAMASK_ADDRESS'],
            'nonce':nonce,
            'maxFeePerGas':web3.toWei('2', 'gwei'),
            'maxPriorityFeePerGas': web3.toWei('1', 'gwei')})
    try: 
        _ = web3.eth.estimateGas(build_tx)
        return build_tx
    except ValueError: 
        print("build_transaction() error")
        return


def get_nonce()-> int:
    ''' Returns the max nonce of:
        - transaction count from wallet 
        - nonce from the last trasaction hash in database 
        Checks to see if the max nonce is higher than the nonce in 
        database if not increment the nonce'''

    global creds, web3
    tx_count_wallet = web3.eth.get_transaction_count(creds['METAMASK_ADDRESS'])
    if not get_last_ponged():
        return tx_count_wallet
    else:
        _,_, last_tx_hash, last_db_nonce = get_last_ponged()

        for i in range(50):
            try:
                last_tx = web3.eth.get_transaction(last_tx_hash)
            except:
                time.sleep(120)

        assert int(last_db_nonce) == last_tx.nonce, "tx_hash.nonce and db nonce are different"
        max_nonce = max(last_tx.nonce, tx_count_wallet)
        return max_nonce + 1 if max_nonce <= int(last_db_nonce) else max_nonce 
        

def account_balance() -> bool:
    ''' Checks to see if the wallet has sufficient 
        balance to make a transaction '''
    global creds
    account_bal_wei = web3.eth.get_balance(creds['METAMASK_ADDRESS'])
    account_bal_eth = float(web3.fromWei(account_bal_wei, 'ether')) 
    transaction_fee = 0.000023151000162057
    for _ in range(100):
        if account_bal_eth > transaction_fee:
            return True
        else:
            print("Top-up account balance")
            time.sleep(900)
    return False



def pong_transact() -> tuple:
    
    assert account_balance(), "Insufficient account balance"
    _nonce = get_nonce()
    _index, ping_hash = get_first_unPonged()
    build_tx = build_transaction(nonce=_nonce, pingHash=ping_hash)
    assert build_tx, "No transaction was built"
    signed_tx = web3.eth.account.sign_transaction(build_tx, creds['PRIVATE_KEY'])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=240)
    if tx_receipt.status == 1:
        update_pongStatus(index=_index, tx_hash=tx_hash.hex(), nonce=_nonce)
        result_available.set()
    

result_available = threading.Event()

def main():
    
    while True:
        
        thread = threading.Thread(target=pong_transact())
        thread.start()

        result_available.wait()


if __name__ == "__main__":
   
   main()