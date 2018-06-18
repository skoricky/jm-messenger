import os
import json


class JRepository:
    """
    Базовый класс Хранилище (с примером сохранения в json)
    """
    pass


class JsonFileRepository(JRepository):
    DIR_NAME = 'json'
    FILE_NAME = 'test.json'
    FILE_PATH = os.path.join(os.path.dirname(__file__), os.path.abspath(f"{DIR_NAME}\\{FILE_NAME}"))

    def __init__(self, data):
        self.data = data
        self.set_datainfile()

    def set_datainfile(self):
        print(self.FILE_PATH)
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(self.data, file)


class PostgresDbRepository(JRepository):
    pass


class SqliteDbRepository(JRepository):
    pass


if __name__ == '__main__':
    data = {"name": "admin"}
    JsonFileRepository(data)
