def find_pos_tags(txt):
    from collections import defaultdict
    import re
    from nltk import pos_tag,ne_chunk,word_tokenize
    tag_count=defaultdict(int)
    tags_list=['NN','IN','DT','CC','JJ','VB','TO','RB','PR','OT']
    for key in tags_list:
        tag_count[key]=0.0 
    txt=u''.join(txt).encode('utf-8').strip()
    regex = re.compile('[^a-zA-Z0-9 ]')
    data = regex.sub(' ', txt)
    data = data.replace("\xc2\xa0"," ")
    data=data.replace("cid 9","")
    data = data.replace("\n\n\n"," ")
    data = re.sub(' +',' ',data)
    data = re.sub("[0-9]+","num",data)
    txt=data
    tags=pos_tag(word_tokenize(txt))
    if len(tags)==0:
        tags=pos_tag('BLANKLINE')
    tree = ne_chunk(tags)
    #print txt,tags,len(txt)
    #print tree
    traverse_tree(tree,tag_count)
    pos_tag_perc=[]
    #print txt
    for tag,count in tag_count.items():
        perc=round(float(count)/len(tags),2)
        #print tag,count,perc
        pos_tag_perc.append(perc)
    #print "Sum :",sum(pos_tag_perc),len(tags)
    
    return pos_tag_perc

def traverse_tree(tree,tag_count):
    tags_list=['NN','IN','DT','CC','JJ','VB','TO','RB','PR','OT']
    for branch in tree:
        
        if type(branch) is tuple:
            #try:
                txt = u':'.join(word for word in branch)
                tag = txt.split(':')[1].strip()
                flag=False
                for t in tags_list:
                    if tag.find(t)==0:
                        tag_count[t]+=1
                        flag=True
                #print tag,flag
                if not flag:
                    tag_count['OT']+=1
            #except Exception:
                #print "Exception", branch,type(branch),len(branch)
           
        else:
             traverse_tree(branch,tag_count)

