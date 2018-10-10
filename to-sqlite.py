from sys import (argv, exc_info)

from openpyxl import load_workbook

from src.inserts import (insert_sessions, insert_voters)
from src.voters import Voters
from src.sessions import get_sessions
from src.sql.transactions import close_connection
from src.migrate import run_migrate

wb = load_workbook(filename = argv[1] if len(argv) > 1 else r'data/urban-girls-movement-labb-1.xlsx')
run_migrate()

insert_sessions(get_sessions(wb))
insert_voters(Voters(wb['Voters']))

close_connection()
