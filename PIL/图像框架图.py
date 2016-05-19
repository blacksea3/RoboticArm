# coding: utf-8

from PIL import Image
TempImage = Image.open(u'生.jpg')

Imageinfo = []
TempList = []
RawImage = []

(ImageWidth,ImageHeight)=TempImage.size


for YLoc in xrange(0,ImageHeight):
    TempList = []
    for XLoc in range(0,ImageWidth):
        (InR,InG,InB) = TempImage.getpixel((XLoc,YLoc))
        if InR < 128 and InG < 128 and InB < 128:                      #黑
            TempList.append(0)
        else:
            TempList.append(255)                                       #白
    RawImage.append(TempList)

################################################生成框架图#############################################

#获取框架
#参数:ImageHeight高度,ImageWidth宽度,待处理的原始图,直接修改BoneImage
def get_frame(ImageHeight,ImageWidth,BoneImage):
    # 局部变量
    TempFrameList = []                              #局部框架变量列表

    for YLoc in xrange(0,ImageHeight):
        for XLoc in range(0,ImageWidth):
            #如果不是黑点,进行下一个循环
            if BoneImage[YLoc][XLoc]:
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
            if TempValue == 8:
                TempFrameList.append((YLoc,XLoc))
    
    f = open(u'图像框架样式.txt','w+')

    for YLoc in xrange(0,ImageHeight):
        for XLoc in range(0,ImageWidth):
            if (YLoc,XLoc) in TempFrameList:
                BoneImage[YLoc][XLoc] = 255

get_frame(ImageHeight,ImageWidth,RawImage)

################################################生成新的图片###########################################

img_array=TempImage.load()

imb = Image.new('RGB', (ImageWidth,ImageHeight))
pimb = imb.load()

for YLoc in xrange(0,ImageHeight):
    for XLoc in range(0,ImageWidth):
        if RawImage[YLoc][XLoc] == 255:
            pimb[XLoc,YLoc] = (255,255,255)
            #f.write(' ')
        else:
            pimb[XLoc,YLoc] = (0,0,0)
            #f.write('*')
    #f.write('\n')

imb.save(u'生框架图.jpg')