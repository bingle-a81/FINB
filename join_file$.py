# -*- coding: utf-8 -*-
import os, shutil, time, io
import re

PATH_FOR_CHECK_JOIN = 'C:\\Users\\Programmer\\Desktop\\BDUP\\join_files\\'  # папка проги со станков
PATH_FOR_CHECK_JOIN_SUM = 'C:\\Users\\Programmer\\Desktop\\BDUP\\join_files_sum\\'
def serch_in_check(path_for_check):  # ищем файл в папке  со станков
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла

def main():
    for file in serch_in_check(PATH_FOR_CHECK_JOIN):  # ищем файл в папке  со станков
        file_name = file.split('\\')[-1]  # имя файла файла со станков
        if '$2' not in file_name:
            file_name_2='$2$'+file_name
            if os.path.exists(os.path.join(PATH_FOR_CHECK_JOIN,file_name_2)):
                with open(os.path.join(PATH_FOR_CHECK_JOIN,file_name), 'r') as file1:
                    lines = file1.readlines()
                str = '%'
                pattern = re.compile(re.escape(str))
                with open(os.path.join(PATH_FOR_CHECK_JOIN,file_name), 'w') as f:
                    for line in lines:
                        result = pattern.search(line)
                        if result is None:
                            f.write(line)
                with open(os.path.join(PATH_FOR_CHECK_JOIN,file_name), 'r') as file1:
                    data1 = file1.read()
                with open(os.path.join(PATH_FOR_CHECK_JOIN,file_name_2), 'r') as file2:
                    data2 = file2.read()
                with open(os.path.join(PATH_FOR_CHECK_JOIN_SUM, file_name), 'w') as file_sum:
                    file_sum.write('$1\n')
                    file_sum.write(data1)
                    file_sum.write('\n')
                    file_sum.write('$2\n')
                    file_sum.write(data2)
                    file_sum.write('\n')

# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
