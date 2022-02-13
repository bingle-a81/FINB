# -*- coding: utf-8 -*-
import json

import settings
import start_for_copy as st
import logging.config
from settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('json_logger')
# logger.addFilter(settings.CustomFilter())

# -----------------------------------------------------------------------
def chek_json(path_for_base):

    for file in st.serch_in_check(path_for_base):  #ищем файл в папке  со станков
        file_name_new = file.split('\\')[-1]  # имя файла файла со станков
        dir_file = '\\'.join(file.split(('\\'))[0:6])  # путь до папки в БД УП

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
                logger.info(f'{data[name_prog]}')
            else:
                continue


            ## Save our changes to JSON file
            jsonFile = open("guide.json", "w+", encoding="utf-8")
            jsonFile.write(json.dumps(data,indent=4,ensure_ascii=True))
            jsonFile.close()
        else:
            pass




def main():
    pass


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()