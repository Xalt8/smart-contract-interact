import time
import csv

LOCKED = False

def wait_for_lock(func):
    ''' Decorator function to ensure that functions 
        don't read/write to CSV file at the same time'''
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


@wait_for_lock
def create_csv() -> None:
    ''' Creates a CSV file called ping_data.csv 
        with 3 columns -> 'blockNumber', 'transactionHash', 'PongStatus' 
        Contains no entries -> use add_to_ping_csv() to add data to file '''

    with open('ping_data2.csv', 'w') as new_file:
        csv_writer = csv.writer(new_file, delimiter=',')
        csv_writer.writerow(['blockNumber', 'transactionHash', 'PongStatus'])


@wait_for_lock
def add_to_ping_csv(ping_data:tuple) -> None:
    ''' Takes in a tuple ('blockNumber', 'transactionHash')
        Checks to see if the transactionHash exists in the CSV
        If it does not exist -> add ping_data + No Pong to CSV'''
    _, transactionHash = ping_data
    with open('ping_data2.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if transactionHash not in [line['transactionHash'] for line in csv_reader]:
            add_row = list(ping_data)
            add_row.append("No Pong")
            with open('ping_data2.csv', 'a', newline='') as csv_file_append:
                csv_writer = csv.writer(csv_file_append)
                csv_writer.writerow(add_row)
                print(f"Adding {ping_data} to csv file")

@wait_for_lock
def get_last_entry() -> list:
    ''' Returns the last row of the ping_data.csv as a tuple
        (blockNumber, transactionHash, PongStatus) if there are 
        entries otherwise returns None'''
    
    with open('ping_data2.csv', 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        lines = [list(line.values()) for line in csv_reader]
        return lines[-1] if lines else None
        

@wait_for_lock
def get_first_unPonged() -> tuple:
    ''' Returns the index and transactionHash of 
        first instance where PongStatus is 'No Pong' 
        ============================================
        Checks to see if there are any entries in the CSV 
        then if there are any 'No Pong' instances if not
        waits 2 minutes and re-checks '''
    for _ in range(20):
        with open('ping_data2.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            lines = [list(line.values()) for line in csv_reader if line['PongStatus'] == 'No Pong'] 
            return lines[0] if lines else time.sleep(120)


@wait_for_lock
def update_pongStatus(index:int, tx_hash:str) -> None:
    ''' Updates the PongStatus & Nonce in the CSV file after transaction'''
    pass


if __name__ == '__main__':
    
    # create_csv()
    
    # pd = (987654321, '0x8b7307d22786478e4ebcd8ba5c6ef8042fa20c818d42ad7eeb3e0c18e604795i')
    # add_to_ping_csv(pd)

    unponged = get_first_unPonged()
    print(unponged)
    