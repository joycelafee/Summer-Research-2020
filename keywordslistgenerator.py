#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 06:56:20 2020

@author: patrick
This class module will read an excel file and collects expected keywords
"""
import pandas as pd
 

class keywordsgenerator:
    def __init__(self, path, file, sheetname):
        self.path = path
        self.file = file
        self.WS = sheetname
    
    def googledatasetupbatch(self):
        df = pd.read_excel(self.path + self.file, sheet_name=self.WS)
        df = df[df['status'].isnull()]
        uniquelist = df[['geo','timeframe']].drop_duplicates()
        setupdict = {}
        indexs = uniquelist.index
        keys = range(len(uniquelist.index))
        for i in keys:
            geo = uniquelist.loc[indexs[i], 'geo']
            timeframe = uniquelist.loc[indexs[i], 'timeframe']
            filters = (df['geo'] == geo) & (df['timeframe'] == timeframe)
            keywordslist = df['keyword'][filters].to_list()
            setupdict[i] = [geo, timeframe, keywordslist]
        
        return setupdict
            
    def googledatasetup(self):
        df = pd.read_excel(self.path + self.file, sheet_name=self.WS)
        df = df.reset_index()
        df = df[df['status'].isnull()]
        df = df[['geo','timeframe','keyword','index']]
        setupdict = df.T.to_dict(orient='list')    
        return setupdict