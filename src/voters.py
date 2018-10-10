from math import floor

from .question.question_type import QuestionType

# @ | 64
# A | 65 <-
CHAR_BEGIN = ord('A') - 1
# Z | 64 + 26 <-
# [ | 64 + 27
MAX_CHAR = ord('Z') + 1 - CHAR_BEGIN

QUESTION_COLUMN_BEGIN = 'D'


def max_column_char(columns):
    max_num = floor(columns / MAX_CHAR)
    lpad = max_column_char(max_num) if max_num > 1 else ''
    char_num = max(columns - (MAX_CHAR * max_num), 0) + CHAR_BEGIN
    return lpad + chr(char_num)


class Voters():
    def __init__(self, worksheet):
        question_row = None

        lists = {
            'questions': list(),
            'answers': list(),
            'voters': list(),
        }


        for row_number in range(1, worksheet.max_row):
            if question_row:
                break

            font = worksheet.cell(row=row_number, column=1).font
            if not font or not font.color or font.color.rgb != 'FFFFFFFF':
                continue

            question_row = row_number

        if not question_row:
            raise KeyError('Can not find voter summary')

        max_column = max_column_char(worksheet.max_column)
        questions_ws = worksheet['{2}{0}:{1}{0}'.format(
            question_row, max_column, QUESTION_COLUMN_BEGIN)][0]
        new_max = None
        j = ord(QUESTION_COLUMN_BEGIN) - CHAR_BEGIN - 1
        for i in range(0, len(questions_ws)):
            j = j + 1

            q_value = questions_ws[i].value

            value = str(q_value).replace(
                ':', '') if q_value and 'resultatet' not in str(q_value) else None

            if not value:
                if not new_max:
                    new_max = j
                continue
            else:
                new_max = None

            lists['questions'].append((i, value, QuestionType.types['choices']))

        if new_max:
            max_column = max_column_char(new_max)

        for row_number in range(question_row + 1, worksheet.max_row):
            rows = worksheet['A{0}:{1}{0}'.format(row_number, max_column)][0]

            lists['voters'].append(tuple(map(lambda r: r.value, rows[:3])))
            lists['answers'].append(tuple(map(lambda r: r.value, rows[2:])))

        self.questions = lists['questions']
        self.answers = lists['answers']
        self.voters = lists['voters']
