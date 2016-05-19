# coding: utf-8

from PIL import Image
TempImage = Image.open(u'生.jpg')

Imageinfo = []
TempList = []
TargetXY = []                          #当低于(128,128,128)时记录x,y
AfterImage = []

(ImageWidth,ImageHeight)=TempImage.size

f = open(u'图像初始样式.txt','w+')
f.write('START。。。\n')
f.write('\n\n')

f.write('行')
for XLoc in xrange(0,ImageWidth):
    f.write(("% 12d" % XLoc))

f.write('\n')

for YLoc in xrange(0,ImageHeight):
    TempList = []
    f.write('第%3d列 ' % YLoc)
    for XLoc in range(0,ImageWidth):
        (InR,InG,InB) = TempImage.getpixel((XLoc,YLoc))
        f.write(("%3d,%3d,%3d " % (InR,InG,InB)))
        if InR < 128 and InG < 128 and InB < 128:                      #黑
            TargetXY.append((XLoc,YLoc))
            TempList.append(0)
        else:
            TempList.append(255)                                       #白
    f.write('\n')
    AfterImage.append(TempList)


f.write('\n\n')
f.write('目标字用*大致取样')

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        if (XLoc,YLoc) in TargetXY:
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

imb.save(u'生原始图.jpg')