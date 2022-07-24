from listner import pingpong_contract, web3, creds
from data_script import get_first_unPonged, update_pongStatus
import asyncio


def build_transaction(nonce:int,  pingHash:str, gasEstimate=23200) -> dict:
    ''' Helper function that returns a trsnaction dictionary'''
    global pingpong_contract, creds, web3

    build_tx = pingpong_contract.functions.pong(pingHash).buildTransaction({
            'from':creds['METAMASK_ADDRESS'],
            'nonce':nonce,
            'gas': gasEstimate,
            'gasPrice':web3.eth.gas_price})
    try: 
        _ = web3.eth.estimateGas(build_tx)
        return build_tx
    except ValueError: 
        return
    

async def main():

    while True:
        account_bal = web3.eth.get_balance(creds['METAMASK_ADDRESS'])
        assert account_bal > 0.00005787, "Insufficient account balance"
        
        _index, ping_hash = get_first_unPonged()
        
        _nonce = web3.eth.get_transaction_count(creds['METAMASK_ADDRESS'])
        
        build_tx = build_transaction(nonce=_nonce, pingHash=ping_hash)
        assert build_tx, "No transaction was built"
        
        signed_tx = web3.eth.account.sign_transaction(build_tx, creds['PRIVATE_KEY'])
        
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=240)
        assert tx_receipt.status == 1, "No transaction receipt"
        
        update_pongStatus(index=_index, tx_hash=tx_hash.hex())
        


if __name__ == "__main__":
   
   asyncio.run(main())
    # _nonce = web3.eth.get_transaction_count(creds['METAMASK_ADDRESS'])
    # print(_nonce)