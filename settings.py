# -*- coding: utf-8 -*-
import os, shutil, time

data_izm = (os.path.getmtime('c:\\4video\\8\\1306.PRG'))
# data_izm2 = (os.path.getmtime('c:\\4video\\8\\1337.PRG'))


data_izm = time.gmtime(data_izm)
a=(time.strftime('%d.%m.%Y', data_izm))

os.mkdir(a)

# if data_izm > data_izm2:
#     data_izm = time.gmtime(data_izm)
#     print(data_izm)
#     print('1357.PRG=', time.strftime('%x', data_izm))
# else:
#     data_izm2 = time.gmtime(data_izm2)
#     print('1337.PRG =', time.strftime('%x', data_izm2))
