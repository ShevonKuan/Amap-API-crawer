import setting
import AmapApi
from AmapApi import area
import pickle
import mysql.connector
import json

# 并行
# from multiprocessing.dummy import Pool as ThreadPool

import requests
cnx = mysql.connector.connect(user=setting.user, password=setting.password,
                              database=setting.database,
                              # auth_plugin='mysql_native_password'
			     )
cursor = cnx.cursor()
add_data = ("INSERT INTO guangzhou "
            "(id, name, type, typecode, biz_type, address, location, tel, pname, cityname, adname) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


# 执行到这个矩形区域 113.657068,22.867568|113.669171,22.858269

# buffer = [area(112.490000,24.140000,113.480000,22.270000)]测试
# try: 
#     f = open('buffer', 'rb')
#     buffer = pickle.load(f)
#     f.close()
# except:
#     f = open('buffer','wb')
#     pickle.dump(buffer, f)
#     f.close()
# f = open('buffer','wb')
for type_code in setting.type_code_list: # 循环poi类型
    print('开始POItype',type_code)
    buffer = setting.buffer
    layer = 0
    while buffer != []:
        layer+=1
        buffer2 = []
        print('------------------------------------------')
        for areai in buffer:
            print(areai,end=',')
        for areai in buffer:
            print('+'*layer, areai)
            data = AmapApi.polygon_search(areai, type_code)
            
            if data == False:
                continue
            if data != None:
                print('\r',end='')
                for i in data:
                    try:
                        cursor.execute(add_data, (
                            str(i['id']),
                            str(i['name']),
                            str(i['type']),
                            str(i['typecode']),
                            str(i['biz_type']),
                            str(i['address']),
                            str(i['location']),
                            str(i['tel']),
                            str(i['pname']),
                            str(i['cityname']),
                            str(i['adname'])
                        ))
                        cnx.commit()
                    except:
                        continue
            else:
                buffer2.extend(AmapApi.onefourth(areai))
        #
        #    print(area)
        buffer = buffer2.copy()
        
