# -*- coding: utf-8 -*-
import os,shutil,time
import json_modl as js
import parser_nc

KEY_FOR_SEARCH='1'          #что ищем
# PATH_FOR_SEARCH='//VLADIMIR//Users//Public//Alcohol.2.0.2.5629//Атлант//'   #папка где ищем
PATH_FOR_SEARCH='C:\\4video\\9\\'   #папка где ищем
PATH_FOR_COPY='C:\\4video\\10\\'    #папка дляя копирования(должна быть!)



def search():#поиск всех файлов в папках поиска
    for adress,dirs,files in os.walk(PATH_FOR_SEARCH):
        if adress == PATH_FOR_COPY:#не ищем в папке для копировани(частный случай)
            continue
        for file in files:
            file_in_folder=os.path.join(adress, file)
            parser_nc.pars(file_in_folder)
            js.write_json(js.poluch_att_file(path_file=attrib(file_in_folder)[0],razm=attrib(file_in_folder)[1]
                                             ,date_izm=attrib(file_in_folder)[2]))
            # if file.endswith('.PRG'): # условия отбора файла(расширение и тд)
            yield os.path.join(adress,file)#возвращаем адрес файла
# -------------------=====================--------------------------
def attrib(file_in_folder):
    data_izm = time.ctime(os.path.getatime(file_in_folder))
    razmer = os.path.getsize(os.path.join(file_in_folder))
    name_f=file_in_folder
    lst=[name_f,razmer,data_izm]
    return lst
# -------------------=====================--------------------------
def read_from_pathtxt(path):
    with open(path) as r:#только чтение файла
        for i in r:   #построчное чтение
            if KEY_FOR_SEARCH in i:#поиск по ключевому слову
                return copy(path)

def copy(path):

    file_name=path.split('\\')[-1]

    #разбиваем путь файла и  находим имя [-1]
    # count=1 #счетчик если имена файлов одинаковые(файл в папке копирования уже есть)
    # while True:
    #     if os.path.isfile(os.path.join(PATH_FOR_COPY,file_name)):
    #         if f'({count-1})' in file_name:
    #             file_name=file_name.replace(f'({count-1})','')
    #         file_name=f'({count}).'.join(file_name.split('.'))
    #         count+=1
    #     else:
    #         break
    if os.path.isdir(os.path.join(PATH_FOR_COPY,file_name))==False:
        os.mkdir(os.path.join(PATH_FOR_COPY,file_name))
    ff=os.path.join(PATH_FOR_COPY,file_name,file_name)
    print('pp',path)
    print('a',ff)
    shutil.copyfile(path,ff)
    #копируем файл в папку
    print('file copy',file_name)



def main():
    for i in search():  # запускаем поиск
        try:
            read_from_pathtxt(i)  # ищем ключевое слово
        except Exception as e:  # обработчик ошибок(не та кодировка и др)
            with open(os.path.join(PATH_FOR_COPY, 'errors.txt'), 'a') as r:
                r.write(str(e) + '\n' + i + '\n')  # пишем в файл errors.txt
   # js.write_json(poluch_att_file(poisk_modul.att()))

if __name__ == '__main__':
    main()