from pydantic import BaseModel


class TaskSchema(BaseModel):
    '''Схема добавления задачи'''
    title: str
    description: str
    deadline: str 