# -*- coding: utf-8 -*-
import os,shutil,time

KEY_FOR_SEARCH='O1029'          #что ищем
PATH_FOR_SEARCH='//SERVER2016//Docs//УП//УП//Альфа Стил//'   #папка где ищем
PATH_FOR_COPY='C://4video//10//'    #папка дляя копирования(должна быть!)



def search():#поиск всех файлов в папках поиска
    for adress,dirs,files in os.walk(PATH_FOR_SEARCH):
        if adress == PATH_FOR_COPY:#не ищем в папке для копировани(частный случай)
            continue
        for file in files:
            data_izm = time.ctime(os.path.getatime(os.path.join(adress,file)))
            razmer=os.path.getsize(os.path.join(adress,file))
            print(file,'||',data_izm,'||',razmer)
            # if file.endswith('.PRG'): # условия отбора файла(расширение и тд)
            yield os.path.join(adress,file)#возвращаем адрес файла

def read_from_pathtxt(path):
    with open(path) as r:#только чтение файла
        for i in r:   #построчное чтение
            if KEY_FOR_SEARCH in i:#поиск по ключевому слову
                return copy(path)

def copy(path):

    file_name=path.split('\\')[-1]

    #разбиваем путь файла и  находим имя [-1]
    count=1 #счетчик если имена файлов одинаковые(файл в папке копирования уже есть)
    while True:
        if os.path.isfile(os.path.join(PATH_FOR_COPY,file_name)):
            if f'({count-1})' in file_name:
                file_name=file_name.replace(f'({count-1})','')
            file_name=f'({count}).'.join(file_name.split('.'))
            count+=1
        else:
            break

    shutil.copyfile(path,os.path.join(PATH_FOR_COPY,file_name))
    #копируем файл в папку
    print('file copy',file_name)

for i in search():#запускаем поиск
    try:
        read_from_pathtxt(i)#ищем ключевое слово
    except Exception as e:#обработчик ошибок(не та кодировка и др)
        with open(os.path.join(PATH_FOR_COPY,'errors.txt'),'a') as r:
            r.write(str(e)+'\n'+i+'\n')#пишем в файл errors.txt
