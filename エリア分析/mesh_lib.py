#  メッシュコード計算

#  meshcode_to_latlong,  メッシュコードから緯度・経度へ
#  latlong_to_meshcode,  緯度・経度からメッシュコードへ。
#  dms_to_deg,           度・分・秒から度（小数点表示）へ。
#  deg_to_dms,           度（小数点表示）から度・分・秒へ。

#  latlong_to_half_meshcode, 　緯度・経度から1/2メッシュコードを作成

import re  # 正規表現によるパターンマッチ

########################################
# メッシュコードを渡し、対応する緯度・経度を返す。
# メッシュコードは数値（整数）でも文字列型でも可。
# 
# 返値は数値データが２つ並んだタプル。
# 
# 特に指定しなければメッシュの中央の座標を返す。
# メッシュコードは一次、ニ次、三次いずれも可。
#
# NW, NE, SW, SE を２つ目の引数として渡すと、それぞれ北西、北東、南西、南東の
# コーナーの座標を返す。
#
# 緯度・経度は度単位の小数。
# 
#  usage 
#  code_a = "55354251" # 三次メッシュコード
#  lat_lon = mesh_lib.meshcode_to_latlong(code_a);  # 中央の緯度・経度
#  print('latitude\t', lat_lon[0], '\tlongitude\t', lat_lon[1], 
#
#  code_a = "55354251" # 三次メッシュコード
#  lat_lon = mesh_lib.meshcode_to_latlong(code_a, 'NE') # 北東端
#  print('latitude\t', lat_lon[0], '\tlongitude\t', lat_lon[1], 

def meshcode_to_latlong(code, loc = 'C'):

    if type(code) != int:  # 整数型に（文字列が渡された場合に対応）
        try:
            code = int(code)
        except:  # 形式チェック
            print("Error in  mesh_lib.meshocode_to_latlong()  Not a valid code handed.")
            raise

    code = str(code) # あらためて文字型に。

    code12 = ''
    code34 = ''
    code5  = ''
    code6  = ''
    code7  = ''
    code8  = ''

    loc = loc.upper()

    if re.match("^C|(NE)|(NW)|(SE)|(SW)$", loc) == None:
        raise Exception ("Invalid option to meshcode_to_latlong()")

    match_1_result = re.match("\d{4}", code)

    if re.match("\d{4}", code):  # 最初の４文字が数字

        code12 = code[0:2]
        code34 = code[2:4]
        lat_width  = 2.0 / 3.0  # grid cell の緯度方向の間隔
        long_width = 1.0        # grid cell の経度方向の間隔

    else:
        return (None)           # メッシュコードとして無効

    if re.match("\d{6}", code):   # 少なくとも最初の６文字は数字

        code5 = code[4:5]
        code6 = code[5:6]
        lat_width  /= 8.0;
        long_width /= 8.0;

    if re.match("\d{8}", code):  # 最初の８文字は数字

        code7 = code[6:7]
        code8 = code[7:8]
        lat_width  /= 10.0;
        long_width /= 10.0;

    # 以下、南西コーナーの座標を求める。

    lat  = float(code12) * 2 / 3          #  一次メッシュ
    long = float(code34) + 100

    if (code5 != '') & (code6 != ''):     # 二次メッシュ or 三次メッシュ
        lat  += (float(code5) * 2 / 3) / 8
        long += float(code6) / 8 

    if (code7 != '') & (code8 != ''):     # 三次メッシュ
        lat  += float(code7) * 2 / 3 / 8 / 10
        long += float(code8) / 8 / 10 

    # ここまでで南東端の緯度・経度が得られた

    # 中央の座標なら、一区画の幅（経度幅）・高さ（緯度幅）の半分を足す。
    if loc == 'C':
        lat  += lat_width  / 2 
        long += long_width / 2

    # 北端の座標なら、一区画の高さ（緯度幅）を足す
    if re.search('N', loc):
        lat += lat_width

    # 東端の座標なら、一区画の幅（経度幅）を足す
    if re.search('E', loc):
        long  += long_width

    return (lat, long)     # タプルを返す。




