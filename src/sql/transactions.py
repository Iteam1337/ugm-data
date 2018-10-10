from sqlite3 import (connect, Error)

DB_CON = connect('test.db')


def transactions(sql_transactions):
    cur = DB_CON.cursor()

    try:
        cur.execute('begin')
        for transaction in sql_transactions:
            cur.execute(transaction)

        cur.execute('commit')
    except Error as error:
        print('failed transaction', error)
        cur.execute('rollback')


def close_connection():
    DB_CON.close()
