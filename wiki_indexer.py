from __future__ import print_function
import xml.etree.ElementTree as etree
import codecs
import csv,sys
import time
import os
import re
# from nltk.thon import RegexpStemmer
# from nltk.stem.porter import PorterStemmer
from collections import *
from Stemmer import Stemmer as PyStemmer
d=PyStemmer('porter')
# st = RegexpStemmer('ing$|s$|e$|able$', min=4)
# ps = PorterStemmer()
ENCODING = "utf-8"
reload(sys)
sys.setdefaultencoding('utf-8')
def strip_tag_name(t):
    t = elem.tag
    idx = k = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t

sd =defaultdict(int)

with open('stops_words.txt','r') as file:
    word = file.read().split('\n')
    for i in word:
        i = d.stemWord(i)
        sd[i] = 1
dti = defaultdict(int)
dte = defaultdict(int)
ind = defaultdict(list)
temp_array = []
pg_cnt = 0
ARG=sys.argv
for event, elem in etree.iterparse(ARG[1], events=('start', 'end')):

    tname = strip_tag_name(elem.tag)

    # times += 1
    if tname == 'page' and event == 'end':
        pg_cnt+=1

        for i in temp_array:
            if dti[i]==0:
                st = "p" + str(pg_cnt) + "d" + str(dte[i])

            elif dte[i]==0:
                st = "p" + str(pg_cnt) + "t" + str(dti[i])
            else:
                st = "p" + str(pg_cnt) + "t" + str(dti[i]) + "d" + str(dte[i])
            ind[i].append(st)
        dti = defaultdict(int)
        dte = defaultdict(int)
        temp_array = []



    if tname == 'title' and event == 'end':
        # try:
        for i in re.split("[^A-Za-z]+", str(elem.text)):
            i = d.stemWord(i).lower()
            if i not in sd:
                if i:
                    dti[i]+= 1
                    if dti[i]==1 and dte[i]==0:
                        temp_array.append(i)

    elif tname == 'text' and event == 'end':
        for i in re.split("[^A-Za-z]", str(elem.text)):
            i = d.stemWord(i).lower()

            if i not in sd:
                if i:
                    dte[i]+= 1
                    if dte[i]==1 and dti[i]==0:
                        temp_array.append(i)
    elem.clear()


FL=open(ARG[2],'w')
out = sorted(ind)
for i in out:
    # print i,ind[i]
    my=""
    # for j in ind[i]:
    #     my = my + "|" + str(j)
    # print i,my
    my = '|'.join(ind[i])
    s=i+':'+my
    print(s,file=FL)
    # cnt+=1
    # if cnt>100:break
