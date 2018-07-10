#from Fedex import  FedEx
import numpy as np
def group_lines(line_dict,xbias=5,ybias=25):
    locs=list(line_dict.keys())
    values=list(line_dict.values())
    y=[i[1] for i in locs]
    order=np.argsort(y)
    values=np.array(values)[order]
    locs=np.array(locs)[order]
    boxLocs=[]
    boxValues=[]

    while(len(locs)!=0):
        tmp_locs = []
        indices=[]
        start=-1
        txt=[]
        prev=[]
        end=0
        for i in range(len(locs)):
            if start==-1:
                txt.append(values[i])
                tmp_locs.append(locs[i])
                start=i
                indices.append(i)
                prev=locs[i]
            else:
                x_start=float(prev[0])
                y_start=float(prev[3])
                if float(locs[i][0]) > x_start - xbias and float(locs[i][0]) < x_start+xbias and float(locs[i][1]) < y_start+ybias:
                    txt.append(values[i])
                    tmp_locs.append(locs[i])
                    indices.append(i)
                    prev=locs[i]
                else:
                    continue
        """print(tmp_locs[0][0],tmp_locs[0][1],tmp_locs[len(tmp_locs)-1][2],tmp_locs[len(tmp_locs)-1][3])
        print(txt)"""
        boxLocs.append((tmp_locs[0][0],tmp_locs[0][1],tmp_locs[len(tmp_locs)-1][2],tmp_locs[len(tmp_locs)-1][3]))
        boxValues.append(u'\n'.join(txt))
        tmp=[locs[j] for j in range(len(locs)) if j not in indices]
        locs=tmp
        tmp = [values[j] for j in range(len(values)) if j not in indices]
        values=tmp
    return boxLocs,boxValues