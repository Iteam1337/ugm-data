'''
Creates a sqlite db from a xlxs file

This script first expects _you_ to have a excel-file anywhere accessable by
this file, default is in `data/*.xlsx`
It then tries to run migrations on _your_ sqlite-db-file which it then tries
to fill with content
'''
from sys import argv

from openpyxl import load_workbook

from src.inserts import (insert_sessions, insert_voters)
from src.voters import Voters
from src.sessions import get_sessions
from src.sql.transactions import close_connection
from src.migrate import run_migrate


if __name__ == '__main__':
    WORKBOOK = load_workbook(filename=argv[1] if len(
        argv) > 1 else r'data/urban-girls-movement-labb-1.xlsx')
    run_migrate()

    insert_sessions(get_sessions(WORKBOOK))
    insert_voters(Voters(WORKBOOK['Voters']))

    close_connection()
