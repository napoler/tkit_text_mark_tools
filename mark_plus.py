 

from albertk import *
from pprint import  pprint
# import tkitText
model,tokenizer=load_albert("model/albert_tiny/")

def run():

    # tt=tkitText.Text()
    text_list=[]

    # text=''
    keyword = input("输入关键词:")

    mjson=tkitFile.Json("data/marked.json")
    # print(text_list)
    c_list=read_labels()
    data=[]
    # klist=run_search_sent(keyword,tokenizer,model,3)
    text_list=[]
    try:
        marked_text,marked_label=bulid_t_data(mjson)
        # print(marked_text[:2],marked_label[:2])
    except:
        pass
    # for it in marked_text:
    #     print(len(it))
    # print(len(marked_text),len(marked_label))
    for item in search_content(keyword):
        text=item.title+"\n"+item.content
        text_list.append(text)
    print("获取数据:",len(text_list))
    if len(c_list)==0:
        n= input("输入新建标签:")
        c_list[len(c_list)]=n
        save_labels(c_list)
    try:
        
        pre=auto_train(text_list,marked_text,marked_label,tokenizer,model,n_neighbors=len(c_list))
    except:
        pre=len(text_list)*[-1]
    print("text_list",text_list[:2])
    for i,p in enumerate(pre):
        # print(type(p))
        # print("句子：",new_text_list[i])
        print("##"*20)
        print("\n"*5)
        print(text_list[i][:300])
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
                one={"label":len(c_list)-1,'sentence':text_list[i]}
                print(one)
                mjson.save([one]) 
        else:
            try:
                # c=int(c)
                # print(c)
                if c_list.get(str(c)):
                    one={"label":int(c),'sentence':text_list[i]}
                    print(one)
                    mjson.save([one])

            except:
                pass
while True:

    print("###"*20)
    print("\n"*5)
    print("###"*20)
    run()