import sqlite3

''' - Create 2 DBs -> One for the pings and another for pongs
    - Save the nonce in the pong DB 
    - For every ping start a process to emit a pong and monitor if it has gone through'''


conn = sqlite3.connect('pingpong.db')
c = conn.cursor()


def create_ping_table() -> None:
    global conn, c
    c.execute("""CREATE TABLE Ping (
        blockNumber integer PRIMARY KEY,
        transactionHash text NOT NULL
    ) """)
    conn.commit()



def data_in_ping_db(ping_data:tuple)-> bool:
    ''' Checks to see if a ping_data entry is already in the DB using the 
        unique transactionHash 
        Helper function for add_to_ping_db() '''
    global conn, c
    _, transactionHash = ping_data
    with conn:
        c.execute("SELECT * FROM Ping WHERE transactionHash=:transactionHash", {'transactionHash':transactionHash})
        instance = c.fetchone()
        return True if instance else False


def add_to_ping_db(ping_data:tuple) -> None:
    ''' If the data is not in the db -> adds data to db'''
    global conn, c
    blockNumber, transactionHash = ping_data
    if not data_in_ping_db(ping_data):    
        with conn:
            c.execute("INSERT INTO Ping VALUES (:blockNumber, :transactionHash)", {'blockNumber':blockNumber, 'transactionHash':transactionHash})
    print(f"added {(blockNumber, transactionHash)} to ping table")


def get_last_entry()-> tuple:
    ''' Returns the last row of data in the Ping db table ordered by blockNumber'''
    global conn, c
    with conn:
        c.execute('SELECT * FROM Ping ORDER BY blockNumber DESC LIMIT 1')
        return c.fetchone()


if __name__ == '__main__':
    # create_ping_table()
    pass
    