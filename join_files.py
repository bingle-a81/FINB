# -*- coding: utf-8 -*-
import os, shutil, time, io

def serch_in_check_nomura(path_for_check):  # ищем файл в папке  со станков
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла

def common_files_nomura(path_for_check_join,machine):
    path_folder=os.path.join(path_for_check_join,machine)
    if os.path.isdir(path_folder+'-CHANGE') == False:
        os.makedirs(path_folder+'-CHANGE')
    for file in serch_in_check_nomura(path_folder):  # ищем файл в папке  со станков
        file_name = file.split('\\')[-1]  # имя файла файла со станков
        if '$2' not in file_name:
            file_name_2='$2$'+file_name
            if os.path.exists(os.path.join(path_folder,file_name_2)):
                first_file=open(os.path.join(path_folder,file_name),'r')
                second_file=open(os.path.join(path_folder,file_name_2),'r')
                common_file=open(os.path.join(path_folder+'-CHANGE',file_name),'w')

                a='\n$1\n'
                for line in first_file:
                    if '%' not in line:
                        a=a+line
                common_file.write(a)
                a='$2\n'
                for line in second_file:
                    if '%' not in line:
                        a=a+line
                    else:
                        a=a+'%'
                common_file.write(a)


def main():
    common_files_nomura(PATH_FOR_CHECK_JOIN)



# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
