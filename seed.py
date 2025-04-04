from random import randint
import sqlite3
import faker

NUMBER_USERS = 10
NUMBER_TASKS = 10
STATUS_NAMES = [('new',), ('in progress',), ('completed',)]

def get_fake_data(number_users: int, number_tasks: int, status_names: list[tuple]) -> tuple[list[tuple]]:
    fake_users = []
    fake_tasks = []
    number_statuses = len(status_names)

    fake_data = faker.Faker()

    for _ in range(number_users):
        fake_users.append((fake_data.name(), fake_data.email()))

    for _ in range(number_tasks):
        fake_tasks.append((fake_data.text(), fake_data.text(), randint(1, number_statuses), randint(1, number_users)))

    return fake_users, fake_tasks

def insert_data_to_db(users: list[tuple], status: list[tuple], tasks: list[tuple]) -> None:

    with sqlite3.connect('tasks.db') as con:

        cur = con.cursor()

        sql_to_users = """INSERT INTO users(full_name, email)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        sql_to_status = """INSERT INTO status(name)
                               VALUES (?)"""
        cur.executemany(sql_to_status, status)

        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id)
                               VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        con.commit()

if __name__ == "__main__":
    users_data, tasks_data = get_fake_data(NUMBER_USERS, NUMBER_TASKS, STATUS_NAMES)
    insert_data_to_db(users_data, STATUS_NAMES, tasks_data)
