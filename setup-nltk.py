import nltk

def main():
    #download all of nltk's dependencie
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
    nltk.download('brown')
    nltk.download('maxent_treebank_pos_tagger')
    nltk.download('wordnet')

if __name__ == "__main__":
    main()
