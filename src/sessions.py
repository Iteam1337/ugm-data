from .question import (Question, is_meta, is_new_question)

def get_sessions(workbook):
    sessions = {}

    date = None

    sheets = [sheet for sheet in workbook.sheetnames if sheet.startswith('Session') and sheet != 'Session 1']

    for session_name in sheets:
        ws = workbook[session_name]

        questions = []
        question = None

        for row_number in range(1, ws.max_row):
            cell_q = ws.cell(row=row_number, column=1).value
            cell_a = ws.cell(row=row_number, column=2).value

            if not cell_q and not cell_a:
                continue

            if is_new_question(cell_q):
                if question:
                    questions.append(question)
                question = Question(cell_q)
                continue

            if not question:
                continue

            if is_meta(cell_q):
                question.add_meta(cell_q, cell_a)
                continue

            question.add_answer(cell_q, cell_a)

            if not date or question.before_date(date):
                date = question.get_date()

        sessions[session_name] = {
            'questions': questions,
            'date': date,
        }


    return sessions