##################
#  緯度・経度（度単位）を受けとり、これを含むメッシュのコードを返す
#  緯度。経度の型は float でも文字列でも可。
#
#  返値のメッシュコードは数値（整数）データ。
#
#  ３番めの引数として 1,2,3 を渡せば、一次メッシュ、二次メッシュ、
#  三次メッシュコードを計算する。指定がなければ三次メッシュ、
#
# Usage:
#  code3 = meshlib.latlong_to_meshcode(35.3, 138.5)      # 三次メッシュコード
#  code2 = meshlib.latlong_to_meshcode(35.3, 138.5, 2)   # 二次メッシュコード
#  code1 = meshlib.latlong_to_meshcode(35.3, 138.5, 1)   # 一次メッシュコード
#

def latlong_to_meshcode(lat, long, order = 3):

    if type(lat) != float:  # 実数型でないなら変換
        lat = float(lat)

    if type(long) != float: # 実数型でないなら変換
        long = float(long)

    if (order < 1) | (order > 3):
        raise Exception ("Invalid parameter to latlong_to_meshcode()")

    # Latitude 

    lat_in_min = lat * 60.0

    code12 = int(lat_in_min / 40)  # codeの1, 2文字目部分（数値）
    lat_rest_in_min = lat_in_min - code12 * 40   # 残差
    
    code5 = int(lat_rest_in_min / 5 )   #  code 5文字目 二次メッシュの１区画は緯度5分
    lat_rest_in_min -= code5 * 5        #  残差

    code7 = int(lat_rest_in_min / (5/10)) # code 7文字目 三次メッシュの１区画は緯度５分の 1/10

    # Longitude 

    code34 = int(long) - 100  # codeの3, 4文字目部分（数値）

    long_rest_in_deg = long - int(long)

    code6 = int(long_rest_in_deg * 8)
    long_rest_in_deg -= code6 / 8;

    code8 = int(long_rest_in_deg / (1/80) )

    code = code12 * 100 + code34

    if order >= 2:
        code = code * 100 + code5 * 10 + code6

    if order == 3:
        code = code * 100 + code7 * 10 + code8

    return int(code)



##################
#  度、分、秒を受けとり、度の単位で小数点表示に変換して返す。
#
# Usage:
#  deg = meshlib.dms_to_deg(35, 20, 15)

def dms_to_deg (deg, min, sec):

    in_deg = deg + min / 60.0 + sec / 3600.0

    return in_deg


##################
# 度の単位の小数点表示を受けとり、 度、分、秒に変換して返す。
# 戻り値は数値データが３つ並んだタプル。
#
# Usage:
#  dms = meshlib.deg_to_dms(35.3375)

def deg_to_dms(in_deg):

    deg         = int(in_deg)
    rest_in_deg = in_deg - deg

    min         = int( rest_in_deg * 60 )
    rest_in_min = rest_in_deg * 60 - min;

    sec = rest_in_min * 60;

    # もし繰り上がってしまっていたら、その分の調整、

    if sec >= 60:   # 秒が60を越えたら
        sec -= 60
        min += 1 


    if min == 60:    # 分が60 を越えたら
       min -= 60
       deg += 1

    return (deg, min, sec)  # タプルを返す。


