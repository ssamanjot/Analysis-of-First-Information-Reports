# FIRProject
## Pdf To Image
Firstly, we were given the pdfs of Punjab Police FIR which are converted to images using PDF2Image library of python. Then using the OS library we iterated through the folders and subfolders and searched for the file that ends with "pdf" and stored in the list. Then that list is passed through the "convert_from_path" class of the pdf2image library the pdfs are converted to the images. This way the image is then converted to the dataframe. The name of the image is kept with the filename_index (Index is basically from 1 to 4 which are the number of pages.)

## Data Preprocessing
The dataframe recieved after the image-text extraction is converted to dataframe and then sent for preprocessing

#### Special symbols

In data preprocessing, the data is cleaned using various lambda functions which removed the special symbols from the dataframe

#### Stopwords

Then a list of punjabi stopwords is created and named as "stopwords_pun_updated.txt" and then the stopwords are removed from the dataframe.

#### Tokenization 

Then afterwards the punjabi words are tokenized using "inltk" library. This library is basically for nlp for Indian Languages. Tokenize is the function that is used to tokenize the punjabi text when language_code='pa' is passed.

