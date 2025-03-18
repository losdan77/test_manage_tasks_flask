from flask import Flask, request, jsonify
from pydantic import ValidationError
from typing import List

from schemas import TaskSchema
from utils import validate_date


app = Flask(__name__)


tasks = [] 
next_id = 1


@app.route("/tasks", methods=["POST"])
def add_task():
    '''Функция добавление задачи, проверка на соответсвие входных данных
    pydantic схемы, првоерка формата даты, сохранение даты в формате строки
    и в формате datetime для дальнейшей сортировки в get запросе'''
    global next_id

    try:
        data = TaskSchema(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    deadline_date = validate_date(data.deadline)
    if not deadline_date:
        return jsonify({"error": "Неверный формат даты, необходимо вводить: DD-MM-YYYY"}), 400
    
    task = {
        "id": next_id,
        "title": data.title,
        "description": data.description,
        "deadline": data.deadline,
        "deadline_date": deadline_date
    }
    tasks.append(task)
    next_id += 1
    
    return jsonify(task), 200


@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    '''Функция вывода всех задач, сначала выводятся задачи у которых
    ближе дедлайн (по полю deadline_date, которое специально добавленно
    при вставке задач)'''
    sorted_tasks = sorted(tasks, key=lambda x: x["deadline_date"])
   
    return sorted_tasks


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    '''Функция удаления задачи по id, выполняется за 0(N)'''
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Задача удалена"}), 200


if __name__ == "__main__":
    app.run(debug=True)


# Как была придумана структура данных:
# 1) По условию было сказано использовать список для хранения задач (без БД);
# 2) Каждая задача хранится в виде словаря, поиск в словаре O(1);
# 3) Для избегания дубликатов id, используется переменная next_id;
# 4) Добавленно дополнительное поле deadline_date, типа datetime для
# сортировки задач по дате дедлайна, при выводе всех задач;
# 5) Pydantic для валидации данных

# Улучшение проекта для продакшена:
# 1) Использование FastAPI с uvicorn для лучшей производительности (асинхронный фреймворк);
# 2) Использование БД Postgres или MongoDB для хранения задач (асинхронное взаимодействие с ними);
# 3) Использование Redis для кеширования часто используемых запросов;
# 4) Использование Celery или отдельного сервиса для уведомления пользователей о подходящих дедлайнах;
# 5) Использования jwt access token и refresh_token для авторизации пользователей, возможно
# добавление oauth авторизации через сторонние сервисы;
# 6) Добавление логгирования и алертинга ошибок через Sentry;
# 7) Добавление дополнительных ручек для работы с задачами (напрмиер, изменение задач);
# 8) Покрытие кода тестами с помощью библиотеки pytest;
# 9) Развертывание сервисов в docker-compose.