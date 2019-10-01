import os
from pdf2image import convert_from_path
import pandas as pd
from tesserocr import PyTessBaseAPI
from PIL import Image
import sys
from os import path

class Preprocessing:

#PDF2Image is a function to convert PDF to images
    def PDF2Image(rootdir):

        file_paths = []
        file_p = []
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                if file.endswith(".pdf"):
                    file_paths.append(subdir + '/' + file)
                    file_p.append(file)

        for j in range(0, 216):
            for i in file_paths:
                pages = convert_from_path(i)
                image_counter = 1
                for page in pages:
                    filename = file_p[j] + str(image_counter) + ".jpg"
                    page.save(filename, 'JPEG')
                    image_counter = image_counter + 1

        return

#Text2Dataframe function is used to convert Punjabi text data present in First Information content to DataFrame
    def Text2Dataframe(FIRDf,Textdata,FIRCompContent):

        listToStr = ' '.join(map(str, Textdata))


        if listToStr.lower().__contains__('first information contents'):
            Content = listToStr.lower().split('first information contents')[1]
        elif(listToStr.lower().__contains__('12') ):
            Content = listToStr.lower().split('12')[1:]
            if type(Content) == list:
                print (Content,"HAVE TO WORK ON THIS")

        elif ((listToStr.lower().__contains__('13')) and (listToStr.lower().__contains__('Action'))):
            Content = listToStr.lower().split('13')[0]
        FIRCompContent = FIRCompContent + Content



        return FIRDf,FIRCompContent

#Image2Text Function is used to convert Punjabi FIR images extracted from PDF to Punjabi text
    def Image2Text(ImgFiles,ImageFileSplitted,FIRDf):
        ImageFileSplitted=set(ImageFileSplitted)
        with PyTessBaseAPI(path='C:/Users/Aman/Documents/Python Scripts/tesserocr-master/tessdata/.',
                           lang='script/Gurmukhi+eng') as api:
            for img in ImageFileSplitted:

                FIRCompContent = ""
                for iter in range(3,9):
                    ImageNminPNG=img + '_' + str(iter) + '.png'
                    Textdata=[]

                    if(path.exists(ImageNminPNG))==True:
                        column = Image.open(ImageNminPNG)
                        gray = column.convert('L')
                        blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
                        blackwhite.save(ImageNminPNG)
                        api.SetImageFile(ImageNminPNG)
                        Text=api.GetUTF8Text()

                        Textdata.append(Text)
                        FIRDf,FIRCompContent = Preprocessing.Text2Dataframe(FIRDf, Textdata,FIRCompContent)
                    else:
                        break
                FIRDf = FIRDf.append({'First_Information_Contents': FIRCompContent}, ignore_index=True)
        return FIRDf

#FileNamesinList is a function used to store the names of png and jpg files at a specified path
    def FileNamesinList(files):

        ImgFiles = []
        ImageFileSplitted=[]
        arr = os.listdir()
        for i in arr:
            if '.txt' in i:
                files.append(i)

            if '.jpg' in i.lower() or '.png' in i.lower():
                if i.__contains__('_'):
                    ImageFileSplitted.append(i.split('_')[0])
                ImgFiles.append(i)

        return files, ImgFiles, ImageFileSplitted


files = []
rootdir = '/home/nitpreet/Documents/Fir/FIR/FEB-2019/'
FIRDf = pd.DataFrame(columns=['First_Information_Contents'])
files,ImgFiles,ImageFileSplitted=Preprocessing.FileNamesinList(files)
FIRDf=Preprocessing.Image2Text(ImgFiles,ImageFileSplitted,FIRDf)

FIRDf.to_csv(r'FIRDf.csv')
#FIRDf=Preprocessing.Text2Dataframe(FIRDf,Textdata)
df=pd.read_csv('FIRDf.csv')
