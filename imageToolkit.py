from PIL import Image
from PIL import ImageDraw
from PIL import ImageTk
import numpy as np
import tkinter as tk
from tkinter import filedialog 
from tkinter import Frame
from tkinter import Label, Toplevel
import os
from processingTools import processingTools

# image to be transformed
global imageToolkit 
imageToolkit = processingTools()
global currentWidth
global currentHeight
currentWidth = 0
currentHeight = 0
global labelCurrentImg

# helper functions
def upload_image():
      print("Image Uploaded")
      filepath = None
      filepath = filedialog.askopenfilename(filetypes= ( ("image files", "*.jpg"), ("all files", "*.*") ))
      if (filepath == "" or filepath == ()):
            print("No image given :(")
            return
      fileName = filepath
      img = Image.open(fileName)
      img_pixls = img.load()
      imageToolkit.setInfo(fileName, img_pixls, img)
      #img.show()
      currentTkImage = ImageTk.PhotoImage(img)
      labelCurrentImg.configure(image = currentTkImage)
      labelCurrentImg.image = currentTkImage
      currentWidth, currentHeight = img.size
      displayImageDimensions(currentWidth, currentHeight)


def getNewDim():
      newWidth = widthE.get(1.0, "end-1c")
      newHeight = heightE.get(1.0, "end-1c")
      imageToolkit.scaleImage(newWidth, newHeight)
      displayImageDimensions(newWidth, newHeight)

def getNewDimBilinear():
      newWidth = widthE.get(1.0, "end-1c")
      newHeight = heightE.get(1.0, "end-1c")
      imageToolkit.bilinearScaleImage(newWidth, newHeight)
      displayImageDimensions(newWidth, newHeight)

def getAngle():
      angleOfRotation = rotationE.get(1.0, "end-1c")
      imageToolkit.rotateImage(angleOfRotation)
      displayImageDimensions(imageToolkit.curW, imageToolkit.curH)

def getNewCoordinates():
      topLeftXGiven = topLeftXc.get(1.0, "end-1c")
      topLeftYGiven = topLeftYc.get(1.0, "end-1c")
      botRightXGiven = botRightXc.get(1.0, "end-1c")
      botRightYGiven = botRightYc.get(1.0, "end-1c")
      if (topLeftXGiven == "" or topLeftYGiven == "" or botRightXGiven == "" or botRightYGiven == ""):
            print("invalid input given")
            return False
      imageToolkit.cropImage(topLeftXGiven, topLeftYGiven, botRightXGiven, botRightYGiven)
      displayImageDimensions(int(botRightXGiven) - int(topLeftXGiven), int(botRightYGiven) - int(topLeftYGiven))

def getNewCoordinatesReflected():
      topLeftXGiven = topLeftXc.get(1.0, "end-1c")
      topLeftYGiven = topLeftYc.get(1.0, "end-1c")
      botRightXGiven = botRightXc.get(1.0, "end-1c")
      botRightYGiven = botRightYc.get(1.0, "end-1c")
      if (topLeftXGiven == "" or topLeftYGiven == "" or botRightXGiven == "" or botRightYGiven == ""):
            print("invalid input given")
            return False
      imageToolkit.cropImageReflectedIndex(topLeftXGiven, topLeftYGiven, botRightXGiven, botRightYGiven)
      displayImageDimensions(int(botRightXGiven) - int(topLeftXGiven), int(botRightYGiven) - int(topLeftYGiven))

def getNewCoordinatesCircular():
      topLeftXGiven = topLeftXc.get(1.0, "end-1c")
      topLeftYGiven = topLeftYc.get(1.0, "end-1c")
      botRightXGiven = botRightXc.get(1.0, "end-1c")
      botRightYGiven = botRightYc.get(1.0, "end-1c")
      if (topLeftXGiven == "" or topLeftYGiven == "" or botRightXGiven == "" or botRightYGiven == ""):
            print("invalid input given")
            return False
      imageToolkit.cropImageCircularIndex(topLeftXGiven, topLeftYGiven, botRightXGiven, botRightYGiven)
      displayImageDimensions(int(botRightXGiven) - int(topLeftXGiven), int(botRightYGiven) - int(topLeftYGiven))

def ChangeContrastOrBrightness():
      a = linearMA.get(1.0, "end-1c")
      b = linearMB.get(1.0, "end-1c")
      imageToolkit.linearGreyLevelMapping(a, b)

