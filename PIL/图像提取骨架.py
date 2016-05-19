# coding: utf-8

from PIL import Image

#变量定义
TempImage = Image.open(u'生.jpg')
Imageinfo = []
TempList = []
TargetXY = []                          #当低于(128,128,128)时记录x,y
AfterImage = []

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

for YLoc in xrange(0,ImageHeight):
    TempList = []
    for XLoc in range(0,ImageWidth):
        (InR,InG,InB) = TempImage.getpixel((XLoc,YLoc))
        if InR < 128 and InG < 128 and InB < 128:              #黑
            TempList.append(0)
        else:                                                  #白
            TempList.append(255)
    AfterImage.append(TempList)

f = open(u'图像提取骨架.txt','w+')

f.write('\n\n')
f.write('目标字细化,*代表存在像素, 代表不存在像素')

Xihua(ImageHeight,ImageWidth,AfterImage,array)                  #调用细化函数

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        #f.write(str(AfterImage[YLoc][XLoc]))
        #f.write(' ')
        if(AfterImage[YLoc][XLoc] == 0):
            f.write('*')
        else:
            f.write(' ')
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

imb.save(u'生框架图.jpg')