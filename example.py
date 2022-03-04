import os

path = '/home/user/code/app-test/tradingview'


with os.scandir(path) as file:
    with open('file.txt', 'w') as files:
        for entry in file:
            if not entry.name.startswith('.') and entry.is_file() or entry.is_dir():
                print(entry.name)
                files.write(entry.name + '\n')