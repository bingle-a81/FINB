# -*- coding: utf-8 -*-
import os, shutil, time, io
import logging.config
from settings import logger_config
import re
import json
import make_json
import join_files
from smtp_post import send_email

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')

TO_ADDR_MAIL="workmy327@aol.com"


PATH_FOR_CHECK = 'C:\\Users\\Programmer\\Desktop\\BDUP\\STANKI\\'  # папка проги со станков
PATH_FOR_BASE = '//SERVER2016\\Docs\\УП\\УП-2\\'  # папка УП/УП
PATH_FOR_COPY_NEW_FILES = 'C:\\Users\\Programmer\\Desktop\\BDUP\\New_Program\\'  # копируем новые файлы
ARCHIVE_PROGRAMM = '//SERVER2016\\Docs\\УП\\АРХИВ\\BdUp\\'

#
# PATH_FOR_CHECK = 'C:\\Users\\Programmer\\Desktop\\BDUP\\STANKI\\'  # папка проги со станков
# PATH_FOR_BASE = 'C:\\Users\\Programmer\\Desktop\\BDUP\\BAZA\\'  # папка УП/УП
# PATH_FOR_COPY_NEW_FILES = 'C:\\Users\\Programmer\\Desktop\\BDUP\\BAZA_NEW\\'  # копируем новые файлы
# ARCHIVE_PROGRAMM = 'C:\\Users\\Programmer\\Desktop\\BDUP\\BAZA_arhiv\\'


# ***********************************************************************
def serch_in_check(path_for_check):  # ищем файл в папке  со станков
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла


# -----------------------------------------------------------------------

def serch_in_base(path_for_base, file_name):  # ищем файл в базе программ
    try:
        a = 0
        for adress, dirs, files in os.walk(path_for_base):
            for file in files:
                if file == file_name:
                    adress_file_in_base = os.path.join(adress, file)
                    yield adress_file_in_base  # возвращаем адрес файла
    except:
        logger.exception(f'Exception here ')


# -----------------------------------------------------------------------
def find_name_prog(path):  # из программы извлекаем имя файла в скобках
    with open(path, 'r') as r:  # только чтение файла
        i = 0
        while i < 4:

            st = r.readline()  # чтение текстового файла построчно
            i += 1
            if ('(' in st) and (')' in st):
                f_name = st[(st.index('(') + 1):(st.index(')'))].strip()
                f_name = correction_of_the_line(f_name)
                # logger.debug(f'name++{f_name}')
                return f_name
                break
            else:
                pass
        else:
            a = chenge_name(path.split('\\')[-1])  # если в файле названия нет - берем имя файла
            # logger.debug(f'name=={a}')
            return chenge_name(path.split('\\')[-1])


# -----------------------------------------------------------------------

def find_name_machine(folder_machine,path):  # ищем название станка
    lisst = ['nomura20-1-CHANGE', 'nomura20-2-CHANGE', 'nomura20-3-CHANGE']
    if any([i == folder_machine for i in lisst]):
        a = 'NOMURA-20J2'
    elif folder_machine == 'nomura10-CHANGE':
        a = 'NOMURA-10E'
    elif folder_machine == 'colchester':
        a = 'COLCHESTER'
    elif folder_machine == 'hanhwa':
        a = 'HANHWA-XDH20'
    elif folder_machine == 'miano':
        a = 'MIYANO-BNJ42SY'
    elif folder_machine == 'nexturn12':
        a = 'NEXTURN-12B'
    elif folder_machine == 'nexturn26':
        a = 'NEXTURN-26PY'
    elif folder_machine == 'nomura16':
        a = 'NOMURA-16UBS'
    elif folder_machine == 'sitizen-1':
        a = 'CITIZEN-L12(1)'
    elif folder_machine == 'sitizen-2':
        a = 'CITIZEN-L12(2)'
    elif folder_machine == 'NONE':
        citizen_lst=['CITIZEN-L12','G630','#814']
        nomura20_lst = ['NOMURA-20','G50X60.Y152.','G50X252.Y0.']
        nomura10_lst = ['NOMURA-10', 'G50X20.', 'G50X0.Z0.']
        nomura16_lst = ['NOMURA-16', 'G50X60.Y330.', 'M131M231']
        tfc_125_lst = [';']
        nexturn26py_lst = ['NEXTURN26PY', 'M98P7','G50Z250.' ]
        nexturn12b_lst = ['NEXTURN-12', 'G3000','G310Z160.T2000']
        hanhwa_lst=['HANHWA','G310Z210.0T2100']
        myano_lst=['MIYANO','M94','M177']
        colhester_lst=['COLCHESTER','G10P']
        itr_lst=['G0G90G55G95','G0G90G54G95']
        a='NONE'
        with open(path, 'r') as r:  # только чтение файла
            for line in r:
                if any([x in line for x in citizen_lst]) :
                    a='CITIZEN-L12(1)'
                    with open(path, 'r') as r1:
                        for line in r1:
                            if 'G165' in line:
                                a='CITIZEN-L12(2)'
                elif any([x in line for x in nomura20_lst]) :
                    a='NOMURA-20J2'
                elif any([x in line for x in nomura10_lst]) :
                    a='NOMURA-10E'
                elif any([x in line for x in nomura16_lst]) :
                    a='NOMURA-16UBS'
                elif any([x in line for x in tfc_125_lst]) :
                    a='TFC-125'
                elif any([x in line for x in nexturn26py_lst]) :
                    a='NEXTURN-26PY'
                elif any([x in line for x in nexturn12b_lst]) :
                    a='NEXTURN-12B'
                elif any([x in line for x in hanhwa_lst]) :
                    a='HANHWA-XDH20'
                elif any([x in line for x in myano_lst]) :
                    a='MIYANO-BNJ42SY'
                elif any([x in line for x in colhester_lst]) :
                    a='COLCHESTER'
                elif any([x in line for x in itr_lst]) :
                    a='IRT-80'
    return a
