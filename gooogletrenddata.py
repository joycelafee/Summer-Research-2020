#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 06:50:10 2020

@author: patrick

This script will generate google serach index data. Firstly, it reads expected
key words list from an excel file. Then it sends this list to google server and
collects data. Finally, it tranforms and saves data into a csv file

"""
import pandas as pd
import datetime as dt
import openpyxl 
from keywordslistgenerator import keywordsgenerator as keygen
from googledata import searchindexdata
prodtime = str(dt.datetime.today())
path = '/Users/patrick/Desktop/'
file = 'keywordinventory.xlsx'
sheetname = 'inventory'

keywordexcel = keygen(path, file, sheetname)
keyworddict = keywordexcel.googledatasetup()

wbk = openpyxl.load_workbook(path + file)
ws = wbk[sheetname]
df = pd.DataFrame()

for keyindex, value in keyworddict.items():
    print(keyindex, ":", value)
    googledata = searchindexdata([value[2]])
    try:
        data = googledata.datagenerator(value[1], value[0])
        data = data.reset_index()
        data['keyword'] = value[2]
        data = data.rename(columns={value[2]:'value'})
        # put prod date into the columns of status prodtime
        ws.cell(row=value[3]+2, column=4).value = prodtime
    except:
        print('no data')
    df = df.append(data, sort=None)

wbk.save(path + file)
# save data file with today's data
df.to_csv(path + 'googlesearchindexdata_' + prodtime + '.csv')