def latlong_to_detail_meshcode(lat, log, param=0):
    """
    = (QUOTIENT($A2*60,40) & 
        INT($B2-100) & 
        [p1] QUOTIENT(MOD($A2*60,40),40/8) & 
        [p2] QUOTIENT(MOD(($B2-100),1)*60,60/8) & 
        [p3] QUOTIENT(MOD(MOD($A2*60,40),40/8),40/8/10) & 
        [p4] QUOTIENT(MOD(MOD(($B2-100),1)*60,60/8),60/8/10) & 
        [p5] QUOTIENT(MOD(MOD(MOD($A2*60,40),40/8),40/8/10),40/8/10/2)*2 + 
            QUOTIENT(MOD(MOD(MOD(($B2-100),1)*60,60/8),60/8/10),60/8/10/2)+1)*1
    """
    lat60, mod = divmod(lat * 60, 40)
    lng = log - 100

    p1 = divmod(mod, 40/8 )[0]
    p2 = divmod(divmod(lng,1)[1]*60,(60/8))[0]
    p3 = divmod(divmod(mod, 40/8 )[1], 40/8/10)[0]
    p4 = divmod(divmod(divmod(lng,1)[1]*60,(60/8))[1], (60/8/10))[0]
    p5 = (divmod(divmod(divmod(mod, 40/8)[1], 40/8/10)[1], 40/8/10/2 )[0] * 2 + \
          divmod(divmod(divmod(divmod(lng,1)[1]*60,(60/8))[1], (60/8/10))[1],60/8/10/2)[0]) + 1
    
    print("lat60", int(lat60))
    print("lng", lng)
    print("p1", p1)
    print("p2", p2)
    print("p3", p3)
    print("p4", p4)
    print("p5", p5)
    #print("p5_1", divmod(divmod(divmod(mod, 40/8)[1], 40/8/10)[1], 40/8/10/2 )[0] * 2)
    #print("p5_2", divmod(divmod(divmod(divmod(lng,1)[1]*60,60/8)[1], (60/8/10))[1],60/8/10/2)[0]) + 1)
    result_mesh = []
    if(param == 2 or param == 0):
        result_mesh.append(str(int(lat60))+str(int(lng))+'-'+str(int(p1))+str(int(p2))+str(int(p3))+str(int(p4))+'-'+str(int(p5)))
        if(param == 2 ):
            return result_mesh

    """
        [p6] = QUOTIENT(MOD(MOD(MOD(MOD($A2*60,40),40/8),40/8/10),40/8/10/2),40/8/10/2/2)*2 + 
               QUOTIENT(MOD(MOD(MOD(MOD(($B2-100),1)*60,60/8),60/8/10),60/8/10/2),60/8/10/2/2)+1)*1
    """
    p6 = (divmod(divmod(divmod(divmod(mod, 40/8)[1], 40/8/10)[1], 40/8/10/2 )[1],40/8/10/2/2)[0] * 2 + \
          divmod(divmod(divmod(divmod(divmod(lng,1)[1]*60,60/8)[1], 60/8/10)[1],60/8/10/2)[1],60/8/10/2/2)[0] + 1)
    if(param == 4 or param == 0):
        result_mesh.append(str(int(lat60))+str(int(lng))+'-'+str(int(p1))+str(int(p2))+str(int(p3))+str(int(p4))+'-'+str(int(p5))+'-'+str(int(p6)))
        if(param == 4 ):
            return result_mesh
    """
        [p7] = QUOTIENT(MOD(MOD(MOD(MOD(MOD($A2*60,40),40/8),40/8/10),40/8/10/2),40/8/10/2/2),40/8/10/2/2/2)*2 + 
               QUOTIENT(MOD(MOD(MOD(MOD(MOD(($B2-100),1)*60,60/8),60/8/10),60/8/10/2),60/8/10/2/2),60/8/10/2/2/2)+1)*1    
    """
    p7 = (divmod(divmod(divmod(divmod(divmod(mod, 40/8)[1], 40/8/10)[1], 40/8/10/2 )[1],40/8/10/2/2)[1],40/8/10/2/2/2)[0] * 2 + \
          divmod(divmod(divmod(divmod(divmod(divmod(lng,1)[1]*60,60/8)[1], 60/8/10)[1],60/8/10/2)[1],60/8/10/2/2)[1],60/8/10/2/2/2)[0] + 1)

    result_mesh.append(str(int(lat60))+str(int(lng))+'-'+str(int(p1))+str(int(p2))+str(int(p3))+str(int(p4))+'-'+str(int(p5))+'-'+str(int(p6))+'-'+str(int(p7)))
    return result_mesh
