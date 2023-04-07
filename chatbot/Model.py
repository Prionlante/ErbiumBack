import random, json, pickle, os, nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.models import load_model
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
russian_stopwords = stopwords.words("russian")

class NLPneural():
    """
    Neural net for chat bot system
    """
    def __init__(self, model_name="modelNLP"):
        self.model_name = model_name
        self.words = pickle.load(open(f'{self.model_name}_words.pkl', 'rb'))
        self.classes = pickle.load(open(f'{self.model_name}_classes.pkl', 'rb'))
        self.model = load_model(f'{self.model_name}.h5')
        self.load_from_json('text.json')
        self.lemmatizer = WordNetLemmatizer()

    # load dataset
    def load_from_json(self, intents):
        self.intents = json.loads(open(intents, encoding='utf-8').read())

    def bag_of_words(self, sentence, words):
        """
        This function create list (np format)
        that contain all words
        """
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]

        bag = [0] * len(words)
        for s in sentence_words:
            for i, word in enumerate(words):
                if word == s:
                    bag[i] = 1

        return np.array(bag)

    def predict_class(self, sentence):
        """
        This function return enumerate list
        from model predict result
        """
        p = self.bag_of_words(sentence, self.words)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.1
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})

        return return_list

    def get_response(self, ints, intents_json):
        """
        Get model predict tag and chose
        random response under predictuble tag
        """
        try:
            tag = ints[0]['intent']
            list_of_intents = intents_json['context']
            for i in list_of_intents:
                if i['tag']  == tag:
                    result = random.choice(i['responses'])
                    break
        except IndexError:
            result = "Я не пониаю!"
        return result, ints[0]['intent']

    def request(self, message):
        ints = self.predict_class(message)
        return self.get_response(ints, self.intents)

class NLPrecom(NLPneural):
    """
    Neural net for the rocommendetion system 
    """
    def __init__(self, model_name="modelNLP"):
        NLPneural.__init__(self, model_name)
        self.taglist = []
        with open('Tags.txt', encoding='cp1251') as file:
            self.taglist += file.readlines()

    def predict_tag(self, sentence):
        p = self.bag_of_words(sentence, self.words)
        resai = self.model.predict(np.array([p]))[0]
        resault = []
        tagstr = self.taglist[np.argmax(resai)][:-1]
        resault += tagstr.split(' ')
        return resault
