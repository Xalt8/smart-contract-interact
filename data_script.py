import pandas as pd
import time

LOCKED = False

def wait_for_lock(func):
    ''' Decorator function to ensure that functions 
        don't read/write to CSV file at the same time 
        =============================================
        - Checks to see if the lock is enabled. If not then
        enables lock & executes the read/write and then
        disables the lock. 
        - If locked, then waits 2 seconds before 
        checking to see if the lock is diabled '''

    def wrapper(*args, **kwargs):
        global LOCKED
        for i in range(100):
            if not LOCKED:
                LOCKED = True
                val = func(*args, **kwargs)
                LOCKED = False
                return val
            else:
                time.sleep(2)
    return wrapper 


def create_csv() -> None:
    ''' Creates a CSV file called ping_data.csv 
        with columns headers -> 'blockNumber', 'transactionHash', 'PongStatus', Nonce 
        Contains no entries -> use add_to_ping_csv() to add data to CSV '''

    ping_df = pd.DataFrame(columns = ['blockNumber', 'transactionHash', 'PongStatus', 'Nonce']).astype(str)
    ping_df.to_csv('ping_data.csv', index=False)


@wait_for_lock
def add_to_ping_csv(ping_data:tuple) -> None:
    ''' Takes in a tuple ('blockNumber', 'transactionHash')
        checks to see if the transactionHash exists in the CSV
        If it does not exist -> adds ping_data, PongStatus=0 & Nonce=None to the CSV'''
    _, transactionHash = ping_data
    pd_df = pd.read_csv('ping_data.csv')
    if not transactionHash in pd_df['transactionHash'].values:
        add_row = list(ping_data) + ["No Pong", "None"]
        # add_row.extend(["No Pong", "None"])
        pd_df.loc[len(pd_df)] = add_row
        pd_df.to_csv('ping_data.csv', index=False)
        print(f"Adding {ping_data} to ping_data.csv")



@wait_for_lock
def get_last_entry() -> tuple:
    ''' Returns the last row of the ping_data.csv as a tuple
        (blockNumber, transactionHash, PongStatus, Nonce) if there are 
        entries otherwise returns None'''

    pd_df = pd.read_csv('ping_data.csv')
    return tuple(pd_df.iloc[-1].values) if pd_df.shape[0] > 0 else None
        


@wait_for_lock
def get_first_unPonged() -> tuple:
    ''' Returns the index and transactionHash of 
        first instance where PongStatus is 'No Pong' 
        ============================================
        Checks to see if there are any entries in the CSV 
        Checks for any 'No Pong' entries if none
        waits 5 minutes and re-checks '''

    for _ in range(50):
        pd_df = pd.read_csv('ping_data.csv')
        if (pd_df.shape[0] > 0) and (any(pd_df['PongStatus'] == "No Pong")):
            index = pd_df.loc[pd_df['PongStatus'] == "No Pong"].head(1).index[0]
            tx_hash = pd_df.iloc[index]['transactionHash']
            return (int(float(index)), tx_hash)
        else:
            time.sleep(300)


@wait_for_lock
def get_last_ponged() -> list:
    ''' Returns the last Ponged entry in the database '''
    pd_df = pd.read_csv('ping_data.csv')
    if (pd_df.shape[0] > 0) and (any(pd_df['PongStatus'] != "No Pong")):
        filter = pd_df['PongStatus'].values != 'No Pong'
        return list(pd_df[filter].values[-1])
    else:
        print('There are no ponged entries')
        return None


@wait_for_lock
def update_pongStatus(index:int, tx_hash:str, nonce:int) -> None:
    ''' Updates the PongStatus & Nonce in the CSV file after transaction'''
    assert isinstance(index, int), "index is not an int"
    assert isinstance(tx_hash, str), "tx_hash is not a str"
    pd_df = pd.read_csv('ping_data.csv')
    pd_df.at[index,'PongStatus'] = tx_hash
    pd_df.at[index,'Nonce'] = nonce
    pd_df.to_csv('ping_data.csv', index=False)
    print(f"Updating Pong Status at index {index}")



if __name__ == '__main__':
    
    create_csv()

    
    
