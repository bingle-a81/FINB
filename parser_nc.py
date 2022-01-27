# -*- coding: utf-8 -*-
import poisk_modul

def pars(file_in_folder):
    with open(file_in_folder) as r:#только чтение файла
        for i in r:   #построчное чтение
            if 'O' in i:
                return i[i.index('(') + 1:i.index(')')]






if __name__ == '__main__':
    ...
