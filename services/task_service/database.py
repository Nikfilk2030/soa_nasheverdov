import sqlite3
import uuid

import services.proto.service_pb2 as service_pb2

from services.task_service.task_service import EStatus

DATABASE = '/data/tasks.db'


def get_connection():
    return sqlite3.connect(DATABASE)


def get_task_from_tuple(task_tuple):
    task_id, username, content, date, tag = task_tuple
    return service_pb2.Task(
        id=task_id,
        username=username,
        content=content,
        date=date,
        tag=tag
    )


def create_task(task_id: int, username: str, content: str, date: str, tag: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO tasks (id, username, content, date, tag)
                          VALUES (?, ?, ?, ?, ?)''',
                       (task_id, username, content, date, tag))
        conn.commit()
        conn.close()

        return True

    except Exception:
        return False


def update_task(task_id: int, content: str, date: str, tag: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''UPDATE tasks
                          SET content=?, date=?, tag=?
                          WHERE id=?''',
                       (content, date, tag, task_id))
        if cursor.rowcount == 0:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    except Exception:
        return False


def delete_task(task_id: int) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM tasks WHERE id=?''', (task_id,))
        if cursor.rowcount == 0:
            conn.close()
            return False
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        return False


def get_task_by_id(task_id: int) -> (bool, service_pb2.Task):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM tasks WHERE id=?''', (task_id,))
        if cursor.rowcount == 0:
            conn.close()
            return False, service_pb2.Task()
        task_tuple = cursor.fetchone()

        conn.close()
        return True, get_task_from_tuple(task_tuple)

    except Exception as e:
        return False, service_pb2.Task()


def get_tasks(page_number: int, page_size: int) -> service_pb2.TaskList:
    offset = (page_number - 1) * page_size

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM tasks
            LIMIT ? OFFSET ?
        ''', (page_size, offset,))

        if cursor.rowcount == 0:
            conn.close()
            return service_pb2.TaskList(status=EStatus.ERROR)

        task_rows = cursor.fetchall()

        task_list = []

        for task_row in task_rows:
            task = get_task_from_tuple(task_row)
            task_list.append(task)

        conn.close()
        return service_pb2.TaskList(status=EStatus.SUCCESS, tasks=task_list)

    except Exception as e:
        return service_pb2.TaskList(status=EStatus.ERROR)

