import json

# concat extra data together
# e.g.[{name:xxx},{name:yyy}][{name:zzz}] -----> 
#     [{name:xxx}, {name:yyy}, {name:zzz}]
def concat_json(json_path):
    json_file = open(json_path, 'r')
    txt = ''

    if json_file.readable():
        txt = json_file.read()
        txt = txt.replace('][', ',')

    json_file = open(json_path, 'w')
    json_file.write(txt)


