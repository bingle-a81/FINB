# -*- coding: utf-8 -*-
import json
from random import choice

import poisk_modul



def poluch_att_file(*,f_name,f_path,a):

    person={
        'name':f_name,
        'tel':f_path,
        'path':a
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


# write_json(poluch_att_file('5','7'))