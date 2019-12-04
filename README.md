# **Semantics using NLP for handwritten Punjabi FIR Reports**


## *Overview*

>**Natural Language Processing** is a subfield of Machine learning that is concerned with linguistics, computers and Artificial intelligence. 
NLP provides a great significance to the interaction of Human languages with Computers.

>**Semantics using NLP for handwritten Punjabi FIR reports** is NLP project which takes into account the  Punjabi language text for operations.

>Project has been aimed to extract semantics from Punjabi handwritten FIR reports and provide Punjab police with the domain of FIR. 
>A subdivision of Project also includes extracting Named entity recognition from Punjabi text and Using to  fill various columns of FIR reports.

>As it is a live project for Punjab police,a extension to this involves creation of Chatbot that would ask Punjab police to provide further information of what is not provided in the FIR.


## *Implementation*
>FIR reports were provided in the form of PDF of generally 5 images. The general format of FIR report contained Information content of the FIR written in the paragraph form starting from third page.
![Fir no- 14, dated 03-2-2019-MGA pdf3](https://user-images.githubusercontent.com/12868865/67265190-c4923c80-f4ca-11e9-98f2-402495a18fbd.jpg)


>First task was to extract images from FIR PDF and save them with naming convention to easily identify images of any FIR PDF.
>FIR report images contained handwritten texts. There are various Image to Text libraries for English language but the task here was to convert the Image to Text for Punjabi language . OCR tessract was used to convert Punjabi FIR images to Text .
>Further, we converted the Text to dataframe and used it to perform further operation on Punjabi Text
>cnltk library was used to remove stop words from the text and perform tokenization . 
>inltk library was used to create word embeddings and further TF IDF was applied to Punjabi words . Dot product was applied on TF IDF and word embeddings to get Doc2vec vector .



