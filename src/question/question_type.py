class SqlQAnswer():
    def __init__(self, question_type, choice=None, votes=None, response=None):
        self.question_type = question_type
        self.choice = choice
        self.votes = votes
        self.response = response

    def print(self):
        return '{}'.format({
            'question_type': self.question_type,
            'choice': self.choice,
            'votes': self.votes,
            'response': self.response,
        })

    def __str__(self):
        return self.print()

    def __repr__(self):
        return self.__str__()


class QuestionType():
    types = {
        'choices': 1,
        'choices_images': 2,
        'wordcloud': 3,
    }

    def get_type(self):
        return QuestionType.types[self.type]

    def __init__(self, question_type):
        self.type = question_type

    def add_answer(self, _question, _answer):
        return NotImplemented

    def get_answers(self):
        return NotImplemented

    def __str__(self):
        return self.get_answers()

    def __repr__(self):
        return self.__str__()


class Choices(QuestionType):
    def __init__(self, question_type='choices'):
        self.votes = {}
        super().__init__(question_type)

    def add_answer(self, q, a):
        q_str = str(q)

        if q_str in ['Choices', 'No votes for this session']:
            return

        self.votes[q_str] = str(a)

    def get_answers(self):
        answers = []

        question_type = self.get_type()

        for choice, votes in self.votes.items():
            answers.append(SqlQAnswer(
                question_type,
                choice=choice,
                votes=votes
            ))

        return answers


class ChoicesImages(Choices):
    def __init__(self, question_type='choices_images'):
        self.votes = {}
        super().__init__(question_type)


class Wordcloud(QuestionType):
    def __init__(self, question_type='wordcloud'):
        super().__init__(question_type)

        self.responses = []

    def add_answer(self, q, _a):
        if q in ['Responses', 'No votes for this session']:
            return

        self.responses.append(str(q))

    def get_answers(self):
        q_type = self.get_type()
        return list(map(lambda response: SqlQAnswer(q_type, response=response), self.responses))


class Slide(QuestionType):
    def __init__(self, question_type='slide'):
        self.responses = []
        super().__init__(question_type)


TYPES = {
    'choices': Choices,
    'choices_images': ChoicesImages,
    'wordcloud': Wordcloud,
}


def get_question_type(question_type):
    if not question_type:
        return None

    question_type_str = str(question_type)

    if question_type_str in TYPES:
        return TYPES[question_type_str]()

    return None
