# coding: utf-8

#复制文件需要
#import shutil

from PIL import Image

#变量定义
TempImage = Image.open(u'生.jpg')
#NewImage = Image.copy(TempImage,u'生copy.jpg')

Imageinfo = []
TempList = []
TargetXY = []                          #当低于(128,128,128)时记录y,x(列,行)
AfterImage = []
TempStrokeInfo = []

(ImageWidth,ImageHeight)=TempImage.size

array = [0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\
         1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\
         0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\
         1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\
         1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,\
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
         1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,1,\
         0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
         0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\
         1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,\
         0,0,1,1,0,0,1,1,1,1,0,1,1,1,0,1,\
         1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,\
         1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,\
         1,1,0,0,1,1,1,1,0,0,0,0,0,0,0,0,\
         1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,0,\
         1,1,0,0,1,1,1,0,1,1,0,0,1,0,0,0]

#函数部分

#垂直细化
def VThin(height,width,image,array):
    h = height
    w = width
    NEXT = 1
    for i in range(h):
        for j in range(w):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i][j-1]+image[i][j]+image[i][j+1] if 0<j<w-1 else 1
                if image[i][j] == 0  and M != 0:                  
                    a = [0]*9
                    for k in range(3):
                        for l in range(3):
                            if -1<(i-1+k)<h and -1<(j-1+l)<w and image[i-1+k][j-1+l]==255:
                                a[k*3+l] = 1
                    sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                    image[i][j] = array[sum]*255
                    if array[sum] == 1:
                        NEXT = 0
    return image

#水平细化    
def HThin(height,width,image,array):
    h = height
    w = width
    NEXT = 1
    for j in range(w):
        for i in range(h):
            if NEXT == 0:
                NEXT = 1
            else:
                M = image[i-1][j]+image[i][j]+image[i+1][j] if 0<i<h-1 else 1   
                if image[i][j] == 0 and M != 0:                  
                    a = [0]*9
                    for k in range(3):
                        for l in range(3):
                            if -1<(i-1+k)<h and -1<(j-1+l)<w and image[i-1+k][j-1+l]==255:
                                a[k*3+l] = 1
                    sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                    image[i][j] = array[sum]*255
                    if array[sum] == 1:
                        NEXT = 0
    return image

#总细化
#参数:height高度,width宽度
#image:含有黑0白255信息的嵌套列表[[x1,y1],[x2,y2]……]
#array:待比较的列表,  参考http://www.cnblogs.com/xianglan/archive/2011/01/01/1923779.html
#num循环次数
#返回:处理后的image,其实不用return image也已经改变了
def Xihua(height,width,image,array,num=10):
    for i in range(num):
        VThin(height,width,image,array)
        HThin(height,width,image,array)
    return image

def Thin(height,width,image,array):
    h = height
    w = width
    for i in range(h):
        for j in range(w):
            if image[i][j] == 0:
                a = [1]*9
                for k in range(3):
                    for l in range(3):
                        if -1<(i-1+k)<h and -1<(j-1+l)<w and image[i-1+k][j-1+l]==0:
                            a[k*3+l] = 0
                sum = a[0]*1+a[1]*2+a[2]*4+a[3]*8+a[5]*16+a[6]*32+a[7]*64+a[8]*128
                image[i][j] = array[sum]*255
    return image  

##########################################获取原始图像数据##########################################
for YLoc in xrange(0,ImageHeight):
    TempList = []
    for XLoc in range(0,ImageWidth):
        (InR,InG,InB) = TempImage.getpixel((XLoc,YLoc))
        if InR < 128 and InG < 128 and InB < 128:              #黑
            TempList.append(0)
        else:                                                  #白
            TempList.append(255)
    AfterImage.append(TempList)

# 调用细化函数
Xihua(ImageHeight,ImageWidth,AfterImage,array)                  

#############################################输出骨架样子###########################################

f = open(u'骨架和笔画.txt','w+')

f.write('\n\n')
f.write('目标字细化,*代表存在像素, 代表不存在像素')

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        #f.write(str(AfterImage[YLoc][XLoc]))
        #f.write(' ')
        if(AfterImage[YLoc][XLoc] == 0):
            f.write('*')
        else:
            f.write(' ')
    f.write('\n')