def powerMapping():
      y = powerMA.get(1.0, "end-1c")
      imageToolkit.powerLawMapping(y)

def shearing():
      offset = shearHA.get(1.0, "end-1c")
      imageToolkit.shearImage(offset)

def displayImageDimensions(currentWidth, currentHeight):
      var.set(str(currentWidth) + " x " + str(currentHeight)) 

def updatingCurrentImg():
      if(imageToolkit.original_img == None):
            print("No image uploaded to update")
            return 
      currentTkImage = ImageTk.PhotoImage(imageToolkit.original_img)
      labelCurrentImg.configure(image = currentTkImage)
      labelCurrentImg.image = currentTkImage

def getHistogram():
      imageToolkit.createHistogram()

def getEHistogram():
      open_popup()
      imageToolkit.HistEqualization()

def applyConv():
      kernelString = kernelSave.get(1.0, "end-1c")
      imageToolkit.applyConvolution(kernelString)

def applyMin():
      imageToolkit.applyMinFilter()

def applyMedian():
      imageToolkit.applyMedianFilter()

def applyMax():
      imageToolkit.applyMaxFilter()

def doEdgeDetection():
      imageToolkit.applyEdgeDetection()

def viewImage():
      if(imageToolkit.original_img == None):
            print("No image uploaded to update")
            return 
      imageToolkit.show_current()

def open_popup():
   top= Toplevel(root)
   top.geometry("800x200")
   top.title("NOTICE")
   Label(top, text= "NOTE: if Image is not greyscale, it will be converted to greyscale :)", font=('Arial 14 bold')).place(x=100,y=100)

#---------------------------------------------------------------
root = tk.Tk()
var = tk.StringVar()

# window settings 820x600
#root['bg']='#856ff8'
root.geometry("900x950")
root.title("Image Processing Toolkit")

# set up button frame so that I can easily sort my buttons on the GUI
buttonFrame = tk.Frame(root)
buttonFrame.columnconfigure(0)
buttonFrame.columnconfigure(1)
buttonFrame.columnconfigure(2)
buttonFrame.columnconfigure(3)
buttonFrame.columnconfigure(4)


# buttons and interacable components of windows
# 1. drop down for choosing how to flip image
uploadButton = tk.Button(buttonFrame, text="Upload Image", font=('Ariel', 12), command = upload_image)
uploadButton.grid(row=0, column=1)


# input fields for flipping
button2 = tk.Button(buttonFrame, text="Vertical Flip", font=('Ariel', 9), command = imageToolkit.flipImageVertical)
button2.grid(row=1, column=1)

button3 = tk.Button(buttonFrame, text="Horizontal Flip", font=('Ariel', 9), command = imageToolkit.flipImageHorizontal)
button3.grid(row=2, column=1)

#Edge detection
EDButton = tk.Button(buttonFrame, text="EdgeDetection", font=('Ariel', 9), command = doEdgeDetection)
EDButton.grid(row=0, column=3)

# input fields for scaling
widthL = tk.Label(buttonFrame, text="Input Width:", font=('Ariel', 10))
widthL.grid(row=4, column=1)
widthE = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
widthE.grid(row=4, column=2)

heightL = tk.Label(buttonFrame, text="Input Height:", font=('Ariel', 10))
heightL.grid(row=5, column=1)
heightE = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
heightE.grid(row=5, column=2)
scaleB = tk.Button(buttonFrame, text="Scale", font=('Ariel', 9), command = getNewDim)
scaleB.grid(row=4, column=3)
scaleBb = tk.Button(buttonFrame, text="BilinearInterScale", font=('Ariel', 9), command = getNewDimBilinear)
scaleBb.grid(row=5, column=3)

# input fields for rotating
rotationL = tk.Label(buttonFrame, text="Input angle in Degrees:", font=('Ariel', 10))
rotationL.grid(row=7, column=1)
rotationE = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
rotationE.grid(row=7, column=2)
rotationS = tk.Button(buttonFrame, text="Rotate", font=('Ariel', 9), command = getAngle)
rotationS.grid(row=7, column=3)

# input fields for croping 
topLeftX = tk.Label(buttonFrame, text="TopLeft X:", font=('Ariel', 10))
topLeftX .grid(row=9, column=0)
topLeftXc = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
topLeftXc.grid(row=9, column=1)
topLeftY = tk.Label(buttonFrame, text="TopLeft Y:", font=('Ariel', 10))
topLeftY .grid(row=9, column=2)
topLeftYc = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
topLeftYc.grid(row=9, column=3)

