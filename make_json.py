# -*- coding: utf-8 -*-
import json
import os

PATH_FOR_BASE = 'C:\\Users\\Programmer\\Desktop\\BDUP\\B_DATA\\'  # папка УП/УП

# class MyEncoder(json.JSONEncoder):
#     def default(self, o) :
#         if isinstance(o,set):
#             return list(o)
#         return o


def write_json(person_dict):
    with open('guide.json','a') as file:
        json.dump(person_dict,file,indent=2,ensure_ascii=False)


def serch_in_check():   #ищем файл в папке  со станков
    for adress, dirs, files in os.walk(PATH_FOR_BASE):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла

def main():
    for file in serch_in_check():  # ищем файл в папке  со станков
        file_name_new = file.split('\\')[-1]  # имя файла файла со станков
        program_dict={file_name_new:file}
        write_json(program_dict)


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()