# -*- coding: utf-8 -*-
import os, shutil, time,io

PATH_FOR_CHECK = 'C:\\4video\\8\\'  # папка проги со станков
PATH_FOR_BASE = 'C:\\4video\\9\\'  # папка УП/УП
PATH_FOR_COPY_NEW_FILES = 'C:\\4video\\10\\'  # копируем новые файлы


def serch_in_check():
    for adress, dirs, files in os.walk(PATH_FOR_CHECK):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла


def attrib(file):
    date_of_change = os.path.getmtime(file)
    size_file = os.path.getsize(file)
    return [date_of_change, size_file]


def serch_in_base(file_name):
    for adress, dirs, files in os.walk(PATH_FOR_BASE):
        for file in files:
            if file == file_name:
                adress_file_in_base = os.path.join(adress, file)
                yield adress_file_in_base  # возвращаем адрес файла


def chenge_name(st=''):
    if st.rfind('.') >0:
        return st[0:st.rfind('.')]
    else:
        return st

def find_name_prog(path):
    with open(path,'r') as r:#только чтение файла
        lines = r.readlines()
        if 'O' in lines[0]:
            return (lines[0][lines[0].index('(') + 1:lines[0].index(')')]).strip()
        else:
            pass
        if '(' in lines[1]:
            return  (lines[1][lines[1].index('(') + 1:lines[1].index(')')]).strip()
        else:
            pass
        if '(' in lines[2]:
            return (lines[2][lines[2].index('(') + 1:lines[2].index(')')]).strip()
        else:
            return chenge_name(path.split('\\')[-1])


def main():
    lst = []
    for file in serch_in_check():
        name_prog=find_name_prog(file)  # ищем ключевое слово

        file_name_new = file.split('\\')[-1]
        for file_name_old in serch_in_base(file_name_new):
            lst.append(file_name_old)

        flag=all(attrib(i)[1]!=attrib(file)[1] for i in lst)

        if flag :
            date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))

            if os.path.isdir(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change)) == False:
                os.makedirs(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change))
            shutil.copyfile(file,os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change,
                                               file_name_new))
        else:

            date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
            if os.path.isdir(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change)) == False:
                os.makedirs(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change))
            shutil.copyfile(file, os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change,
                                               file_name_new))




    pass
    # print(serch_in_check())


if __name__ == '__main__':
    main()
