# -*- coding: utf-8 -*-
import json

def write_json(person_dict):
    try:
        data=json.load(open('pers.json'))
    except:
        data=[]
    data.append(person_dict)

    with open('pers.json','w') as file:
        json.dump(data,file,indent=2,ensure_ascii=False)