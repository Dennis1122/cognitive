import numpy as np
import pandas as pd
from collections import defaultdict
import re
class LineReader:
    def __init__(self):
        self.line_dict=defaultdict()
        self.word_dict=defaultdict()
    def find_lines(self,start, end, X1, Y1, X2, Y2, Text, line_dict,xbias=25):
        #print(Text[start:end])
        order = np.argsort(X1[start:end])
        x1_tmp = np.array(X1[start:end])[order]
        x2_tmp = np.array(X2[start:end])[order]
        y1_tmp = np.array(Y1[start:end])[order]
        y2_tmp = np.array(Y2[start:end])[order]
        text = np.array(Text[start:end])[order]
        f_start = 0
        f_end = 0
        if start == end:
            return line_dict
        curr = float(x2_tmp[0])
        for i in range(len(x1_tmp)):
            if float(x1_tmp[i]) <= float(curr) + float(xbias):
                curr = float(x2_tmp[i])
                f_end = i + 1
            else:
                cordinate = (x1_tmp[f_start], y1_tmp[f_start], x2_tmp[f_end - 1], y2_tmp[f_end - 1])
                tmp = u' '.join(str(i) for i in text[f_start:f_end])
                if len(tmp) > 0:
                    line_dict[cordinate] = tmp
                    #print("Temp ==> ", tmp,len(tmp))
                curr = x2_tmp[i]
                f_start = i
                f_end = i+1
        cordinate = (x1_tmp[f_start], y1_tmp[f_start], x2_tmp[f_end - 1], y2_tmp[f_end - 1])

        tmp = u' '.join(str(i) for i in text[f_start:f_end])
        if len(tmp)>0:
            line_dict[cordinate]=tmp
            #print("Temp ==> ", tmp,len(tmp))
        curr = x2_tmp[i]
        """f_start = i
        f_end = i
        cordinate = (x1_tmp[f_start], y1_tmp[f_start], x2_tmp[f_end - 1], y2_tmp[f_end - 1])
        line_dict[cordinate] = u' '.join \
            (str(i) for i in text[f_start:f_end])"""
        return line_dict
    def csv_reader(self,df,type='line',ybias=7,xbias=25):
        print(len(df))
        Text = df.iloc[:, 0]
        Text = [re.sub('[^a-zA-Z0-9-.?!&/":#\';()| ]', '', str(i)) for i in Text]
        Text = [re.sub(' +', ' ', str(i)) for i in Text]
        X1 = list(df.iloc[:, 1])
        X2 = list(df.iloc[:, 3])
        Y1 = list(df.iloc[:, 2])
        Y2 = list(df.iloc[:, 4])
        i=0
        while i < len(Text):
            if len(re.sub('[^a-zA-Z0-9&#]','',Text[i]))<=0:
                Text.pop(i)
                X1.pop(i)
                X2.pop(i)
                Y1.pop(i)
                Y2.pop(i)
            else:
                i+=1
        if type=='word':
            for x1, y1, x2, y2, text in zip(X1, Y1, X2, Y2, Text):
                if len(re.sub('[^a-zA-Z0-9]', '', text)) <= 0:
                    continue
                self.word_dict[(x1, y1, x2, y2)] = text
            return self.word_dict
        order = np.argsort(Y1)
        X1 = np.array(X1)[order]
        Y1 = np.array(Y1)[order]
        X2 = np.array(X2)[order]
        Y2 = np.array(Y2)[order]
        Text = np.array(Text)[order]
        curr = float(Y1[0])
        start = 0
        end = 0
        line_dict = defaultdict(str)
        for i in range(len(X1)):
            if float(Y1[i])<= float(curr) + float(ybias):
                end = i + 1
                curr = float(Y1[i])
            else:
                if(X2[i]>X1[i]):
                    line_dict = self.find_lines(start, end, X1, Y1, X2, Y2, Text, line_dict,xbias)
                    start = i
                    end = i+1
                    curr = Y1[i]
        return line_dict,Text