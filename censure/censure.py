from utils.to_json import ToJson
import os

print(os.getcwd())
cur_dir = os.getcwd()

path = os.path.join(cur_dir, os.path.join('static', 'censure.txt'))  # r'/static/censure.txt'
print(path)
name = r'censure'

to_json = ToJson()

to_json.make(path=path, directory='static', name=name)
