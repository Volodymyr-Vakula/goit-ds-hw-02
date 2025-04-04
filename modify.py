import sqlite3
import re
from random import randint
import faker
from seed import NUMBER_USERS, STATUS_NAMES, NUMBER_TASKS

def execute_query(sql: str) -> list[tuple]:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()
    
def modify_data(sql: str) -> None:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()

def print_results(selection: list[tuple]) -> None:
    for el in selection:
        print(f"{el}\n")
    print()

if __name__ == "__main__":

    user_id = randint(1, NUMBER_USERS)
    status_id = randint(1, len(STATUS_NAMES))
    task_id = randint(1, NUMBER_TASKS)

    fake_data = faker.Faker()
    task_title = fake_data.text()
    full_name = fake_data.name()

    task_description = "NULL"

    # Task 1 (select)
    select = f"""
    SELECT * FROM tasks
    WHERE user_id = {user_id}
    """
    # print("\nTask 1:\n")
    # print_results(execute_query(select))

    # Task 2 (select)
    select = f"""
    SELECT * FROM tasks
    WHERE user_id = {user_id}
    AND status_id = {status_id}
    """
    # print("\nTask 2:\n")
    # print_results(execute_query(select))

    # Task 3 (update)
    update = f"""
    UPDATE tasks
    SET status_id = {status_id}
    WHERE id = {task_id}
    """
    # select = f"""
    # SELECT * FROM tasks
    # WHERE id = {task_id}
    # """
    # print("\nTask 3:\n")
    # print_results(execute_query(select))
    modify_data(update)
    # select = f"""
    # SELECT * FROM tasks
    # WHERE id = {task_id}
    # """
    # print_results(execute_query(select))

    # Task 4 (select)
    select = """
    SELECT id, full_name FROM users as u
    WHERE u.id NOT IN (SELECT user_id from tasks)
    """
    # print("\nTask 4:\n")
    # print_results(execute_query(select))

    # Task 5 (insert)
    insert = f"""
    INSERT INTO tasks(title,description,status_id,user_id)
    VALUES('{task_title}', {task_description}, {status_id}, {user_id})
    """
    modify_data(insert)
    # print("\nTask 5:\n")
    # select = """
    # SELECT * FROM tasks
    # WHERE id = (SELECT MAX(id) from tasks)
    # """
    # print_results(execute_query(select))

    # Task 6 (select)
    select = """
    SELECT * FROM tasks
    WHERE NOT status_id = 3
    """
    print("\nTask 6:\n")
    print_results(execute_query(select))

    # Task 7 (delete)
    delete = f"""
    DELETE from TASKS where id = {task_id}
    """
    modify_data(delete)
    # select = """
    # SELECT * FROM tasks
    # """
    # print("\nTask 7:\n")
    # print_results(execute_query(select))

    # Task 8 (select)
    select = f"""
    SELECT email FROM users
    WHERE id = {user_id}
    """
    email = execute_query(select)[0][0]
    pattern = email[1:3]
    select = f"""
    SELECT * FROM users
    WHERE email LIKE '%{pattern}%'
    """
    # print("\nTask 8:\n")
    # print(email)
    # print(f"pattern: {pattern}\n")
    # print_results(execute_query(select))

    # Task 9 (update)
    update = f"""
    UPDATE users
    SET full_name = '{full_name}'
    WHERE id = {user_id}
    """
    # select = f"""
    # SELECT * FROM users
    # WHERE id = {user_id}
    # """
    # print("\nTask 9:\n")
    # print_results(execute_query(select))
    modify_data(update)
    # select = f"""
    # SELECT * FROM users
    # WHERE id = {user_id}
    # """
    # print_results(execute_query(select))

    # Task 10 (select)
    select = """
    SELECT COUNT(t.status_id), s.name
    FROM tasks as t
    LEFT JOIN status as s ON t.status_id = s.id
    GROUP by s.name
    ORDER by s.id
    """
    # print("\nTask 10:\n")
    # print_results(execute_query(select))

    # Task 11 (select)
    select = f"""
    SELECT email FROM users
    WHERE id = {user_id}
    """
    email = execute_query(select)[0][0]
    re_pattern = r"@[\w\.]*"
    match = re.search(re_pattern, email)
    pattern = match.group()
    select = f"""
    SELECT t.id, t.title, t.description, t.status_id, t.user_id, u.email
	FROM tasks as t
    LEFT JOIN users as u ON t.user_id = u.id
    WHERE u.email LIKE '%{pattern}%'
    ORDER by t.id
    """
    # print("\nTask 11:\n")
    # print(f"Pattern: {pattern}\n")
    # print_results(execute_query(select))

    # Task 12 (select)
    select = """
    SELECT *
	FROM tasks
    WHERE description IS NULL
    ORDER by id
    """
    # print("\nTask 12:\n")
    # print_results(execute_query(select))

    # Task 13 (select)
    task_status = "in progress"
    select = f"""
    SELECT u.id, u.full_name, t.id, t.title, t.description, s.name
    FROM users AS u
	INNER JOIN tasks AS t ON u.id = t.user_id
    INNER JOIN status AS s ON t.status_id = s.id
    WHERE s.name = '{task_status}'
    ORDER by u.id, t.id
    """
    # print("\nTask 13:\n")
    # print_results(execute_query(select))

    # Task 14 (select)
    select = """
    SELECT u.id, u.full_name, COUNT(t.id)
    FROM users AS u
	LEFT JOIN tasks AS t ON u.id = t.user_id
    GROUP by u.id
    ORDER by u.id
    """
    # print("\nTask 14:\n")
    # print_results(execute_query(select))
