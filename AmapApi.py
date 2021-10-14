import requests as re
import setting
import random
import datetime,time

def waitToTomorrow():
    """等待至第二日"""
    tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), 
        hour=0, minute=0, second=0)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds+60)
class area:
    def __init__(self, Lng1, Lat1, Lng2, Lat2):
        # 通过矩形区域新建一个区域
        '''
        Lng1:矩形区域左上角经度
        Lat1:矩形区域左上角纬度
        Lng2:矩形区域右下角经度
        Lat2:矩形区域右下角纬度
        '''
        self.Lng1 = Lng1
        self.Lat1 = Lat1
        self.Lng2 = Lng2
        self.Lat2 = Lat2
        self.polygon = '%.6f' % Lng1 + ',' + '%.6f' % Lat1 + '|' + '%.6f' % Lng2 + ',' + '%.6f' % Lat2
        self.status = 0 # 记录该区域状态，0为未获取或失败，1为已获取
        self.pois = 0
    def __str__(self):
        return '矩形区域 ' + self.polygon
    def get_polygon(self):
        return self.polygon
    
def polygon_search(areai: area, types):
    # 请求函数
    url = "https://restapi.amap.com/v3/place/polygon"
    param = {}
    param['key'] = random.choice(setting.key)
    param['polygon'] = areai.get_polygon()
    param['types'] = types # POI类型代码
    param['page'] = 1
    res = re.get(url=url, params=param).json()
    if int(res['count']) >= 700: # 高德api不会返回1000个只会返回700来个数据所以大于700即可认为无效
        return None
    elif int(res['count']) == 0:
        return False
    else:
        try:
            b = []
            b.extend(res['pois'])
            while True:
                print('\r page', param['page'],end='',flush=True)
                param['page'] += 1
                res = re.get(url=url, params=param).json()
                if res['pois'] == []:
                    break
                b.extend(res['pois'])
            return b
        except:
            print(res)
            print('key超额,将于明日0点重新启动...')
            if res['infocode'] == '10003':
                waitToTomorrow()
            else:
                param['page'] += 1
            while True:
                print('\r page', param['page'],end='',flush=True)
                res = re.get(url=url, params=param).json()
                param['page'] += 1
                if res['pois'] == []:
                    break
                b.extend(res['pois'])
            return b
def onefourth(areai: area):
    # 一个区域分4份返回4个区域
    a1 = area(areai.Lng1, areai.Lat1, (areai.Lng1 + areai.Lng2) / 2, (areai.Lat1 + areai.Lat2) / 2)
    a2 = area((areai.Lng1 + areai.Lng2) / 2, areai.Lat1, areai.Lng2, (areai.Lat1 + areai.Lat2) / 2)
    a3 = area(areai.Lng1, (areai.Lat1 + areai.Lat2) / 2, (areai.Lng1 + areai.Lng2) / 2, areai.Lat2)
    a4 = area((areai.Lng1 + areai.Lng2) / 2, (areai.Lat1 + areai.Lat2) / 2, areai.Lng2, areai.Lat2)
    return a1, a2, a3, a4
