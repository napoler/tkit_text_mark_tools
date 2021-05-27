# -*- coding: utf-8 -*- 
"""
这是一个训练标注脚本

"""
from albertk import *
from pprint import  pprint

import pymongo
client = pymongo.MongoClient("localhost", 27017)
# DB = client.gpt2Write
DB = client.kg_scrapy
print(DB.name)
# import tkitText
model,tokenizer=load_albert("model/albert_tiny/")

MarkDB = client.Mark
print(MarkDB.name)

# kg_content
def getItem(task_name):
    # .aggregate([ {'$sample': {'size':2000}}])
    # for i,item in enumerate(DB.content_pet.find({})):
    # for i,item in enumerate(DB.content_pet.aggregate([ {'$sample': {'size':100}}])):
    for i,item in enumerate(DB.kg_content.aggregate([ {'$sample': {'size':100}}])):
        item['task_name']=task_name
        if check(item):
            continue
        yield item
    # for i,resp in enumerate(OldDB.content_pet.aggregate([ {'$sample': {'size':2000}}])):
def getmarkedItem(task_name):
    # .aggregate([ {'$sample': {'size':2000}}])
    for i,item in enumerate(MarkDB.marked.find({'task_name':task_name})):
        # item['task_name']=task_name
        # pprint.pprint(item)
        if check(item):
            pass
        else:
            continue
        yield item
def add(item):
    """添加标记信息
    需要包括
    item["task_name"]="aa"
    item["label"]="aa"

    """
    MarkDB.marked.update_one({'_id':item['_id']},{'$set':item},True)    
def check(item):
    """检查是否存在
    """
    return MarkDB.marked.find_one({'_id':item['_id'],'task_name':item['task_name']})
def bulid_t_data_mg(mjson):
    data=[]
    labels=[]
    for it in mjson:
        if len(it['sentence'])>2:
            data.append(it['sentence'])
            labels.append(int(it['label']))
    return data,labels
def run(task_name):
    """这里运行开始脚本
    
    """
    # print("自动选择")
    # checktype=
    while True:
        
        # for it in mjson:
        #     print(it)
        mdata=getmarkedItem(task_name)
        # print(text_list)
        c_list=read_labels()
        data=[]
        # klist=run_search_sent(keyword,tokenizer,model,3)
        text_list=[]
        

        try:
            marked_text,marked_label=bulid_t_data_mg(mdata)
            # print("marked_text",marked_text)
        except:
            pass
        
        try:
            mjson=tkitFile.Json("data/marked.json")
            marked_text_old,marked_label_old=bulid_t_data(mjson)
            marked_text=marked_text+marked_text_old
            marked_label=marked_label+marked_label_old
            # print("marked_text",marked_text)
        except:
            pass 
        # for it in marked_label:
        #     print(it)
        # print(len(marked_text),len(marked_label))
        # print(marked_text[:2],marked_label[:2])  
        # 
        data=[]
          
        for num,item in enumerate(getItem(task_name)):
            #这里限制多久重新需要你连一次
            # if num>100:
            #     break
            # print(item)
            # text_list=[]
            text=item['title']+"\n"+item['content']
            text_list.append(text)
            data.append(item)
        print("获取数据:",len(text_list))
        # print("text_list",text_list[:2])
        if len(c_list)==0:
            n= input("输入新建标签:")
            c_list[len(c_list)]=n
            save_labels(c_list)
        try:
            #限制最后的500个标记数据作为训练，加快速度
            marked_text=marked_text[-2500:]
            marked_label=marked_label[-2500:]
            pass
        except:
            pass
        try:
            print("预训练")
            pre=auto_train(text_list,marked_text,marked_label,tokenizer,model,n_neighbors=len(c_list))
        except:
            print("预训练失败")
            pre=len(text_list)*[-1]
        # print("pre",pre)
        for i,p in enumerate(pre):
            item=data[i]
            #这里限制处理预测为0的
            # if p==1:
            #     continue
            # print(type(p))
            # print("句子：",new_text_list[i])
            print("##"*20)
            print("\n"*2)
            # print(text_list[i][:300])
            print("标题：",item['title'])
            print("--"*20)
            print("内容：",item['content'][:300])
            print("*"*20)
            try:
                print("预测结果:",p,c_list[str(p)])
            except:
                pass

            print("标签信息:",c_list)
            print("*"*20)
            c = input("输入对应标签(新建输入n):")
            if c=="n":
                    n= input("输入新建标签:")
                    c_list[len(c_list)]=n
                    save_labels(c_list)
                    one={"_id":item["_id"],"task_name":task_name,"label":len(c_list)-1,'sentence':text_list[i],"original":item}
                    # print(one)
                    add(one) 
            else:
                try:
                    # c=int(c)
                    # print(c)
                    if c_list.get(str(c)) :
                        one={"_id":item["_id"],"task_name":task_name,"label":int(c),'sentence':text_list[i],"original":item}
                        # print(one)
                        # mjson.save([one])
                        add(one)

                except:
                    pass
while True:
    task_name="文本质量判断"
    print("###"*20)
    print("\n"*5)
    print("###"*20)
    run(task_name)