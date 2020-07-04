#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 06:57:47 2020

@author: patrick
ref: 
    1. pytrend: https://medium.com/@yanweiliu/getting-the-google-trends-data-with-python-67b335e7d1cf
    2. normalization: https://medium.com/@rrfd/standardize-or-normalize-examples-in-python-e3f174b65dfc
This module will send key words list to google and generate expected data

"""
import numpy as np
from pytrends.request import TrendReq

class searchindexdata:
    """this class is search index data class"""
    def __init__(self, keywords):
        self.keywords = keywords
    @classmethod
    def serverconfig(self, hl='en-US', tz=360):
        pytrend = TrendReq(hl=hl, tz=tz, retries=10, backoff_factor=0.5)
#        pytrend = TrendReq(hl=hl, tz=tz, timeout=(10,25), 
#                           proxies=['https://34.203.233.13:80',], retries=2, 
#                           backoff_factor=0.1, requests_args={'verify':False})
        return pytrend

    def datagenerator(cls, timeframe='all', geo='US', cat = 0, gprop=''):
        pytrend = cls.serverconfig()
        pytrend.build_payload(kw_list=cls.keywords,
                              cat=cat,
                              timeframe=timeframe,
                              geo=geo,
                              gprop=gprop)
        data = pytrend.interest_over_time()      
        data= data.drop(labels=['isPartial'],axis='columns')
        datamatrix = data[cls.keywords].to_numpy()
        data['normalized value'] = searchindexdata.normlization(datamatrix)
        data['geo'] = geo
        return data
    @staticmethod
    def normlization(inputarray):
        """This function will normalize a float vector or matrix
        Math function 100*(x-min)/(max-min)"""
        try:
            minvector = np.amin(inputarray, axis=0)
            maxvector = np.amax(inputarray, axis=0)
            output = 100 * (inputarray - minvector) / (maxvector - minvector)
            output = np.round(output, 0)
        except:
            print("error: check if all identic or input format is numpy array!")
            raise
        return output

    @staticmethod
    def datanormlization(data):
        """this function will normalize different timeseries data"""
        df = data.select_dtypes(include=[np.number])
        npdf = df.to_numpy()
        npdf = searchindexdata.normlization(npdf)
        df.iloc[:,:] = npdf
        return df