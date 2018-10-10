from src import (transactions, QuestionType)



def run_migrate():
  transactions([
#################
### meta
#################
    '''
CREATE TABLE IF NOT EXISTS
  questions
(
  id CHAR(2) PRIMARY KEY NOT NULL,
  name TEXT
)
    ''',
    '''
INSERT OR IGNORE INTO questions (id, name) VALUES ({}, 'choices')
    '''.format(QuestionType.types['choices']),
    '''
INSERT OR IGNORE INTO questions (id, name) VALUES ({}, 'choices_images')
    '''.format(QuestionType.types['choices_images']),
    '''
INSERT OR IGNORE INTO questions (id, name) VALUES ({}, 'wordcloud')
    '''.format(QuestionType.types['wordcloud']),

#################
### sessions
#################
    '''
CREATE TABLE IF NOT EXISTS
  sessions
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE,
  name TEXT,
  UNIQUE (date, name) ON CONFLICT REPLACE
)
    ''',
    '''
CREATE TABLE IF NOT EXISTS
  session_questions
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_name TEXT NOT NULL,
  question TEXT NOT NULL DEFAULT '',
  respondents INTEGER NOT NULL DEFAULT 0,
  question_type CHAR(2),
  session_id INTEGER NOT NULL,
  FOREIGN KEY (question_type) REFERENCES questions(id),
  FOREIGN KEY (session_id) REFERENCES sessions(id),
  UNIQUE (session_id, question_name) ON CONFLICT REPLACE
)
    ''',
    '''
CREATE TABLE IF NOT EXISTS
  session_answers
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  choice TEXT,
  votes INTEGER,
  response TEXT,
  FOREIGN KEY (question_id) REFERENCES session_questions(id)
)
    ''',
#################
### voters
#################
    '''
CREATE TABLE IF NOT EXISTS
  voters
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date DATE NOT NULL,
  session INTEGER NOT NULL,
  voter INTEGER NOT NULL,
  UNIQUE (session, voter) ON CONFLICT REPLACE
)
    ''',
    '''
CREATE TABLE IF NOT EXISTS
  voter_questions
(
  id INTEGER PRIMARY KEY,
  question TEXT NOT NULL,
  question_type CHAR(2),
  FOREIGN KEY (question_type) REFERENCES questions(id)
)
    ''',
    '''
CREATE TABLE IF NOT EXISTS
  voter_answer
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  response TEXT DEFAULT '',
  voter_id INTEGER NOT NULL,
  question_id INTEGER NOT NULL,
  FOREIGN KEY (voter_id) REFERENCES voters(id),
  FOREIGN KEY (question_id) REFERENCES voter_questions(id)
)
    '''
  ])