#获取笔画
#参数:ImageHeight高度,ImageWidth宽度,待处理的骨架图
def get_stroke(ImageHeight,ImageWidth,BoneImage):
    # 局部变量
    global TempStrokeInfo                             #笔画信息,[列一，列二],每格列是一个列表,包含各行八邻域的黑点数量
                                                      #例如[[1,1,1,1],[1,1,1,1]]
    TempStrokeList = None

    for YLoc in xrange(0,ImageHeight):
        TempStrokeList = []
        for XLoc in range(0,ImageWidth):
            #如果不是黑点,进行下一个循环
            if BoneImage[YLoc][XLoc]:
                TempStrokeList.append(0)
                continue
            #是黑点的情况,查八邻域的点
            TempValue = 0
            
            if YLoc == ImageHeight-1:
                if XLoc == ImageWidth-1:
                    if not BoneImage[YLoc-1][XLoc-1]:
                        TempValue += 1
                    if not BoneImage[YLoc-1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc-1]:
                        TempValue += 1
                elif XLoc == 0:
                    if not BoneImage[YLoc+1][XLoc-1]:
                        TempValue += 1
                    if not BoneImage[YLoc+1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc-1]:
                        TempValue += 1
                else:
                    if not BoneImage[YLoc-1][XLoc-1]:
                        TempValue += 1
                    if not BoneImage[YLoc-1][XLoc]:
                        TempValue += 1         
                    if not BoneImage[YLoc+1][XLoc-1]:
                        TempValue += 1
                    if not BoneImage[YLoc+1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc-1]:
                        TempValue += 1
            elif YLoc == 0:
                if XLoc == ImageWidth-1:
                    if not BoneImage[YLoc-1][XLoc+1]:
                        TempValue += 1
                    if not BoneImage[YLoc-1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc+1]:
                        TempValue += 1
                elif XLoc == 0:
                    if not BoneImage[YLoc+1][XLoc+1]:
                        TempValue += 1
                    if not BoneImage[YLoc+1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc+1]:
                        TempValue += 1
                else:
                    if not BoneImage[YLoc-1][XLoc+1]:
                        TempValue += 1
                    if not BoneImage[YLoc-1][XLoc]:
                        TempValue += 1         
                    if not BoneImage[YLoc+1][XLoc+1]:
                        TempValue += 1
                    if not BoneImage[YLoc+1][XLoc]:
                        TempValue += 1
                    if not BoneImage[YLoc][XLoc+1]:
                        TempValue += 1                
            elif XLoc == ImageWidth-1:
                if not BoneImage[YLoc-1][XLoc+1]:
                    TempValue += 1
                if not BoneImage[YLoc-1][XLoc]:
                    TempValue += 1         
                if not BoneImage[YLoc-1][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc+1]:
                    TempValue += 1
            elif XLoc == 0:
                if not BoneImage[YLoc+1][XLoc+1]:
                    TempValue += 1
                if not BoneImage[YLoc+1][XLoc]:
                    TempValue += 1         
                if not BoneImage[YLoc+1][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc+1]:
                    TempValue += 1
            else:
                try:
                    if not BoneImage[YLoc+1][XLoc+1]:
                        TempValue += 1
                except Exception as e:
                    print XLoc,YLoc,ImageHeight,(YLoc == ImageHeight-1)
                    raise Exception('stop')
                if not BoneImage[YLoc+1][XLoc]:
                    TempValue += 1         
                if not BoneImage[YLoc+1][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc-1]:
                    TempValue += 1
                if not BoneImage[YLoc][XLoc+1]:
                    TempValue += 1
                if not BoneImage[YLoc-1][XLoc+1]:
                    TempValue += 1
                if not BoneImage[YLoc-1][XLoc]:
                    TempValue += 1         
                if not BoneImage[YLoc-1][XLoc-1]:
                    TempValue += 1
            TempStrokeList.append(TempValue)
        TempStrokeInfo.append(TempStrokeList)

    #return TempStrokeInfo

#############################################输出周围黑点样子#######################################

get_stroke(ImageHeight,ImageWidth,AfterImage)


f.write('\n\n')
f.write('目标黑点周围黑点可取值0-8,空点0,端点1,交叉点2及以上')

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        if TempStrokeInfo[YLoc][XLoc] == 1:
            f.write('·')
        elif TempStrokeInfo[YLoc][XLoc] == 2:
            f.write('-')
        elif TempStrokeInfo[YLoc][XLoc] == 0:
            f.write(' ')
        else:
            f.write('*')
    f.write('\n')

#############################################获取具体笔画###########################################

# 笔画列表 [((StartY,StartX),(EndY,EndX),(Loc,Loc,LOc))]
# Loc确定法则,移动方向      3 2 1
#                          4   8
#                          5 6 7

DetailStrokeList = []

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        if TempStrokeInfo[YLoc][XLoc] == 1:
            f.write('·')
        elif TempStrokeInfo[YLoc][XLoc] == 2:
            f.write('-')
        elif TempStrokeInfo[YLoc][XLoc] == 0:
            f.write(' ')
        else:
            f.write('*')
    f.write('\n')

f.close()

################################################生成新的图片###########################################

img_array=TempImage.load()

imb = Image.new('RGB', (ImageWidth,ImageHeight))
pimb = imb.load()

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        if AfterImage[YLoc][XLoc] == 255:
            pimb[XLoc,YLoc] = (255,255,255)
        else:
            pimb[XLoc,YLoc] = (0,0,0)

imb.save(u'生笔画图.jpg')