botRightX = tk.Label(buttonFrame, text="BotRight X:", font=('Ariel', 10))
botRightX .grid(row=10, column=0)
botRightXc = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
botRightXc.grid(row=10, column=1)
botRightY = tk.Label(buttonFrame, text="BotRight Y:", font=('Ariel', 10))
botRightY .grid(row=10, column=2)
botRightYc = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
botRightYc.grid(row=10, column=3)

cropB = tk.Button(buttonFrame, text="Crop", font=('Ariel', 8), command = getNewCoordinates)
cropB.grid(row=9, column=4)
cropC = tk.Button(buttonFrame, text="CropReflectedIndex", font=('Ariel', 8), command = getNewCoordinatesReflected)
cropC.grid(row=10, column=4)
cropR = tk.Button(buttonFrame, text="CropCircularIndex", font=('Ariel', 8), command = getNewCoordinatesCircular)
cropR.grid(row=8, column=4)


# labels and buttons for linear mapping 
linearMLabel = tk.Label(buttonFrame, text="a(contrast):", font=('Ariel', 9))
linearMLabel .grid(row=12, column=0)
linearMA = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
linearMA.grid(row=12, column=1)
linearMBLabel = tk.Label(buttonFrame, text="b(brightness):", font=('Ariel', 9))
linearMBLabel .grid(row=12, column=2)
linearMB = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
linearMB.grid(row=12, column=3)

linearMappingT = tk.Button(buttonFrame, text="Apply Contrast/Brightness", font=('Ariel', 9), command = ChangeContrastOrBrightness)
linearMappingT.grid(row=12, column=4)

# power law mapping stuff
powerMLabel = tk.Label(buttonFrame, text="Input Gamma(Y):", font=('Ariel', 9))
powerMLabel .grid(row=14, column=1)
powerMA = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 20)
powerMA.grid(row=14, column=2)
powerMappingT = tk.Button(buttonFrame, text="PowerMapping", font=('Ariel', 9), command = powerMapping)
powerMappingT.grid(row=14, column=3)

# shearing image buttons
shearHLabel = tk.Label(buttonFrame, text="Shear Offset:", font=('Ariel', 9))
shearHLabel .grid(row=15, column=1)
shearHA = tk.Text(buttonFrame, font=("Arial Black", 10), height = 1, width = 10)
shearHA.grid(row=15, column=2)
shearHT = tk.Button(buttonFrame, text="Apply Horizontal Shear", font=('Ariel', 9), command = shearing)
shearHT.grid(row=15, column=3)

# create histogram
histButton = tk.Button(buttonFrame, text="show Histogram", font=('Ariel', 9), command = getHistogram)
histButton.grid(row=1, column=3)

# create histogram
histEButton = tk.Button(buttonFrame, text="Equalize Histogram", font=('Ariel', 9), command = getEHistogram)
histEButton.grid(row=2, column=3)

# apply convolution 
convolutionButton = tk.Button(buttonFrame, text="apply convolution", font=('Ariel', 11), command = applyConv)
convolutionButton.grid(row=15, column=0)
kernelSave = tk.Text(buttonFrame, font=("Arial Black", 10), height = 2, width = 20)
kernelSave.grid(row=16, column=0)

# apply non linear filtering 
minFilterButton = tk.Button(buttonFrame, text="min filter", font=('Ariel', 11), command = applyMin)
minFilterButton.grid(row=0, column=2)
medianFilterButton = tk.Button(buttonFrame, text="median filter", font=('Ariel', 11), command = applyMedian)
medianFilterButton.grid(row=1, column=2)
maxFilterButton = tk.Button(buttonFrame, text="max filter", font=('Ariel', 11), command = applyMax)
maxFilterButton .grid(row=2, column=2)


# label for image dimensions 
dimensionsLabel = tk.Label(buttonFrame, textvariable=var , font=('Ariel', 10))
dimensionsLabel.grid(row=18, column=1)
buttonU = tk.Button(buttonFrame, text="Update Img", font=('Ariel', 10), command = updatingCurrentImg)
buttonU.grid(row=15, column=4)
buttonV = tk.Button(buttonFrame, text="View Img in New Window", font=('Ariel', 10), command = viewImage)
buttonV.grid(row=16, column=4)



buttonFrame.pack(anchor ='center')


labelCurrentImg = tk.Label(root)
labelCurrentImg.pack()
root.mainloop()





