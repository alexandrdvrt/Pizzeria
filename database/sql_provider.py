import os
from string import Template


class SQLProvider:
    def __init__(self, sql_path: str) -> None:
        self._scripts = {}  # Хранить шаблоны наших SQL-запросов из файла
        for file in os.listdir(sql_path):
            self._scripts[file] = Template(open(f'{sql_path}/{file}').read())

    def get(self, name: str, params: dict) -> str:
        return self._scripts[name].substitute(**params)
