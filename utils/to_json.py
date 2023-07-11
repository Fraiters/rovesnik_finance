import json
import os


# класс для создания json файла из существующего
class ToJson:

    def make(self, path: str, directory: str, name: str):
        """
        Создание json файла
        :param path: путь до существующего файла
        :param directory: папка для создания json файла
        :param name: наименование json файла
        """
        # список слов
        words = []
        # формат
        format_file = r'.json'

        # заполнение списка слов
        with open(path, encoding='utf-8') as file:
            for line in file:
                word = line.lower().split('\n')[0]
                if word != '':
                    words.append(word)

        # создание json-файла со списком слов
        with open(os.path.join(directory, "".join([name, format_file])), 'w', encoding='utf-8') as file:
            json.dump(words, file)
