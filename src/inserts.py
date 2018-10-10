from .sql.transactions import con

def insert_sessions(sessions):
    sessions_inserts__meta = []
    sessions_inserts__questions = []
    sessions_inserts__answers = []

    for session_name, session_info in sessions.items():
        questions = session_info['questions']
        date = session_info['date']
        sessions_inserts__meta.append((date, session_name))

        for question in questions:
            sql = question.to_sql()

            sessions_inserts__questions.append((
                sql.name,
                sql.question,
                sql.respondents,
                sql.type,
                # # # # # # # # # # #
                date,
                session_name,
            ))

            for answer in sql.answers:
                sessions_inserts__answers.append((
                    answer.choice,
                    answer.votes,
                    answer.response,
                    # get session_questions_id
                    date,
                    session_name,
                    sql.name,
                    answer.question_type,
                ))

    # create sessions
    con.executemany('INSERT INTO sessions (date, name) VALUES (?, ?)', sessions_inserts__meta)
    con.commit()

    # create session_questions
    con.executemany('''
    INSERT INTO session_questions (
        question_name,
        question,
        respondents,
        question_type,
        session_id)
    VALUES (
        ?,
        ?,
        ?,
        ?,
        (SELECT id FROM sessions WHERE date = ? AND name = ?)
    )
    ''', sessions_inserts__questions)
    con.commit()

    # create session_answers
    con.executemany('''
    INSERT INTO session_answers (
        choice,
        votes,
        response,
        question_id)
    VALUES (
        ?,
        ?,
        ?,
        (SELECT id FROM session_questions WHERE
            session_id = (SELECT id FROM sessions WHERE date = ? AND name = ?)
                AND question_name = ?
                AND question_type = ?)
    )
    ''', sessions_inserts__answers)
    con.commit()

def insert_voters(voters):
    con.executemany('''
    INSERT OR IGNORE INTO
        voter_questions
            (id, question, question_type)
    VALUES
        (?, ?, ?)
    ''', voters.questions)
    con.executemany('''
    INSERT OR IGNORE INTO
        voters
            (date, session, voter)
    VALUES
        (?, ?, ?)
    ''', voters.voters)
    con.commit()

    for answers in voters.answers:
        voter_id = answers[0]
        for i in range(1, len(answers) - 1):
            con.execute('''
            INSERT OR IGNORE INTO
                voter_answer
                    (response, voter_id, question_id)
            VALUES
                (?, ?, ?)
            ''', (answers[i], voter_id, voters.questions[i - 1][0]))

    con.commit()



