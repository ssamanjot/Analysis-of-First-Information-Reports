# FIRProject
## Pdf To Image
Firstly, we were given the pdfs of Punjab Police FIR which are converted to images using PDF2Image library of python. Then using the OS library we iterated through the folders and subfolders and searched for the file that ends with "pdf" and stored in the list. Then that list is passed through the "convert_from_path" class of the pdf2image library the pdfs are converted to the images. This way the image is then converted to the dataframe. The name of the image is kept with the filename_index (Index is basically from 1 to 4 which are the number of pages.) and then the image is stored at a specific folder (that is the folder name is basically according to months of PDF)

## Data Preprocessing
The dataframe recieved after the image-text extraction is converted to dataframe and then sent for preprocessing

#### Special symbols

In data preprocessing, the data is cleaned using various lambda functions which removed the special symbols from the dataframe

#### Stopwords

Then a list of punjabi stopwords is created and named as "stopwords_pun_updated.txt" and then the stopwords are removed from the dataframe.

#### Tokenization 

Then afterwards the punjabi words are tokenized using "inltk" library. This library is basically for nlp for Indian Languages. Tokenize is the function that is used to tokenize the punjabi text when language_code='pa' is passed.

## Dictionary

#### Reading the dictionary
We were given few pages of bilingual dictionary and we were told that we had to map the dictionary words with the words of dataframe. The basic intuition was that any punjabi word in dataframe would be replaced by the english word of the dictionary. So firstly we read the image of dictionary pages by using the tesseract library of python. In it, the library reads the text from the images and then stored it in csv file. 

#### Cleaning

The text that was obtained by reading dictionary contains too many special symbols. Then the lambda function is defined that basically cleans the text and remove the special symbols and numeric values. Then the words are tokenized on spaces. 
Then we had to build the dataframe that contains the english words in one column and its all 4-5 punjabi meanings in other column. 

## Google Trans
We also tried using the googletrans and then to convert the given punjabi text to english text. The basic idea behid this was that we were not able to find the embeddings of the punjabi language. So we thought of using the googletrans and converting the given punjabi text to english text 
