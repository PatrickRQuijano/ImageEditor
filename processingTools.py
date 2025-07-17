from PIL import Image, ImageOps
from PIL import ImageDraw
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from math import floor
from math import ceil
from math import radians
from math import sin, cos
from math import sqrt
from matplotlib import pyplot as plt
import ast
import json

class processingTools:

    def __init__(self):
        # instance variables
        self.fileName = None
        self.current_img = None
        self.original_img = None
        self.currentRotation = 0
        self.unrotatedImg = None
        self.wasRotated = None
        self.greyScaleVersion = None
        self.scaledPreviousW = 0
        self.scaledPreviousH = 0
        self.curW = 0
        self.curH = 0
        self.isUploaded = False

    # flips the image horizontaly 
    # loops through the pixels and reverses the pixel values 
    # taking and setting each pixel with the opposite side pixels
    # upon the horzontal
    # works with greyscale and RGB
    def flipImageHorizontal(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return
        
        print("flipping Image Horizontal")
        img = self.original_img
        img_pixls = img.load()
        width, height = img.size
        x = width - 1
        temp1 = None
        loopW = round(width/2)

        for i in range(loopW):
            for j in range(height):
                temp1 = img_pixls[i,j]
                img_pixls[i,j] = img_pixls[width-i-1,j]
                img_pixls[width-i-1,j] = temp1
        self.original_img = img

    # flips the image vertically 
    # loops through the pixels and reverses the pixel values 
    # taking and setting each pixel with the opposite side pixels
    # upon the vertical
    # works with greyscale and RGB
    def flipImageVertical(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("flipping Image Vertical")
        img = self.original_img
        img_pixls = img.load()
        width, height = img.size
        x = width - 1
        temp1 = None
        loopH = round(height/2)

        for i in range(width):
            for j in range(loopH):
                temp1 = img_pixls[i,j]
                img_pixls[i,j] = img_pixls[i,height-j-1]
                img_pixls[i,height-j-1] = temp1
        self.original_img = img

    # helper function to fix issue with scaling and rotating 
    # works with greyscale and RGB
    def scaleSaveForRotateImage(self, newWidth, newHeight):

        if (self.uploadedCheck() == False or newWidth == "" or newHeight == ""):
            print("No file Uploaded or invalid Input")
            return

        print("scaling for save rotate Image")
        img = self.unrotatedImg
        img_pixls = img.load()
        newWidthS = int(newWidth)
        newHeightS = int(newHeight)
        xRatio = img.width / int(newWidth)
        yRatio = img.height / int(newHeight)
        print(xRatio)
        print(yRatio)
        newDimensions = (int(newWidth), int(newHeight))
        if (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", newDimensions)
            createNewImage = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            print("Greyscale Image given")
            newImage = Image.new("L", newDimensions)
            createNewImage = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(int(newWidth)):
                for y in range(int(newHeight)):
                    newX = floor(x * xRatio)
                    newY = floor(y * yRatio)
                    createNewImage.point((x,y) , img_pixls[newX,newY])
            self.unrotatedImg = newImage
            self.scaledPreviousW,self.scaledPreviousH = newWidthS, newHeightS

    # scaling an image using nearest neighobour 
    # multipling each pixel by the ratio of the original width and height with
    # the new width and height 
    # this will give us the new pixel value 
    # works with greyscale and RGB
    def scaleImage(self, newWidth, newHeight):

        if (self.uploadedCheck() == False or newWidth == "" or newHeight == ""):
            print("No file Uploaded or invalid Input")
            return

        print("scaling Image")
        print("new width: " + newWidth)
        print("new Height: " + newHeight)
        #img = Image.open(self.fileName)
        img = self.original_img
        img_pixls = img.load()
        newWidthS = int(newWidth)
        newHeightS = int(newHeight)

        xRatio = img.width / int(newWidth)
        yRatio = img.height / int(newHeight)
        print(xRatio)
        print(yRatio)
        newDimensions = (int(newWidth), int(newHeight))
        if (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", newDimensions)
            createNewImage = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            print("Greyscale Image given")
            newImage = Image.new("L", newDimensions)
            createNewImage = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(int(newWidth)):
                for y in range(int(newHeight)):
                    newX = floor(x * xRatio)
                    newY = floor(y * yRatio)
                    createNewImage.point((x,y) , img_pixls[newX,newY])
            self.original_img = newImage
            self.scaledPreviousW,self.scaledPreviousH = newWidthS, newHeightS
            self.scaleSaveForRotateImage(self.scaledPreviousW, self.scaledPreviousH)
        
    # scales an image using bilinear interpolation
    # allows for more accurate scalling 
    # works with greyscale and RGB
    def bilinearScaleImage(self, newWidth, newHeight):

        if (self.uploadedCheck() == False or newWidth == "" or newHeight == ""):
            print("No file Uploaded or invalid Input")
            return

        print("scaling Image - Bilinear Interpolation")
        print("new width: " + newWidth)
        print("new Height: " + newHeight)
        img = Image.open(self.fileName)
        img = self.original_img
        img_pixls = img.load()
        ogImgWidth = img.width
        ogImgHeight = img.height
        newWidthS = int(newWidth)
        newHeightS = int(newHeight)
        if (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", (newWidthS, newHeightS))
            createNewImage = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            print("Greyscale Image given")
            newImage = Image.new("L", (newWidthS, newHeightS))
            createNewImage = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        scaleW = int(ogImgWidth - 1)/int(newWidthS - 1 ) 
        scaleH = int(ogImgHeight - 1)/int(newHeightS - 1)
        print(str(img_pixls[1,1]))

        for i in range (newWidthS):
            for j in range(newHeightS):
                # first put the transfer original image pixals to equivalent spot in new scaled image
                x = i * scaleW
                y = j * scaleH 
                # now get the surounding 4 pixals coordinates in new image
                xLow = floor(x)
                xHigh = min(ogImgWidth - 1, ceil(x))
                if xHigh >= ogImgWidth:
                    xHigh = ogImgWidth - 1
                yLow = floor(y)
                yHigh = min(ogImgHeight - 1, ceil(y))
                if yHigh >= ogImgHeight:
                    yHigh = ogImgHeight - 1
                if (img.mode == "L"):
                    # now get surounding 4 pixals intensity greylevel values
                    v1 = img_pixls[xLow, yLow]
                    v2 = img_pixls[xHigh, yLow]
                    v3 = img_pixls[xLow, yHigh]
                    v4 = img_pixls[xHigh, yHigh]
                    # now get the estimated point from the 4 surrounding points (bilinear interpolation)
                    q1 = (1 - (x-xLow)) * v1 + (x-xLow) * v2
                    q2 = (1 - (x-xLow)) * v3 + (x-xLow) * v4
                    q = (1 - (y-yLow)) * q1 + (y-yLow) * q2
                    #print("This is my newImage: " + str(newImage[i,j]))
                    #print("This is my Q: " + str(q))
                    newImage.putpixel((i,j), int(q))
                elif (img.mode == "RGB"):
                    # now get surounding 4 pixals intensity greylevel values
                    Rv1, Gv1, Bv1  = img_pixls[xLow, yLow][0], img_pixls[xLow, yLow][1], img_pixls[xLow, yLow][2]
                    Rv2, Gv2, Bv2 = img_pixls[xHigh, yLow][0], img_pixls[xHigh, yLow][1], img_pixls[xHigh, yLow][2]
                    Rv3, Gv3, Bv3 = img_pixls[xLow, yHigh][0], img_pixls[xLow, yHigh][1], img_pixls[xLow, yHigh][2]
                    Rv4, Gv4, Bv4 = img_pixls[xHigh, yHigh][0], img_pixls[xHigh, yHigh][1], img_pixls[xHigh, yHigh][2]
                    # now get the estimated point from the 4 surrounding points (bilinear interpolation)
                    Rq1 = (1 - (x-xLow)) * Rv1 + (x-xLow) * Rv2
                    Gq1 = (1 - (x-xLow)) * Gv1 + (x-xLow) * Gv2
                    Bq1 = (1 - (x-xLow)) * Bv1 + (x-xLow) * Bv2

                    Rq2 = (1 - (x-xLow)) * Rv3 + (x-xLow) * Rv4
                    Gq2 = (1 - (x-xLow)) * Gv3 + (x-xLow) * Gv4
                    Bq2 = (1 - (x-xLow)) * Bv3 + (x-xLow) * Bv4

                    Rq = (1 - (y-yLow)) * Rq1 + (y-yLow) * Rq2
                    Gq = (1 - (y-yLow)) * Gq1 + (y-yLow) * Gq2
                    Bq = (1 - (y-yLow)) * Bq1 + (y-yLow) * Bq2
                    newImage.putpixel((i,j), (int(Rq), int(Gq), int(Bq)))
        self.original_img = newImage

    # rotating an image by taking in a degree given by user
    # works with greyscale and RGB
    # first calculate what the new image dimenesions should be by using formula:
    # newWidth = (img.width*abs(cos(newRotateBy)) + img.he ight*abs(sin(newRotateBy)))
    # newHeight = (img.height*abs(cos(newRotateBy)) + img.width*abs(sin(newRotateBy)))
    # then loop through oriningal image width and height and get the values of the pixel
    # of the new image but using the formula giving in class 
    # works with greyscale and RGB
    def rotateImage(self, rotateBy):

        if (self.uploadedCheck() == False or rotateBy == ""):
            print("No file Uploaded or invalid Input")
            return

        print("rotate Image")
        print(int(rotateBy))
        if (self.wasRotated == None):
            print("hello should have gone in here")
            img = self.original_img
            self.unrotatedImg = self.original_img
            self.wasRotated = True
            self.currentRotation = self.currentRotation + int(rotateBy)
        else:
            #first check if any scale has been applied
            if self.scaledPreviousW != 0 & self.scaledPreviousH != 0:
                print("hello here 1")
                self.scaleSaveForRotateImage(self.scaledPreviousW, self.scaledPreviousH)
                img = self.unrotatedImg
                self.currentRotation = self.currentRotation + int(rotateBy)
            else:
                print("hello here 2")
                img = self.unrotatedImg
                self.currentRotation = self.currentRotation + int(rotateBy)
        img_pixls = img.load()
        newRotateBy = radians(self.currentRotation)
        # print(radians(self.currentRotation))
        # print(newRotateBy)
        oGmiddleYLocation = img.height // 2
        oGmiddleXLocation = img.width // 2
        # print("angle: " + str(newRotateBy))
        # print("newWidthNoAbs: " + str(img.width*cos(newRotateBy) + img.height*sin(newRotateBy)))
        # print("newHeightNoAbs: " + str(img.height*cos(newRotateBy) + img.width*sin(newRotateBy)))
        newWidth = (img.width*abs(cos(newRotateBy)) + img.height*abs(sin(newRotateBy)))
        newHeight = (img.height*abs(cos(newRotateBy)) + img.width*abs(sin(newRotateBy)))
        if (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", (int(newWidth) , int(newHeight)))
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            print("Greyscale Image given")
            newImage = Image.new("L", (int(newWidth) , int(newHeight)))
            draw = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            print("newWidth: " + str(newImage.width))
            print("newHeight: " + str(newImage.height))

            middleYLocation = newImage.height // 2
            middleXLocation = newImage.width // 2

            center_h = newImage.height - img.height
            center_w = newImage.width - img.width

            for x in range(img.width):
                for y in range(img.height):
                    newX = x - oGmiddleXLocation 
                    newY = y - oGmiddleYLocation 
                    xp = round( (newX) * cos(newRotateBy) - (newY) * sin(newRotateBy) + middleXLocation)
                    yp = round( (newX) * sin(newRotateBy) + (newY) * cos(newRotateBy) + middleYLocation)
                    if 0 <= xp < newImage.width and 0 <= yp < newImage.height:
                        #newImage.putpixel((xp, yp), img_pixls[x,y])
                        draw.point( (xp,yp), img_pixls[x, y])

        self.original_img = newImage
        self.curW, self.curH = self.original_img.size


    # cropping an image using zero padding 
    # user gives the top left and bottom right coordinate values
    # works with greyscale and RGB
    def cropImage(self, topLeftX, topLeftY, botRightX, botRightY):

        if (self.uploadedCheck() == False or topLeftX == "" or topLeftY == "" or botRightX == "" or botRightY == ""):
            print("No file Uploaded or invalid Input")
            return

        print("crop Image")
        print("topX: " + topLeftX + " topY: " + topLeftY + " botX: " + botRightX + " botY: " + botRightY)
        img = self.original_img
        img_pixls = img.load()
        newTopLX = int(topLeftX)
        newTopLY = int(topLeftY)
        newBotRX = int(botRightX)
        newBotRY = int(botRightY)
        # new area
        if (img.mode == "RGB"):
            newImage = Image.new("RGB", img.size )
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            newImage = Image.new("L", img.size )
            draw = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(newImage.width):
                for y in range(newImage.height):
                    if (x > newTopLX and y > newTopLY and x < newBotRX and y < newBotRY):
                        draw.point( (x,y), img_pixls[x, y])
                    else:
                        draw.point( (x,y), 0)

            self.original_img = newImage

    # crop an image using reflected indexing as the padding 
    # rather than zero padding
    # works with greyscale and RGB
    # to achieve reflected indexing the code loops through the pixels of the image 
    # ∀(x,y)∈Z2 , f R (x,y) = f(h(x mod 2M),k(y mod 2N)), 
    # therefore the pixel at x, h(x)=x if x∈0..M−1 and h(x)=2M−1−x if x∈M..2M−1. 
    # And the pixel at y k(y)=y if y∈0..N−1 and k(y)=2N−1−y if y∈N..2N−1.
    # works with greyscale and RGB
    def cropImageReflectedIndex(self, topLeftX, topLeftY, botRightX, botRightY):

        if (self.uploadedCheck() == False or topLeftX == "" or topLeftY == "" or botRightX == "" or botRightY == ""):
            print("No file Uploaded or invalid Input")
            return

        print("crop Image with reflected indexing")
        print("topX: " + topLeftX + " topY: " + topLeftY + " botX: " + botRightX + " botY: " + botRightY)
        img = self.original_img
        img_pixls = img.load()
        newTopLX = int(topLeftX)
        newTopLY = int(topLeftY)
        newBotRX = int(botRightX)
        newBotRY = int(botRightY)
        # new area
        if (img.mode == "RGB"):
            newImage = Image.new("RGB", img.size )
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            newImage = Image.new("L", img.size )
            draw = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(newImage.width):
                for y in range(newImage.height):
                    if ((newTopLX == 0 and newTopLY == 0) or (newBotRX == newImage.width and newBotRY == newImage.height)):
                        if (x >= 0 and x <= newTopLX - 1):
                            xp = ((newBotRX - newTopLX)) - x - 1
                        elif(x >= newBotRX and x <= newImage.width-1):
                            xp = (2*(newBotRX - newTopLX)) - x - 1
                        else: 
                            xp = x
                        if (y >= 0 and y <= newTopLY - 1):
                            yp = ((newBotRY - newTopLY)) - y - 1
                        elif(y >= newBotRY and y <= newImage.height-1):
                            yp = (2*(newBotRY - newTopLY)) - y - 1
                        else:
                            yp = y
                    else:
                        if (x >= 0 and x <= newTopLX - 1):
                            xp = -((newBotRX - newTopLX)) - x - 1
                        elif(x >= newBotRX and x <= newImage.width-1):
                            xp = ((newBotRX - newTopLX)) - x - 1
                        else: 
                            xp = x
                        if (y >= 0 and y <= newTopLY - 1):
                            yp = -((newBotRY - newTopLY)) - y - 1
                        elif(y >= newBotRY and y <= newImage.height-1):
                            yp = ((newBotRY - newTopLY)) - y - 1
                        else:
                            yp = y
                    draw.point( (x,y), img.getpixel((xp,yp)) )
            self.original_img = newImage


    def cropImageCircularIndex(self, topLeftX, topLeftY, botRightX, botRightY):

        if (self.uploadedCheck() == False or topLeftX == "" or topLeftY == "" or botRightX == "" or botRightY == ""):
            print("No file Uploaded or invalid Input")
            return

        print("crop image using circular indexing")
        print("topX: " + topLeftX + " topY: " + topLeftY + " botX: " + botRightX + " botY: " + botRightY)
        img = self.original_img
        img_pixls = img.load()
        newTopLX = int(topLeftX)
        newTopLY = int(topLeftY)
        newBotRX = int(botRightX)
        newBotRY = int(botRightY)
        # new area
        if (img.mode == "RGB"):
            newImage = Image.new("RGB", img.size )
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            newImage = Image.new("L", img.size )
            draw = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")


        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(newImage.width):
                for y in range(newImage.height):
                    if ((x >= newTopLX and x <= newBotRX- 1) and (y >= newTopLY and y <= newBotRY - 1)):
                        newX = x
                        newY = y
                    else:
                        newX = (x-(newTopLX))%(newBotRX - newTopLX) + newTopLX
                        newY = (y-(newTopLY))%(newBotRY - newTopLY) + newTopLY
                    draw.point( (x,y), img.getpixel((newX,newY)) )
            self.original_img = newImage


    # Shearing an image - horizontal shearing
    # works with greyscale and RGB
    def shearImage(self, offset):

        if (self.uploadedCheck() == False or offset == ""):
            print("No file Uploaded or invalid Input")
            return

        print("shearing Image")
        img = self.original_img

        # get the maxOffset in the x and in the y
        # this will help us get the new dimensions of image 
        # that we need to include the whole shearing affect
        maxX = abs(img.width * int(offset))
        maxY = abs(img.height * 0)
       
        if (img.mode == "RGB"):
            newImage = Image.new("RGB", (img.width + maxX, img.height + maxY) )
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "L"):
            newImage = Image.new("L", (img.width + maxX, img.height + maxY) )
            draw = ImageDraw.Draw(newImage)
        else:
            print("image given neither RGB or Greyscale")

        if (img.mode == "RGB" or img.mode == "L"):
            for x in range(img.width):
                for y in range(img.height):
                    newX = x + int(int(offset) * y)
                    draw.point( (newX,y), img.getpixel((x,y)) )
            self.original_img = newImage



    #-----------------------------MAPPINGS METHODS-----------------------------
    # works with greyscale and RGB
    def linearGreyLevelMapping(self, givenA, givenB):

        if (self.uploadedCheck() == False or givenA == "" or givenB == ""):
            print("No file Uploaded or invalid Input")
            return

        print("linear grey-level mapping")
        print("a-val: " + str(givenA) + " B-val: " + str(givenB) )
        img = self.original_img
        img_pixls = img.load()
        aVal = float(givenA)
        bVal = float(givenB)

        if (img.mode == "RGB"):
            # new area
            newImage = Image.new("RGB", img.size )
            draw = ImageDraw.Draw(newImage)
            for x in range(newImage.width):
                for y in range(newImage.height):
                    r, g, b = img.getpixel((x,y))
                    r = round(aVal * r + bVal)
                    g = round(aVal * g + bVal)
                    b = round(aVal * b + bVal)
                    if( r > 255):
                        r = 255
                    elif (r < 0):
                        r = 0
                    if( g > 255):
                        g = 255
                    elif (g < 0):
                        g = 0
                    if( b > 255):
                        b = 255
                    elif (b < 0):
                        b = 0
                    draw.point((x,y), (r,g,b))
            self.original_img = newImage

        elif (img.mode == "L"):
            # new area
            newImage = Image.new("L", img.size )
            draw = ImageDraw.Draw(newImage)
            for x in range(newImage.width):
                for y in range(newImage.height):
                    val = img.getpixel((x,y))
                    val = round(aVal * val + bVal)
                    draw.point((x,y), val)
                    if( val > 255):
                        val = 255
                    elif (val < 0):
                        val = 0
            self.original_img = newImage


    # works with greyscale and RGB
    def powerLawMapping(self, gamma):

        if (self.uploadedCheck() == False or gamma == ""):
            print("No file Uploaded or invalid Input")
            return

        print("power law grey-level mapping")
        print("Gamma: " + str(gamma) )
        img = self.original_img
        newGamma = float(gamma)
        # new area
        if (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", img.size )
            draw = ImageDraw.Draw(newImage)

            for x in range(newImage.width):
                for y in range(newImage.height):
                    r, g, b = img.getpixel((x,y))
                    r = round(255 * (((r/255))**newGamma))
                    g = round(255 * (((g/255))**newGamma))
                    b = round(255 * (((b/255))**newGamma))
                    draw.point((x,y), (r,g,b))
            #print(str(img.getpixel((2,5))))
            self.original_img = newImage

        elif (img.mode == "L"):
            print("Greylevel image given")
            newImage = Image.new("L", img.size )
            draw = ImageDraw.Draw(newImage)

            for x in range(newImage.width):
                for y in range(newImage.height):
                    val = img.getpixel((x,y))
                    val = round(255 * (((val/255))**newGamma))
                    draw.point((x,y), val)
            #print(str(img.getpixel((2,5))))
            self.original_img = newImage



    #-----------------------------HISTOGRAM METHODS-----------------------------
    # works with greyscale and RGB
    def createHistogram(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("createdHistogram")
        img = self.original_img
        img_pixls = img.load()
        # for greyscale images
        imgData = []
        # for RGB images
        imgDataR = []
        imgDataG = []
        imgDataB = []
        # if the image is RGB and not greyscale
        if (img.mode == "RGB"):
            print("RGB image given converting to greyscale")
            imRGB = img.convert(mode='RGB')
        elif (img.mode == "L"):
            print("Greyscale image given")
            imgray = img
            self.greyScaleVersion = imgray
        else:
            print("Image neither RGB or Greyscale Exit")

        # if image is Greyscale 
        if (img.mode == "L"):
            print("making greyscale image histogram")
            for x in range(img.width):
                for y in range(img.height):
                    # grey level should have same value for R G and B so just take one of them
                    r = imgray.getpixel((x,y))
                    imgData.append(r)
            # Creating dataset
            a = np.array(imgData)
            n_bins = 256
            labels = [0, 50, 100, 150, 200, 250]
            # Creating histogram
            plt.xlim(0, 255)
            plt.title("Greyscale image regular histogram")
            plt.hist(a, n_bins)
            plt.show()
        elif (img.mode == "RGB"):
            print("making RGB image histogram")
            for x in range(img.width):
                for y in range(img.height):
                    # grey level should have same value for R G and B so just take one of them
                    r, g, b = imRGB.getpixel((x,y))
                    imgDataR.append(r)
                    imgDataG.append(g)
                    imgDataB.append(b)
            # creating the data sets
            aR, aG, aB = np.array(imgDataR), np.array(imgDataG), np.array(imgDataB)
            n_bins = 256
            # Creating histogram
            #fig, (axR, axG, axB) = plt.subplots(nrows=3, ncols=3)
            plt.xlim(0, 255)
            plt.hist(aR, n_bins, label="R")
            plt.hist(aG, n_bins, label="G")
            plt.hist(aB, n_bins, label="B")
            plt.title("RGB image regular histogram")
            plt.legend(loc='upper right')
            plt.show()


    def HistEqualization(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("createdHistogram")
        img = self.original_img
        # if its an rgb image
        if (img.mode == "RGB"):
            print("given RGB image converting to greyscale first") 
            imgRGB = img
            img_array = np.asarray(imgRGB)
            histArray = np.bincount(img_array.flatten(), minlength=256)
            totalPixls = np.sum(histArray)
            normHistArray = histArray/totalPixls
            cumNormHistArray = np.cumsum(normHistArray)
            transform_map = np.floor(255 * cumNormHistArray).astype(np.uint8)
            img_list = list(img_array.flatten())
            equalizedList = [transform_map[p] for p in img_list]
            equalizedImgArray = np.reshape(np.asarray(equalizedList), img_array.shape)
            finalImg = Image.fromarray(equalizedImgArray, mode='RGB')
            self.original_img = finalImg
        # if its greyscale image
        elif (img.mode == "L"):
            print("image already greylevel image")
            imgray = img
            #convert to NumPy array
            img_array = np.asarray(imgray)
            # now want to normalize the histogram so its codomain is inbetween [0,1]
            #flatten image array and calculate histogram via binning
            #when flatenning changeing the values from (R,G,B) to just 1 greylevel so R
            histArray = np.bincount(img_array.flatten(), minlength=256)
            # array of the occurances of each u so occurances of each intensity
            # 0 has 490 pixals with value 0
            # 256 has 2458 pixels with value 256 etc..
            #normalize
            #print(str(histogram_array))
            totalPixls = np.sum(histArray)
            #chistogram_array = np.cumsum(histogram_array)
            # after this line the whole array is normalized so each value in between [0,1]
            normHistArray = histArray/totalPixls
            #print(str(histogram_array))
            # num_pixels is N*M which is the total amount of pixals and so the commulative sum should be 
            # N*M with dog img its 99600
            #print(str(num_pixels))
            # we want the normalized communative thats why we got the communitive Histogram of L-1 
            # and also the N*M
            # because we will do H_cn (I) / N*M
            #normalized cumulative histogram
            # so each u i nthe array is the sum of the amount of pixals that are <= u
            cumNormHistArray = np.cumsum(normHistArray)
            #print(str(chistogram_array))
            # m(u) = Hgcn(v) * (L-1) = Hfcn(u) * (L-1)
            transform_map = np.floor(255 * cumNormHistArray).astype(np.uint8)
            print(str(transform_map))

            # flatten image array into 1D list
            img_list = list(img_array.flatten())
            #print(str(img_list))
            # transform pixel values to equalize
            equalizedList = [transform_map[p] for p in img_list]
            #print(str(eq_img_list))
            # reshape and write back into img_array
            equalizedImgArray = np.reshape(np.asarray(equalizedList), img_array.shape)
            #convert NumPy array to pillow Image and write to file
            print(str(equalizedImgArray))
            finalImg = Image.fromarray(equalizedImgArray, mode='L')
            #saveImage = ImageOps.colorize(eq_img, black="black", white="white")
            self.original_img = finalImg
        else:
            print("not grey level image or RGB image Exit")

        




    #-----------------------------CONOVOLUTION METHODS-----------------------------
    # works with greyscale and RGB
    def applyConvolution(self, kernelString):

        if (self.uploadedCheck() == False or kernelString == ""):
            print("No file Uploaded or invalid Input")
            return

        #strs = kernelString.replace('[','').split('],')
        kernelList = json.loads(kernelString)
        #kernel = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])
        #[[-2,-1,0], [-1,1,1], [0,1,2]]
        #[[0.1,0.1,0.1], [0.1,0.1,0.1], [0.1,0.1,0.1]]
        kernel = np.array(kernelList)
        img = self.original_img
        if (img.mode == "L"):
            # RGBImg = ImageOps.colorize(img, black="black", white="white")
            # npImg = np.array(RGBImg)
            npImg = np.array(img)
        elif (img.mode == "RGB"):
            npImg = np.array(img)
        # get height and width of the image
        imgH, imgW = npImg.shape[0], npImg.shape[1]
        # get the new image 
        kernH, kernW = kernel.shape[0], kernel.shape[1]
        # create new image of og image size minus broder because we cant do convolution there without using 
        # like zero padding or ciruclar indexing etc
        #newImg = np.zeros((imgH - kernH+1, imgW - kernW+1, 3))
        if (img.mode == "RGB"):
            print('RGB image convolution')
            newImg = np.zeros((imgH , imgW , 3))
            # loop through the pixels in the image
            # skips outer edges of image 
            newStartH = kernH//2
            newStartW = kernW//2
            for i in range (newStartH, imgH - newStartH-1):
                for j in range(newStartW, imgW - newStartW-1):
                    # extract a window of pixels around the current pixel
                    window = npImg[i-newStartH : i+newStartH+1, j-newStartW : j+newStartW+1]
                    # Apply the convolution to the window and set the result as the value of the current pixel in the new image
                    newImg[i, j, 0] = int((window[:,:,0] * kernel).sum())
                    newImg[i, j, 1] = int((window[:,:,1] * kernel).sum())
                    newImg[i, j, 2] = int((window[:,:,2] * kernel).sum())
            print(str(window))
            # Clip values to the range 0-255
            print(str(newImg))
            new_img = np.clip(newImg, 0, 255)
            print(str(new_img.shape))
            print(str(npImg.shape))
            saveImage = Image.fromarray(new_img.astype(np.uint8))
            self.original_img = saveImage
        elif (img.mode == "L"):
            print('greyscale image convolution')
            newImg = np.zeros((imgH , imgW))
            # loop through the pixels in the image
            # skips outer edges of image 
            newStartH = kernH//2
            newStartW = kernW//2
            for i in range (newStartH, imgH - newStartH-1):
                for j in range(newStartW, imgW - newStartW-1):
                    # extract a window of pixels around the current pixel
                    window = npImg[i-newStartH : i+newStartH+1, j-newStartW : j+newStartW+1]
                    # Apply the convolution to the window and set the result as the value of the current pixel in the new image
                    newImg[i, j] = int((window[:,:] * kernel).sum())
            # Clip values to the range 0-255
            new_img = np.clip(newImg, 0, 255)
            saveImage = Image.fromarray(new_img.astype(np.uint8))
            self.original_img = saveImage



    #-----------------------------FILTERING METHODS-----------------------------
    # works with greyscale and RGB
    def applyMinFilter(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        img = self.original_img
        img_pixls = img.load()
        # now create new temp image that will be copy of original
        # in this image we will apply the min filter
        # and at the end save the new image 
        if (img.mode == "L"):
            print("L image given")
            newImage = Image.new("L", img.size)
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", img.size)
            draw = ImageDraw.Draw(newImage)
        else:
            print('not RGB or Greyscale Image')
        # get the neighbours of the current pixel and order them 
        # once ordered take the min value for the current pixel
        neighboursR = [None] * 9
        neighboursG = [None] * 9
        neighboursB = [None] * 9

        for x in range(1, newImage.width-1):
            for y in range(1, newImage.height-1):
                
                if (img.mode == "L"):
                    neighboursR[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1] = img.getpixel((x - 1,y))
                    neighboursR[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3] = img.getpixel((x ,y - 1))
                    neighboursR[4] = img.getpixel((x,y))
                    neighboursR[5] = img.getpixel((x ,y + 1))
                    neighboursR[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7] = img.getpixel((x + 1,y ))
                    neighboursR[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    result = neighboursR[0] 
                    draw.point((x,y), result)
                else:
                    neighboursR[0], neighboursG[0], neighboursB[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1], neighboursG[1], neighboursB[1] = img.getpixel((x - 1,y))
                    neighboursR[2], neighboursG[2], neighboursB[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3], neighboursG[3], neighboursB[3] = img.getpixel((x ,y - 1))
                    neighboursR[4], neighboursG[4], neighboursB[4] = img.getpixel((x,y))
                    neighboursR[5], neighboursG[5], neighboursB[5] = img.getpixel((x ,y + 1))
                    neighboursR[6], neighboursG[6], neighboursB[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7], neighboursG[7], neighboursB[7] = img.getpixel((x + 1,y ))
                    neighboursR[8], neighboursG[8], neighboursB[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    neighboursG.sort()
                    neighboursB.sort()
                    draw.point((x,y), (neighboursR[0], neighboursG[0], neighboursB[0]))
        #newImage.show()
        if (img.mode == "L"):
            saveImage = ImageOps.colorize(newImage, black="black", white="white")
            self.original_img = saveImage
        else:
            self.original_img = newImage

    # works with greyscale and RGB
    def applyMedianFilter(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("applying median filter")
        img = self.original_img
        img_pixls = img.load()
        # now create new temp image that will be copy of original
        # in this image we will apply the min filter
        # and at the end save the new image 
        if (img.mode == "L"):
            print("L image given")
            newImage = Image.new("L", img.size)
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", img.size)
            draw = ImageDraw.Draw(newImage)
        else:
            print('not RGB or Greyscale Image')
        # get the neighbours of the current pixel and order them 
        # once ordered take the median value for the current pixel
        neighboursR = [None] * 9
        neighboursG = [None] * 9
        neighboursB = [None] * 9

        for x in range(1, newImage.width-1):
            for y in range(1, newImage.height-1):
                
                if (img.mode == "L"):
                    neighboursR[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1] = img.getpixel((x - 1,y))
                    neighboursR[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3] = img.getpixel((x ,y - 1))
                    neighboursR[4] = img.getpixel((x,y))
                    neighboursR[5] = img.getpixel((x ,y + 1))
                    neighboursR[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7] = img.getpixel((x + 1,y ))
                    neighboursR[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    result = neighboursR[4] 
                    draw.point((x,y), result)
                else:
                    neighboursR[0], neighboursG[0], neighboursB[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1], neighboursG[1], neighboursB[1] = img.getpixel((x - 1,y))
                    neighboursR[2], neighboursG[2], neighboursB[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3], neighboursG[3], neighboursB[3] = img.getpixel((x ,y - 1))
                    neighboursR[4], neighboursG[4], neighboursB[4] = img.getpixel((x,y))
                    neighboursR[5], neighboursG[5], neighboursB[5] = img.getpixel((x ,y + 1))
                    neighboursR[6], neighboursG[6], neighboursB[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7], neighboursG[7], neighboursB[7] = img.getpixel((x + 1,y ))
                    neighboursR[8], neighboursG[8], neighboursB[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    neighboursG.sort()
                    neighboursB.sort()
                    draw.point((x,y), (neighboursR[4], neighboursG[4], neighboursB[4]))
        #newImage.show()
        if (img.mode == "L"):
            saveImage = ImageOps.colorize(newImage, black="black", white="white")
            self.original_img = saveImage
            if( self.unrotatedImg != None):
                print("hello check121")
                self.unrotatedImg = saveImage
                #self.unrotatedImg.show()
        else:
            self.original_img = newImage


    # works with greyscale and RGB
    def applyMaxFilter(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("apply max filter")
        img = self.original_img
        img_pixls = img.load()
        # now create new temp image that will be copy of original
        # in this image we will apply the min filter
        # and at the end save the new image 
        if (img.mode == "L"):
            print("L image given")
            newImage = Image.new("L", img.size)
            draw = ImageDraw.Draw(newImage)
        elif (img.mode == "RGB"):
            print("RGB image given")
            newImage = Image.new("RGB", img.size)
            draw = ImageDraw.Draw(newImage)
        else:
            print('not RGB or Greyscale Image')
        # get the neighbours of the current pixel and order them 
        # once ordered take the max value for the current pixel
        neighboursR = [None] * 9
        neighboursG = [None] * 9
        neighboursB = [None] * 9

        for x in range(1, newImage.width-1):
            for y in range(1, newImage.height-1):
                
                if (img.mode == "L"):
                    neighboursR[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1] = img.getpixel((x - 1,y))
                    neighboursR[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3] = img.getpixel((x ,y - 1))
                    neighboursR[4] = img.getpixel((x,y))
                    neighboursR[5] = img.getpixel((x ,y + 1))
                    neighboursR[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7] = img.getpixel((x + 1,y ))
                    neighboursR[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    result = neighboursR[8] 
                    draw.point((x,y), result)
                else:
                    neighboursR[0], neighboursG[0], neighboursB[0] = img.getpixel((x - 1,y - 1))
                    neighboursR[1], neighboursG[1], neighboursB[1] = img.getpixel((x - 1,y))
                    neighboursR[2], neighboursG[2], neighboursB[2] = img.getpixel((x - 1,y + 1))
                    neighboursR[3], neighboursG[3], neighboursB[3] = img.getpixel((x ,y - 1))
                    neighboursR[4], neighboursG[4], neighboursB[4] = img.getpixel((x,y))
                    neighboursR[5], neighboursG[5], neighboursB[5] = img.getpixel((x ,y + 1))
                    neighboursR[6], neighboursG[6], neighboursB[6] = img.getpixel((x + 1,y - 1))
                    neighboursR[7], neighboursG[7], neighboursB[7] = img.getpixel((x + 1,y ))
                    neighboursR[8], neighboursG[8], neighboursB[8] = img.getpixel((x + 1,y + 1))
                    neighboursR.sort()
                    neighboursG.sort()
                    neighboursB.sort()
                    draw.point((x,y), (neighboursR[8], neighboursG[8], neighboursB[8]))
        #newImage.show()
        if (img.mode == "L"):
            saveImage = ImageOps.colorize(newImage, black="black", white="white")
            self.original_img = saveImage
        else:
            self.original_img = newImage




    #-----------------------------EXTRA WHATEVER YOU LIKE-----------------------------
    def applyEdgeDetection(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        print("Edge Detection")
        img = self.original_img
        if (img.mode == "L"):
            print("L image given")
            imgray = np.array(img)
        elif (img.mode == "RGB"):
            print("RGB image given")
            img = img.convert(mode='L')
            imgray = np.array(img)
        else:
            print('not RGB or Greyscale Image')

        #x kernel for x edges y kernel for y edges
        xGradientFilter = np.array([[1, 2, 1],[0, 0, 0],[-1, -2, -1]])
        yGradientFilter =  np.array([[1, 0, -1],[2, 0, -2],[1, 0, -1]])
        threshold = 80  #128
        setIntensity = None
        kernelWidth = xGradientFilter.shape[0]//2
        #img_array = np.asarray(imgray)
        if (img.mode == "L" or img.mode == "RGB"):
            newEdgeImage = np.zeros(imgray.shape)
            for i in range(kernelWidth, imgray.shape[0] - kernelWidth):
                for j in range(kernelWidth, imgray.shape[1] - kernelWidth):
                    # gets windows/ surounding pixels
                    x = imgray[i - kernelWidth: i + kernelWidth + 1, j - kernelWidth: j + kernelWidth + 1]
                    # multiply the kernel and the surounding nerhbourhood
                    # sum up the values and get the x magnitude
                    sum_x = (x * yGradientFilter).sum()
                    # gets windows/ surounding pixels
                    y = imgray[i - kernelWidth: i + kernelWidth + 1, j - kernelWidth: j + kernelWidth + 1]
                    # multiply the kernel and the surounding nerhbourhood
                    # gets windows/ surounding pixels
                    sum_y = (y * xGradientFilter).sum()
                    # i - kernelWidth so that the x coordinate starts at 0 then 1,2,3 etc same reason for 
                    # j - kernelWidth
                    gradientMagnitude = sqrt(sum_x**2 + sum_y**2)
                    if (gradientMagnitude >= threshold):
                        setIntensity = 255
                    else:
                        setIntensity = 0
                    newEdgeImage[i - kernelWidth][j - kernelWidth] = setIntensity
            saveImage = Image.fromarray(newEdgeImage.astype(np.uint8))
            self.original_img = saveImage
        

    #-----------------------------HELPER FUNCTIONS(NOT ALGOS)-----------------------------

    def show_current(self):

        if (self.uploadedCheck() == False):
            print("No file Uploaded")
            return

        self.original_img.show()

    def uploadedCheck(self):
        if(self.isUploaded == True):
            return True
        else:
            return False
        
    def setInfo(self, fileName, img_pixls, img):
        self.fileName = fileName
        self.current_img = img_pixls
        self.original_img = img
        self.unrotatedImg = img
        self.curW, self.curH = img.size

        #set is uplaoded to true so we know that a file is uploaded
        if (self.fileName == None):
            return
        else:
            self.isUploaded = True

    

    

