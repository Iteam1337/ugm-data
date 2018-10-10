import moment

from .question_type import (QuestionType, get_question_type)


class SqlQuestion():
    def __init__(self, from_question):
        meta = from_question.meta
        question = from_question.question
        answers = question.get_answers()

        _type = QuestionType.types[str(meta.get('type'))]

        self.date = str(meta.get('date'))
        self.type = _type
        self.question = str(meta.get('question'))
        self.respondents = str(meta.get('respondents'))
        self.answers = answers if answers != _type else None
        self.name = str(meta.get('name'))

    def print(self):
        out = {
            'date': self.date,
            'type': self.type,
            'question': self.question,
            'respondents': self.respondents,
            'answers': self.answers,
            'name': self.name,
        }
        return '{}'.format(out)

    def __repr__(self):
        return self.print()

    def __str__(self):
        return self.print()


class Question():
    handled_types = [
        'Date',
        'Session',
        'Type',
        'Question',
        'Respondents',
    ]

    def __init__(self, name):
        self.meta = {
            'date': None,
            'type': None,
            'question': None,
            'respondents': None,
            'name': name
        }
        self.question = None

    def add_meta(self, question_type, value):
        if not question_type in Question.handled_types:
            return

        meta_type = str(question_type).lower()

        if meta_type == 'type':
            self.question = get_question_type(str(value))

        self.meta[meta_type] = str(value)

    def add_answer(self, question, answer):
        if not self.question:
            return

        self.question.add_answer(question, answer)

    def before_date(self, date):
        this_date = str(self.meta.get('date'))

        if not date:
            return True

        if not this_date:
            return False

        return moment.date(this_date) < moment.date(date)

    def get_date(self):
        return str(self.meta.get('date'))

    def to_sql(self):
        return SqlQuestion(self)

    def _print(self):
        if not self.question:
            return ''

        answers = self.question.get_answers()
        _type = str(self.meta.get('type'))

        out = {
            'date': str(self.meta.get('date')),
            'type': _type,
            'question': str(self.meta.get('question')),
            'respondents': str(self.meta.get('respondents')),
            'answers': answers if answers != _type else None,
            'name': str(self.meta.get('name')),
        }

        return '{}'.format(out)

    def __repr__(self):
        return self._print()

    def __str__(self):
        return self._print()


def is_new_question(question):
    return question and str(question).startswith('Question ')


def is_meta(question):
    return question and str(question) in Question.handled_types
