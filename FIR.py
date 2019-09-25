import os
from pdf2image import convert_from_path
import pandas as pd
from tesserocr import PyTessBaseAPI
from PIL import Image
import sys
import os
class Preprocessing:

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

    def Text2Dataframe(FIRDf,Textdata):

        # for file in files:
        #     FIC = []
        #     FirList = []
        #     for line in open(file, 'r', encoding="utf8"):
        #         FIC.append(line)
        listToStr = ' '.join(map(str, Textdata))
        if listToStr.lower().__contains__('first information contents'):
            Content = listToStr.lower().split('first information contents')[1]
            FIRDf = FIRDf.append({'First_Information_Contents': Content}, ignore_index=True)

        return FIRDf

    def Image2Text(ImgFiles,FIRDf):

        with PyTessBaseAPI(path='C:/Users/Aman/Documents/Python Scripts/tesserocr-master/tessdata/.',
                           lang='script/Gurmukhi+eng') as api:
            for img in ImgFiles:
                Textdata=[]

                column = Image.open(img)
                gray = column.convert('L')
                blackwhite = gray.point(lambda x: 0 if x < 200 else 255, '1')
                blackwhite.save(img)
                api.SetImageFile(img)
                Text=api.GetUTF8Text()

                Textdata.append(Text)
                FIRDf = Preprocessing.Text2Dataframe(FIRDf, Textdata)

        return FIRDf

    def FileNamesinList(files):

        ImgFiles = []

        arr = os.listdir()
        for i in arr:
            if '.txt' in i:
                files.append(i)

            if '.jpg' in i.lower() or '.png' in i.lower():
                ImgFiles.append(i)

        return files, ImgFiles


files = []
rootdir = '/home/nitpreet/Documents/Fir/FIR/FEB-2019/'
#Preprocessing.PDF2Image(rootdir)
FIRDf = pd.DataFrame(columns=['First_Information_Contents'])
files,ImgFiles=Preprocessing.FileNamesinList(files)
FIRDf=Preprocessing.Image2Text(ImgFiles,FIRDf)

FIRDf.to_csv(r'FIRDf.csv')
#FIRDf=Preprocessing.Text2Dataframe(FIRDf,Textdata)
df=pd.read_csv('FIRDf.csv')
print('Hello',df)