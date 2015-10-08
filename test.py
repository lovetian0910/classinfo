#coding=utf-8
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
obj = {'content':"测试内容",'stars':5}
array = []
for i in range(5):
	temp = obj.copy()
	temp['content'] = "测试内容" + str(i)
	temp['stars'] = i;
	array.append(temp.copy())
filecontent = {'name':"jwkuang",'date':20150825,'content':array}
encodedjson = json.dumps(filecontent)
filename = "20150825jwkuang.json"
fileobj = open(filename,"w+")
fileobj.write(encodedjson)

