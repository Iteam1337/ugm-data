from sqlite3 import (connect, Error)

con = connect('test.db')

def transactions(transactions):
    cur = con.cursor()

    try:
        cur.execute('begin')
        for transaction in transactions:
            cur.execute(transaction)

        cur.execute('commit')
    except Error as error:
        print('failed transaction', error)
        cur.execute('rollback')

def close_connection():
  con.close()
