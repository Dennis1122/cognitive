import pyocr
from pyocr import builders
from PIL import Image
import os
import pandas as pd
tools = pyocr.get_available_tools()[0]

def RectdataExtract(imagepath, x1,y1,x2,y2):
    '''This fuction inputs the image path and returns a word_list dataframe with words between coordinates - x1, y1, x2, y2'''
        
    language = "eng"
    image_openend = Image.open(imagepath)
    #image_openend = image_openend.filter(ImageFilter.MinFilter(3))
    word_boxes = tools.image_to_string(image_openend,  lang=language, builder=pyocr.builders.WordBoxBuilder())
    word_lst = []
    for word_box in sorted(word_boxes):
            try:
                output = '"'+str(word_box.content).replace('"',"") +'"'+ '~' +str(word_box.position[0][0])+ '~' +str(word_box.position[0][1])+ '~' +str(word_box.position[1][0])+ '~' +str(word_box.position[1][1])
                print (output)
                if (len(str(word_box.content)) > 0) and (float(word_box.position[0][0]) >= float(x1)) and (float(word_box.position[0][1]) >= float(y1)) and (float(word_box.position[1][0]) <= float(x2)) and (float(word_box.position[1][1]) <= float(y2)):
                    word_box_lst = []
                    word_box_lst.append(str(word_box.content))
                    word_box_lst.append(str(word_box.position[0][0]))
                    word_box_lst.append(str(word_box.position[0][1]))
                    word_box_lst.append(str(word_box.position[1][0]))
                    word_box_lst.append(str(word_box.position[1][1]))
                    word_lst.append(word_box_lst)
                    #print (str(word_box.content))
            except:
                pass
    image_openend.close()
    df_test = pd.DataFrame(word_lst)
    return df_test
