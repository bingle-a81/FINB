# -*- coding: utf-8 -*-
import os, shutil, time, io
import logging.config
from settings import logger_config
import re

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')

# PATH_FOR_SEARCH='//VLADIMIR//Users//Public//Alcohol.2.0.2.5629//Атлант//'   #папка где ищем
PATH_FOR_CHECK = 'C:\\Users\\Programmer\\Desktop\\BDUP\\Program_from_machine\\'  # папка проги со станков
# PATH_FOR_BASE = '//SERVER2016\\Docs\\УП\\АРХИВ\\УП\\'  # папка УП/УП
PATH_FOR_COPY_NEW_FILES = 'C:\\Users\\Programmer\\Desktop\\BDUP\\New_Program\\'  # копируем новые файлы
PATH_FOR_BASE = 'C:\\4video\\9\\УП\\УП\\'

# ***********************************************************************
def serch_in_check(path_for_check):   #ищем файл в папке  со станков
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла


# -----------------------------------------------------------------------

def serch_in_base(file_name):   #ищем файл в базе программ
    try:
        a = 0
        for adress, dirs, files in os.walk(PATH_FOR_BASE):
            for file in files:
                if file == file_name:
                    adress_file_in_base = os.path.join(adress, file)
                    yield adress_file_in_base  # возвращаем адрес файла
    except:
        logger.exception(f'Exception here ')


# -----------------------------------------------------------------------
def find_name_prog(path):   #из программы извлекаем имя файла в скобках
    with open(path, 'r') as r:  # только чтение файла
        i = 0
        while i < 4:
            st = r.readline() # чтение текстового файла построчно
            i += 1
            if '(' in st:
                f_name = st[(st.index('(') + 1):(st.index(')'))].strip()
                f_name = correction_of_the_line(f_name)
                # logger.debug(f'name++{f_name}')
                return f_name
                break
            else:
                pass
        else:
            a = chenge_name(path.split('\\')[-1]) # если в файле названия нет - берем имя файла
            # logger.debug(f'name=={a}')
            return chenge_name(path.split('\\')[-1])


# -----------------------------------------------------------------------

def find_name_machine(path):    #ищем название станка
    with open(path, 'r') as r:  # только чтение файла
        i = 0
        while i < 10:
            st = r.readline()
            i += 1
            if 'CITIZEN-L12' in st:
                return 'CITIZEN-L12'
            elif ';' in st:
                return 'TFC-125'
            elif 'G50X60.Y152.' in st:
                return 'NOMURA-20J2'
            elif 'G50X60.Y330.' in st:
                return 'NOMURA-16UBS'
            elif 'G50X20.' in st:
                return 'NOMURA-10E'
            elif 'NEX' in st or 'M98P7' in st or 'G50Z250.' in st:
                return 'NEXTURN-26PY'
            elif 'HANHWA' in st or 'M7' in st or 'G310Z210.0T2100' in st:
                return 'HANHWA-XDH20'
            elif 'MIYANO' in st or 'G50S' in st:
                return 'MIYANO-BNJ42SY'
            elif 'G92S' in st or 'COLCHESTER' in st:
                return 'COLCHESTER-T8MSY'
            elif 'G0G90G55G95' in st or 'G0G90G54G95' in st:
                return 'IRT-80'
        else:
            return "NONE"


# -----------------------------------------------------------------------


def attrib(file):   #получаем дату изменения  файла и размер
    date_of_change = os.path.getmtime(file)
    size_file = os.path.getsize(file)
    return [date_of_change, size_file]


# -----------------------------------------------------------------------


def chenge_name(st=''): # удаляем расширение файла
    if st.rfind('.') > 0:
        return st[0:st.rfind('.')]
    else:
        return st


# -----------------------------------------------------------------------

def correction_of_the_line(string): # удаляем символы кроме букв,цифр и точки
    reg = re.compile('[^a-zA-Z0-9. ]')
    a = reg.sub('', string)
    return a


# -----------------------------------------------------------------------


# ***********************************************************************
def start():
    quantity_old = 0 #счетчики
    quantity_change = 0
    quantity_new = 0

    for file in serch_in_check():  #ищем файл в папке  со станков
        file_name_new = file.split('\\')[-1] # имя файла файла со станков
        lst = [] # список одинаковых файлов
        for file_name_old in serch_in_base(file_name_new):#ищем файл в базе программ
            lst.append(file_name_old)   #добовляем в список
        # ========================================================================
        # logger.error(f'lst={lst}')
        name_prog = find_name_prog(file)  # парсер названия
        name_of_machine = find_name_machine(file)# парсер станка
        # logger.error(f'machine={name_of_machine}')
        if lst == []: # если список пустой то файл новый-копируем в папку для новых файлов
            try:
                date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                if os.path.isdir(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, name_prog,
                                              date_of_change)) == False:
                    os.makedirs(
                        os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, name_prog, date_of_change))
                shutil.copyfile(file, os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, name_prog,
                                                   date_of_change,
                                                   file_name_new))
                quantity_new += 1
                logger.info(f'file {name_prog} is new!!')
            except:
                logger.exception(f'Exception here, item = {item}')
                pass
        else:
            flag = all(attrib(i)[1] != attrib(file)[1] for i in lst)#проверка - изменился ли размер файлов в списке
            # logger.error(f'flag={flag}')
            if flag:  # новая версия старой программы
                try:
                    dir_file_old = '\\'.join(file_name_old.split(('\\'))[0:7]) # путь до папки в БД УП
                    # logger.info(f'dir {dir_file_old}')
                    date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                    if os.path.isdir(os.path.join(dir_file_old, name_of_machine, date_of_change)) == False:
                        os.makedirs(os.path.join(dir_file_old, name_of_machine, date_of_change))
                    shutil.copyfile(file, os.path.join(dir_file_old, name_of_machine, date_of_change, file_name_new))
                    dir_file_old1 = '\\'.join(file_name_old.split(('\\'))[5:7])
                    quantity_change += 1
                    logger.info(
                        f'file {name_prog} copied to //{os.path.join(dir_file_old1, name_of_machine, date_of_change, file_name_new)}')
                except:
                    logger.exception(f'Exception here ')
                    pass
            else:  # такая программа уже есть
                quantity_old += 1
                # logger.info(f'file {name_prog} is here!Dont copy!')

    logger.info(f'старых файлов= {quantity_old} ')
    logger.info(f'измененных файлов= {quantity_change} ')
    logger.info(f'новых файлов= {quantity_new} ')
    logger.info(f'всего файлов= {quantity_new + quantity_old + quantity_change} ')


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    if os.path.isfile('C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log'): os.remove(
        'C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log') # log файл

    logger.info("Start ")
    start()
    logger.info("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