# -----------------------------------------------------------------------


def attrib(file):  # получаем дату изменения  файла и размер
    date_of_change = os.path.getmtime(file)
    size_file = os.path.getsize(file)
    return [date_of_change, size_file]


# -----------------------------------------------------------------------


def chenge_name(st=''):  # удаляем расширение файла
    if st.rfind('.') > 0:
        return st[0:st.rfind('.')]
    else:
        return st


# -----------------------------------------------------------------------

def correction_of_the_line(string):  # удаляем символы кроме букв,цифр и точки
    reg = re.compile('[^a-zA-Z0-9. -]')
    a = reg.sub('', string)
    return a

# ***********************************************************************
def start(folder_machine):
    time_start=time.localtime()
    counter_start=time.perf_counter()
    text_email = f'Проверка станка {folder_machine} начата в {time.strftime("%H:%M:%S", time_start)}\n'
    logger.info(f'****************************')
    logger.info(f'machine= {folder_machine} ')
    quantity_old = 0  # счетчики
    quantity_change = 0
    quantity_new = 0

    for file in serch_in_check(os.path.join(PATH_FOR_CHECK,folder_machine)):  # ищем файл в папке  со станков
        file_name_new = file.split('\\')[-1]  # имя файла файла со станков
        name_prog = find_name_prog(file)  # парсер названия
        lst = []  # список одинаковых файлов
        jsonFile = open("guide.json", "r", encoding="utf-8")  # Open the JSON file for reading
        json_data = json.load(jsonFile)  # Read the JSON into the buffer
        jsonFile.close()
        if name_prog in json_data:  #если имя файла есть в json-файле - то путь берем оттуда
            path_for_base = json_data[name_prog]
        else:
            path_for_base = PATH_FOR_BASE #иначе ищем в базе УП(общий путь)

        for f in serch_in_base(path_for_base, file_name_new):  # ищем файл в базе программ
            name_prog_old = find_name_prog(f)  # парсер названия
            if name_prog_old == name_prog:
                file_name_old = f
                lst.append(file_name_old)  # добовляем в список
            else:
                continue

        name_of_machine = find_name_machine(folder_machine,file)  # парсер станка
        # logger.error(f'machine={name_of_machine}')

        if lst == []:  # если список пустой то файл новый-копируем в папку для новых файлов
            try:
                date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                if os.path.isdir(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, date_of_change)) == False:
                    os.makedirs(os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, date_of_change))
                shutil.copyfile(file, os.path.join(PATH_FOR_COPY_NEW_FILES, name_prog, name_of_machine, date_of_change,
                                                   file_name_new))
                if os.path.isdir(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine)) == False:
                    os.makedirs(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine))
                shutil.copyfile(file, os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine,file_name_new))
                quantity_new += 1
                logger.info(f'file {name_prog} is new!!')

            except:
                logger.exception(f'Exception here, item = {item}')
                pass
        else:
            flag = all(attrib(i)[1] != attrib(file)[1] for i in lst)  # проверка - изменился ли размер файлов в списке
            # logger.error(f'flag={flag}')
            if flag:  # новая версия старой программы
                try:
                    dir_file_old = '\\'.join(file_name_old.split(('\\'))[0:6])  # путь до папки в БД УП
                    # logger.info(f'dir {dir_file_old}')
                    date_of_change = time.strftime('%d.%m.%Y', time.gmtime(attrib(file)[0]))
                    if os.path.isdir(os.path.join(dir_file_old, name_of_machine, date_of_change)) == False:
                        os.makedirs(os.path.join(dir_file_old, name_of_machine, date_of_change))
                    shutil.copyfile(file, os.path.join(dir_file_old, name_of_machine, date_of_change, file_name_new))

                    if os.path.isdir(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine)) == False:
                        os.makedirs(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine))
                    shutil.copyfile(file, os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine,file_name_new))

                    dir_file_old1 = '\\'.join(file_name_old.split(('\\'))[4:6])
                    quantity_change += 1
                    logger.info(
                        f'file {name_prog} copied to //{os.path.join(dir_file_old1, name_of_machine, date_of_change, file_name_new)}')
                except:
                    logger.exception(f'Exception here ')
                    pass
            else:  # такая программа уже есть
                quantity_old += 1
                logger.info(f'file {name_prog} is {file_name_old}!Dont copy!')
                if os.path.isdir(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine)) == False:
                    os.makedirs(os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine))
                shutil.copyfile(file, os.path.join(ARCHIVE_PROGRAMM, name_prog, name_of_machine, file_name_new))

    logger.info(f'старых файлов= {quantity_old} ')
    logger.info(f'измененных файлов= {quantity_change} ')
    logger.info(f'новых файлов= {quantity_new} ')
    logger.info(f'всего файлов= {quantity_new + quantity_old + quantity_change} ')
    # --------------------------------------------------------------
    # отправка  email
    time_finish = time.localtime()
    counter_end = time.perf_counter()
    text_email += f'Проверка станка {folder_machine} закончена в {time.strftime("%H:%M:%S", time_finish)}\n ' \
                  f'Время проверки {time.strftime("%H:%M:%S", time.gmtime(counter_end - counter_start))} \n' \
                  f'старых файлов= {quantity_old} \n' \
                  f'измененных файлов= {quantity_change} \n' \
                  f'новых файлов= {quantity_new} \n' \
                  f'всего файлов= {quantity_new + quantity_old + quantity_change} \n'

    subject_email=f'Cheak machine  {folder_machine}'
    send_email(TO_ADDR_MAIL, subject_email, text_email)# отправка  письма
    print(text_email)
# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    counter_start1=time.perf_counter()
    if os.path.isfile('C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log'): os.remove(
        'C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log')  # log файл
    source='C:\\Users\\Programmer\\Desktop\\pro\\STANKI\\'
    shutil.copytree(source,PATH_FOR_CHECK, dirs_exist_ok=True) #клонируем папки в папку для разбора
    folders_nomura = ['nomura20-1', 'nomura20-2', 'nomura20-3', 'nomura10']
    folders_machine_new_program = ['nomura20-1-CHANGE', 'nomura20-2-CHANGE', 'nomura20-3-CHANGE', 'nomura10-CHANGE',
                                   'colchester', 'hanhwa', 'miano', 'nexturn12', 'nexturn26', 'nomura16', 'sitizen-1',
                                   'sitizen-2', 'NONE']
    # folders_machine_new_program = [ 'NONE']
    for x in folders_nomura:
        join_files.common_files_nomura(PATH_FOR_CHECK, x)  # объединяем файлы номура.

    if (time.time())-os.path.getmtime("guide.json")>1:#если файл бд не обновлялся больше месяца-обновляем(60*60*24*30)
        logger.info("Start json")
        make_json.chek_json(PATH_FOR_BASE)
        logger.info("end json")

    logger.info("Start ")
    for x in folders_machine_new_program:
        start(x)
    logger.info("End")
    counter_end1=time.perf_counter()
    text=f'Время проверки {time.strftime("%H:%M:%S", time.gmtime(counter_end1-counter_start1))} \n'

    with open('C:\\Users\\Programmer\\Desktop\\BDUP\\debug.log') as r:
        text+=r.read()


    send_email(TO_ADDR_MAIL, 'File log debug.log ', text)
# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
