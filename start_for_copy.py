# -*- coding: utf-8 -*-
import os, shutil, time,io
import logging.config
from settings import logger_config
import re

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')

# PATH_FOR_SEARCH='//VLADIMIR//Users//Public//Alcohol.2.0.2.5629//Атлант//'   #папка где ищем
PATH_FOR_CHECK = 'C:\\4video\\8\\'  # папка проги со станков
PATH_FOR_BASE = 'C:\\4video\\9\\'  # папка УП/УП
PATH_FOR_COPY_NEW_FILES = 'C:\\4video\\10\\'  # копируем новые файлы

#***********************************************************************
def serch_in_check():
    for adress, dirs, files in os.walk(PATH_FOR_CHECK):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            # logger.debug(f'name={adress_file_in_check}')
            yield adress_file_in_check  # возвращаем адрес файла

# -----------------------------------------------------------------------

def attrib(file):
    date_of_change = os.path.getmtime(file)
    size_file = os.path.getsize(file)
    return [date_of_change, size_file]

# -----------------------------------------------------------------------


def serch_in_base(file_name):
    try:
        a=0
        for adress, dirs, files in os.walk(PATH_FOR_BASE):
            for file in files:
                if file == file_name:
                    adress_file_in_base = os.path.join(adress, file)
                    a=1
        if a==0:
            adress_file_in_base=None
            # logger.info(f'name file== {adress_file_in_base} ')
        yield adress_file_in_base  # возвращаем адрес файла
    except:
        logger.exception(f'Exception here ')


# -----------------------------------------------------------------------


def chenge_name(st=''):
    if st.rfind('.') >0:
        return st[0:st.rfind('.')]
    else:
        return st

# -----------------------------------------------------------------------

def correction_of_the_line(string):
    reg = re.compile('[^a-zA-Z0-9. ]')
    a=reg.sub('', string)
    return a

# -----------------------------------------------------------------------

def find_name_prog(path):
    with open(path,'r') as r:#только чтение файла
        i=0
        while i <3:
            st=r.readline()
            i += 1
            if '(' in st:
                f_name=st[(st.index('(')+1):(st.index(')'))].strip()
                f_name=correction_of_the_line(f_name)
                # logger.debug(f'name++{f_name}')
                return f_name
                break
            else:
                pass
        else:
            a=chenge_name(path.split('\\')[-1])
            # logger.debug(f'name=={a}')
            return chenge_name(path.split('\\')[-1])

# -----------------------------------------------------------------------


# ***********************************************************************
def start():
    quantity_old=0
    quantity_change=0
    quantity_new=0

    for file in serch_in_check():
        name_prog=find_name_prog(file)  # парсер названия
        file_name_new = file.split('\\')[-1]
        for file_name_old in serch_in_base(file_name_new):

            if file_name_old!=None:#программа встречалась
                lst.append(file_name_old)
                logger.error(f'lst={lst}')
                flag=all(attrib(i)[1]!=attrib(file)[1] for i in lst)
                lst = []
                if flag:  #новая версия старой программы
                    try:
                        dir_file_old = '\\'.join(file_name_old.split(('\\'))[0:7])
                        # logger.debug(f'dir {dir_file_old}')
                        date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                        if os.path.isdir(os.path.join(dir_file_old, date_of_change)) == False:
                            os.makedirs(os.path.join(dir_file_old, date_of_change))
                        shutil.copyfile(file, os.path.join(dir_file_old, date_of_change, file_name_new))
                        dir_file_old1 = '\\'.join(file_name_old.split(('\\'))[5:7])
                        quantity_change+=1
                        logger.info(
                            f'file {name_prog} copied to //{os.path.join(dir_file_old1, date_of_change, file_name_new)}')
                    except:
                        logger.exception(f'Exception here ')
                        pass
                else:        #такая программа уже есть
                    quantity_old += 1
                    logger.debug(f'file {name_prog} is here!Dont copy!')



            else:# абсолютно новая программа
                try:
                    date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                    if os.path.isdir(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change)) == False:
                        os.makedirs(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change))
                    shutil.copyfile(file, os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, date_of_change,
                                                       file_name_new))
                    quantity_new+=1
                    logger.info(f'file {name_prog} is new!!')
                except:
                    logger.exception(f'Exception here, item = {item}')
                    pass
    logger.info(f'старых файлов= {quantity_old} ')
    logger.info(f'измененных файлов= {quantity_change} ')
    logger.info(f'новых файлов= {quantity_new} ')
    logger.info(f'всего файлов= {quantity_new+quantity_old+quantity_change} ')
# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    if os.path.isfile('debug.log'): os.remove('debug.log')

    logger.info("Start ")
    start()
    logger.info("End")

# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
