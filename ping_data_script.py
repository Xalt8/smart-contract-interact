import pandas as pd
import time

LOCKED = False

def wait_for_lock(func):
    ''' Decorator function to ensure that Ping & Pong 
        don't read/write to CSV file at the same time'''
    def wrapper(*args, **kwargs):
        global LOCKED
        if not LOCKED:
            LOCKED = True
            val = func(*args, **kwargs)
            LOCKED = False
            return val
        else:
            for i in range(10):
                if not LOCKED:
                    LOCKED = True
                    val = func(*args, **kwargs)
                    LOCKED = False
                    return val
                else:
                    time.sleep(2)
    return wrapper 


@wait_for_lock
def add_to_ping_csv(ping_data:tuple) -> None:
    ''' Takes in a tuple ('blockNumber', 'transactionHash')
        Checks to see if the transactionHash exists in the CSV
        If it does not exist -> add ping_data to the CSV '''
    _, transactionHash = ping_data
    pd_df = pd.read_csv('ping_data.csv')
    if not transactionHash in pd_df['transactionHash'].values:
        add_row = list(ping_data)
        add_row.append(0)
        pd_df.loc[len(pd_df)] = add_row
        pd_df.to_csv('ping_data.csv', index=False)
        print(f"Adding {ping_data} to ping_data.csv")


@wait_for_lock
def get_last_entry() -> tuple:
    ''' Returns the last row of the ping_data.csv as a tuple
        (blockNumber, transactionHash, PongStatus)'''
    pd_df = pd.read_csv('ping_data.csv')
    return tuple(pd_df.iloc[-1].values)


@wait_for_lock
def get_first_unPonged() -> tuple:
    ''' Returns the index and transactionHash of 
        first instance where PongStatus is 0 '''
    pd_df = pd.read_csv('ping_data.csv')
    index = pd_df.loc[pd_df['PongStatus'] == 0].head(1).index[0]
    tx_hash = pd_df.iloc[index]['transactionHash']
    return (int(index), tx_hash)


@wait_for_lock
def update_pong_status(index:int) -> None:
    ''' Updates the PongStatus in the CSV file to 1
        after a Pong event'''
    pd_df = pd.read_csv('ping_data.csv')
    pd_df.loc[index, 'PongStatus'] = 1
    pd_df.to_csv('ping_data.csv', index=False)


if __name__ == '__main__':
    
    # ping_df = pd.DataFrame(columns = ['blockNumber', 'transactionHash', 'PongStatus'])
    # ping_df.to_csv('ping_data.csv', index=False)

    print(get_first_unPonged())
