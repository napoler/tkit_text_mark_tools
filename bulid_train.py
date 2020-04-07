import tkitFile


"""
将标记好的数据分割保存为训练数据集

"""



tkitFile.File().mkdir("data/train")
mjson=tkitFile.Json("data/marked.json")
tjson=tkitFile.Json("data/train/train.json")
djson=tkitFile.Json("data/train/dev.json")
data=[]
for item in mjson.auto_load():
    print(item)
    data.append(item)
c=len(data)*0.8
tjson.save(data[:int(c)])
djson.save(data[int(c):])
