# Excel-to-sqlite

To install:

```sh
pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
# or
pip install -r requirements.txt --user
# or
sudo pip install -r requirements.txt
# or ...
```

To run:

```sh
python3 to-sqlite.py
# or
python3 to-sqlite.py data/urban-girls-movement-labb-1.xlsx
```

At the moment it only creates/updates a sqlite-db called test.db in the project root


To get started with the content:

```sql
select *
  from voter_answers as answer
  left join voter_questions question
    on answer.question_id = question.id
  left join voters voter
    on answer.voter_id = voter.id
  order by voter.id;
```
