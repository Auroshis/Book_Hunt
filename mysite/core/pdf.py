import PyPDF2
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

class Process():
    def search_preprocess(self, index_list, Filename):
        temp = list(str(Filename).split(' '))
        Filename = '_'.join(temp)
        path = "media\\books\\pdfs\\{}".format(Filename)
        pdfFileObj = open(path, 'rb')
        pre_string = ""
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        for page_num in index_list:
            pageObj = pdfReader.getPage(page_num-1)
            pre_string += pageObj.extractText()
        pdfFileObj.close()

        stop_words = set(stopwords.words('english')) 
        word_tokens = word_tokenize(pre_string) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words] 
        filtered_sentence = [] 
        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 

        search_op = ''.join(filtered_sentence)
        return search_op

#inst = Process()
#print(inst.search_preprocess([1], "Letter of Intent_Auroshis Ray.pdf"))