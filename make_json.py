# -*- coding: utf-8 -*-
import json
import os
import start_for_copy as st




# Key:value mapping
# student = {
#     "Name": "Peter",
#     "Roll_no": "0090014",
#     "Grade": "A",
#     "Age": 20
# }

# jsonFile = open("guide.json", "r")  # Open the JSON file for reading
# data = json.load(jsonFile)  # Read the JSON into the buffer
# jsonFile.close()  # Close the JSON file
#
# ## Working with buffered content
# tmp = data["Name"]
# print(tmp)
# data["Name"] = 'path'
# for i in range(10):
#     data["mode"+str(i)] = "replay"
#
# ## Save our changes to JSON file
# jsonFile = open("guide.json", "w+")
# jsonFile.write(json.dumps(data,indent=4))
# jsonFile.close()




def main():
    path_for_base = '//SERVER2016\\Docs\\УП\\АРХИВ\\УП\\'  # папка УП/УП

    for file in st.serch_in_check(path_for_base):  #ищем файл в папке  со станков
        file_name_new = file.split('\\')[-1]  # имя файла файла со станков
        dir_file = '\\'.join(file.split(('\\'))[0:7])  # путь до папки в БД УП
        # extension=any([file.endswith('jpg'),file.endswith('jpg')])
        print(file.split('.')[-1])
        a = [file.endswith(a) for a in
             ['jpg', 'pdf', 'bin', 'PDF', 'doc', 'zip', 'lnk', 'exe', 'db', 'docx', 'png', 'bmp', 'ICO', 'bat', '0L',
              '0C', 'gif', 'GIF','bmp','vbs','css','dtd','htm','htm','pptx','iso','sfv','prt','x_b','STEP','ipt','cdd','djvu',
              '__meta__','xlsx','PNG','tcl','dll','frw','bak','out','cdw','log','m3d','tif','rar','xls','spw','JPG']]
        if any(a) != True:
            name_prog = st.find_name_prog(file)  # парсер названия
            jsonFile = open("guide.json", "r", encoding="utf-8")  # Open the JSON file for reading
            data = json.load(jsonFile)  # Read the JSON into the buffer
            jsonFile.close()  # Close the JSON file
            if name_prog not in data:
                data[name_prog] = dir_file
            else:
                print(name_prog,'=Yes')

            ## Save our changes to JSON file
            jsonFile = open("guide.json", "w+", encoding="utf-8")
            jsonFile.write(json.dumps(data,indent=4,ensure_ascii=False))
            jsonFile.close()
        else:
            print('34')







    # path_for_check = 'C:\\Users\\Programmer\\Desktop\\BDUP\\Program_from_machine\\'
    # for file in st.serch_in_check(path_for_check):  #ищем файл в папке  со станков
    #     file_name_new = file.split('\\')[-1] # имя файла файла со станков
    #     name_prog = st.find_name_prog(file)  # парсер названия
    #     for file_name_old in st.serch_in_base(file_name_new):
    #         dir_file_old = '\\'.join(file_name_old.split(('\\'))[0:7])  # путь до папки в БД УП
    #         # print(file_name_new,'==',dir_file_old)
    #         jsonFile = open("guide.json", "r")  # Open the JSON file for reading
    #         data = json.load(jsonFile)  # Read the JSON into the buffer
    #         jsonFile.close()  # Close the JSON file
    #         if file_name_new not in data:
    #             data[file_name_new] = dir_file_old
    #         else:
    #             print(file_name_new,'=Yes')
    #
    #         ## Save our changes to JSON file
    #         jsonFile = open("guide.json", "w+")
    #         jsonFile.write(json.dumps(data,indent=4))
    #         jsonFile.close()


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()