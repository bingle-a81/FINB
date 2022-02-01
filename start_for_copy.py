# -*- coding: utf-8 -*-
import os, shutil, time,io
import logging.config
from settings import logger_config



# PATH_FOR_SEARCH='//VLADIMIR//Users//Public//Alcohol.2.0.2.5629//Атлант//'   #папка где ищем
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
        i=0
        while i <  3:
            if '(' in lines[i]:
                return  (lines[i][lines[i].index('(') + 1:lines[i].index(')')]).strip()
                break
            else:
                i+=1
        else:
            return chenge_name(path.split('\\')[-1])



def main():
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('app_logger')
    logger.info("Start ")
    lst = []
    for file in serch_in_check():
        name_prog=find_name_prog(file)  # парсер названия
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

    # pass
    # print(serch_in_check())
    else:
        logger.info("End")


if __name__ == '__main__':
    main()
