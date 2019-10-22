import os
from pdf2image import convert_from_path
import pandas as pd
from tesserocr import PyTessBaseAPI
from PIL import Image
import sys
from os import path
from cltk.stop.punjabi.stops import STOPS_LIST
import re
from inltk.inltk import get_embedding_vectors
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Preprocessing:

#PDF2Image is a function to convert PDF to images
    def PDF2Image(self,rootdir):

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
        FIRContentPresent=0

        if listToStr.lower().__contains__('first information contents'):
            FIRContentPresent = 1
            Content = listToStr.lower().split('first information contents')[1]
        elif(listToStr.lower().__contains__('12') ):
            FIRContentPresent = 1
            Content = listToStr.lower().split('12',1)[1]
            if type(Content) == list:
                Content=str(Content)
                print (Content,"HAVE TO WORK ON THIS")

        elif ((listToStr.lower().__contains__('13')) and (listToStr.lower().__contains__('Action'))):
            FIRContentPresent = 1
            Content = listToStr.lower().split('13')[0]
        if(FIRContentPresent==1):
            FIRCompContent = FIRCompContent + Content



        return FIRDf,FIRCompContent

#Image2Text Function is used to convert Punjabi FIR images extracted from PDF to Punjabi text
    def Image2Text(ImgFiles,ImageFileSplitted,FIRDf):
        ImageFileSplitted=set(ImageFileSplitted)
        with PyTessBaseAPI(path='C:/Users/Aman/Documents/Python Scripts/tesserocr-master/tessdata/.',
                           lang='script/Gurmukhi+eng') as api:
            for img in ImageFileSplitted:

                FIRCompContent = ""

                if img.lower().__contains__(', dated'):
                    ImagesDtLoc = img.split(', dated')[1]
                elif img.lower().__contains__(',dated'):
                    ImagesDtLoc = img.split(',dated')[1]
                else:
                    ImagesDtLoc = img.split(',')[1]

                if ImagesDtLoc.lower().__contains__('-19 '):
                    ImageLocation=ImagesDtLoc.split('-19 ',1)[1]
                elif ImagesDtLoc.lower().__contains__('19-'):
                    ImageLocation = ImagesDtLoc.split('19-', 1)[1]
                elif ImagesDtLoc.lower().__contains__('-2019 '):
                    ImageLocation = ImagesDtLoc.split('-2019 ', 1)[1]

                ImageDt=ImagesDtLoc.split(ImageLocation,1)[0]

                for iter in range(3,9):
                    ImageNminPNG=img + '_' + str(iter) + '.jpg'
                    Textdata=[]

                    if(path.exists(ImageNminPNG))==True:
                        print(ImageNminPNG)
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
                FIRDf = FIRDf.append({'First_Information_Contents': FIRCompContent,'Date_and_Location': ImagesDtLoc,'FIR_Location': ImageLocation,'FIR_Date':ImageDt,'PDF_Name': img}, ignore_index=True)
                #FIRDf = FIRDf.append({'Date_and_Location': ImagesDtLoc}, ignore_index=True)
                #FIRDf = FIRDf.append({}, ignore_index=True)

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

    def removeStopWords(dataFrame):
        for index,document in enumerate(dataFrame):
            print(index)
            document=str(document).split(' ')
            DocWithoutStopwrds = [word for word in document if not word in STOPS_LIST]

            dataFrame[index]=DocWithoutStopwrds
        return dataFrame

    def WordEmbeddings(self,VocabWords):

        VectList=[]
        VectList1=[]
        VectList2=[]


        #dataFrame=pd.DataFrame(dataFrame)

        # for List in dataFrame.index:
        #     Word=(dataFrame['First_Information_Contents'][List])
        #     Word=Word.replace("'","")
        #     Words=[(i) for i in Word.split(",")]
        #     for j in Words:
        #         WordList.append(j)
        #
        # WordList=list(set(WordList))
        # Word_String=' '.join(word for word in WordList)
        # print(Word_String)

        iter=0

        print('Hello')
        for eachword in VocabWords:
            iter = iter + 1
            print(iter)
            print(eachword)
            Vect = get_embedding_vectors(str(eachword), 'pa')

            VectList1.append(Vect)

        print(len(VectList1))
        return VectList1



#files = []
os.chdir(r'C:\Users\Aman\PycharmProjects\Sabudh\MachineLearning\ProjectWork\data\Feb')
#rootdir = '/home/nitpreet/Documents/Fir/FIR/FEB-2019/'
#FIRDf = pd.DataFrame(columns=['First_Information_Contents','Date_and_Location','FIR_Location','FIR_Date','PDF_Name'])
#files,ImgFiles,ImageFileSplitted=Preprocessing.FileNamesinList(files)

#FIRDf=Preprocessing.Image2Text(ImgFiles,ImageFileSplitted,FIRDf)
#FIRDf.to_csv(r'FIRDf.csv')

#Df=pd.read_csv('FIRDf.csv')
#Df['First_Information_Contents']=Preprocessing.removeStopWords(Df['First_Information_Contents'])
#Df.to_csv(r'FIRDf_WithoutStopwords.csv')
#FIRDf_WithoutStopwords = pd.read_csv('FIRDf_WithoutStopwords.csv')

# tf = TfidfVectorizer()
# Content = tf.fit_transform(FIRDf_WithoutStopwords['First_Information_Contents']).toarray()
# VocabWords=list(tf.vocabulary_.keys())
# print(VocabWords)
# np.save('VocabWords.npy', VocabWords)
VocabWords = np.load('VocabWords.npy')


EmbeddingList=Preprocessing().WordEmbeddings(VocabWords)