# -*- coding: utf-8 -*-
import json
from random import choice

import poisk_modul



def poluch_att_file(*,path_file,razm,date_izm):

    person={
        'path': path_file,
        'razmer':razm,
        'data_chenge':date_izm
    }
    return person



def write_json(person_dict):
    try:
        data=json.load(open('pers.json'))
    except:
        data=[]
    data.append(person_dict)

    with open('pers.json','w') as file:
        json.dump(data,file,indent=2,ensure_ascii=False)
