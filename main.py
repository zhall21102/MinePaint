import cv2
import numpy
import os
import dicMake

defaultDict = dicMake.main("Planks")

def shrink(img, size):
    if img.shape[0] >= img.shape[1] and img.shape[0] > size:
        shrunk = cv2.resize(img, (0, 0), fx = size/img.shape[0]/size, fy = size/img.shape[0])
    elif img.shape[1] > img.shape[0] and img.shape[1] > size:
        shrunk = cv2.resize(img, (0, 0), fx = size/img.shape[1], fy = size/img.shape[1])
    else:
        shrunk = img
    return shrunk

def getDict():
    colorDict = {}
    for file in os.listdir(os.getdir()+'\\textures'):
        myimg = cv2.imread('textures\\'+file)
        avg_color_per_row = numpy.average(myimg, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
        colorDict[file[:-4]] = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
    return colorDict

def compareColors(RGB, dic):
    lis = list(dic.items())
    x = (min(lis, key=lambda x:(abs(x[1][0]-RGB[0])+abs(x[1][1]-RGB[1])+abs(x[1][2]-RGB[2]))/3))
    return x[0]


def getImage(img, dic = defaultDict):
    endList = []
    for e in range(img.shape[0]):
        endList.append([])
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            endList[y].append(compareColors(list(img[y][x]), dic))
    return endList

def deconstruct(inImg, dic = defaultDict):
    out = inImg[:]
    for y in range(len(out)):
        for x in range(len(out[y])):
            out[y][x] = dic[out[y][x]]
    array = numpy.asarray(out).astype(numpy.uint8)
    cv2.imwrite('test.png', array)
    return array

def colorAverage(img):
    myimg = cv2.imread(img)
    avg_color_per_row = numpy.average(myimg, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    out = (int(avg_color[2]), int(avg_color[1]), int(avg_color[0]))
    return out


img = cv2.imread('france.png')
shrunk = shrink(img, 128)
blockArray = getImage(shrunk)
print('Array complete')
copied = [list(row) for row in blockArray]
for y in range(len(blockArray)):
    for x in range(len(blockArray[y])):
        copied[y][x] = blockArray[y][x]
print('Array copied')
end = deconstruct(copied)
print('Image recreated')
