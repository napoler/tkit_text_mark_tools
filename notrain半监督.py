from albertk import *


# fname='data/train.txt'
# fname='data/train_mini.txt'
 
tt=tkitText.Text()
text_list=[]

i=0
text=''
import pymongo
client = pymongo.MongoClient("localhost", 27017)
DB = client.gpt2Write
print(DB.name)

for it in DB.content_pet.find({}):
    # print(it)
    text=text+it['title']+"。"+it['content']
    i=i+1
    if i==100:
        break
    # its.append(it)   
# exit()
text_list=tt.sentence_segmentation_v1(text)
# print(text_list)



mjson=tkitFile.Json("data/marked.json")
c_list=read_labels()


marked_text,marked_label=bulid_t_data(mjson)
# text_list_no=text_list+tt.sentence_segmentation_v1(text)
pre=auto_train(text_list,marked_text,marked_label,n_neighbors=len(c_list)*2)


klist,read_labels=get_pre_label(text_list,pre)
# pprint.pprint(klist)
print("read_labels",read_labels)
print("pre",pre)
for i,k in enumerate(klist.keys()):
    print("##"*30)
    print(k)
    try:
        print(read_labels[str(k)])
    except:
        pass
    print("##"*30)
    pprint.pprint(klist[k])





# label_spread.predict( X)

# #绘图

# x=presentence_embedding
# # plot
# plt.figure(figsize=(4, 3), dpi=160)
# plt.scatter(x[:, 0], x[:, 1], c=cluster_ids_x, cmap='cool')
# # plt.scatter(y[:, 0], y[:, 1], c=cluster_ids_y, cmap='cool', marker='X')
# plt.scatter(
#     cluster_centers[:, 0], cluster_centers[:, 1],
#     c='white',
#     alpha=0.6,
#     edgecolors='black',
#     linewidths=2
# )
# plt.axis([-1, 1, -1, 1])
# plt.tight_layout()
# plt.show()