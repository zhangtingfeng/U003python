# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:00:29 2017

@author: Administrator
"""

import json
import codecs
import re

def extract_query_json(filename,outdir):
    fr=codecs.open(filename,'r','utf-8')
    fw=codecs.open(outdir+'ttte.txt','w','utf-8')
    #fw=codecs.open(outdir+'query_1.txt','w','utf-8')
   # count=0
    line=fr.readline()
    for line in fr:
        line =line.split('\t')
        if line[0] != 'null':
            if 'query'  in line[0]:
                out = re.sub('\"/\"','\":\"',line[0])
                json_dict=json.loads(out)#原始数据中有："word"/"斗神传新的产生"，不满足json格式，将/替换为:
                print ('%s' %json_dict["query"])
                fw.write(json_dict["query"]+"\r\n")
            else:
                print('not here!')
                continue
        else:
            print('aaaaaaaaaaaaaa')
            continue
          
            
    fr.close()
    fw.close()
    
if __name__=='__main__':
    filename='c:/temp/ttt.txt'
    outdir='c:/temp/'
    extract_query_json(filename,outdir)
    
 