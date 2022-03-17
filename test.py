# import os
#
# # dir_name = "/home/user/code/app-test/tradingview"
# dir_name = "/home/user/code/app-test/tradingview/AO/ao.py"
#
# if os.path.isdir(dir_name):
#     print('Exist!')
# else:
#     print('This is not directory!')
#
# # message in Telegram
# # dir_name = "/path/to/dir"
# all_contains = list(filter(lambda x: os.path.isfile(os.path.join(dir_name, x)) and ".png" in x, os.listdir(dir_name)))
# all_contains.sort(key=lambda filename: int(filename.split(".")[0]))

import wsgiref.simple_server


def hello_world(environ, start_response):
    headers = [
        ('Content-type', 'text/plain; charset=utf-8'),
        ("Content–Security–Policy", "default–src 'none';"),
    ]
    start_response('200 OK', headers)
    return [b"hello world", ]


if __name__ == '__main__':
    with wsgiref.simple_server.make_server('', 8000, hello_world) as server:
        server.serve_forever()
