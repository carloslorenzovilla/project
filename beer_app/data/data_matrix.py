import string
import csv
import numpy as np
import hdbscan

class Data_Matrix:
    # min keyword frequency
    FREQ_HIGH = 30
    FREQ_LOW = 10
    # min keyword count
    COUNT = 3
    # column
    COL = 3
    # ignore rows less than
    IGNORE = 0
    # csv filename
    FILE = "beer_app\data\Beer.csv"

    def __init__(self):
        self.items, self.labels = self.csv_import()
        self.keywords = self.keywords()
        self.kw_matrix = self.gen_kw_matrix()
        self.distance_matrix = self.distance_matrix()

    def csv_import(self):

        with open(self.FILE, newline='', encoding="utf8", errors='ignore') as f:
            data = csv.reader(f)
            temp = [
                            row
                            for row
                            in data
                        ]

        # create temp list of items
        temp2 = []
        labels = []
        for row, val in enumerate(temp):
                labels.append(val[self.COL-1])
                temp2.extend(val[self.COL:self.COL+1])
                
        # make single string of items, separated by new line
        items = '\n'.join(temp2)

        # strip punctuations from items list
        items = items.translate(str.maketrans('', '', string.punctuation))

        return items.lower(), labels

    def keywords(self):

        items = list(self.items.split())
        stopwords = ['with', 'noted', 'from', 'style', 'beer',
                    'this', 'brings', 'making', 'that', 'allow',
                    'take', 'your', 'made', 'make', 'very', 'drink',
                    'into', 'gave', 'more', 'much', 'like', 'into', 'some',
                    'brew', 'than', 'after', 'back', 'bill', 'have', 'kept',
                    '2018', 'while', 'give', 'first', 'those', 'business',
                    'thank', "don't", 'most', 'name', 'play', 'think', 'then',
                    'finished', 'brewed', 'brewers', 'notes', 'provided', 'additions',
                    'flavors', 'which', 'several', 'months', 'taste', 'want', 'maximum',
                    'named', 'grown', 'featuring', 'will', 'makes', 'using', 'strain',
                    'addition', 'both', 'enters', 'amount', 'around', 'dont', 'only',
                    'serve', 'still', 'finish', 'lots', 'during', 'late', 'washington',
                    'valley', 'what', 'delivers', 'quench', 'wake', 'logging', 'means',
                    'drinking', 'here', 'weeks', 'about', 'promise', 'just', 'enough',
                    'engine', 'beers', 'were', 'meanest', 'nice', 'whole', 'added',
                    'pouring', 'incredibly', 'coast', 'showcase', 'abundant', 'generous',
                    'took', 'treat', 'kölsch', 'smells',
                    'bodied', 'provide', 'profile', 'another', 'amazing',
                    'appearance', 'really', 'approachable',
                    'carbonation', 'body', 'special', 'extremely', 'something',
                    'thirst', 'enjoy', 'flavor', 'world', 'loose', 'easy', 'tradition',
                    'forward', 'color', 'brewery', 'time', 'nelson', 'lingering', 'technique',
                    'strong', 'hence', 'there', 'three', 'known', 'released', 'anniversary',
                    'house', 'followed', 'hints', 'slightly', 'background', 'palate',
                    'finishes', 'dominate', 'variation', 'undertones', 'head', 'pike', 'well',
                    'displays', 'loaded', 'front', 'lagered', 'cold', 'grains',
                    'follows', 'alcohol', 'additional', 'amounts', 'accentuate',
                    'result', 'small', 'crystal', 'giving', 'best', 'good', 'perhaps',
                    'turned', 'scare', 'wonderful', 'bring', 'tones', 'since', 'famous',
                    'little', 'aroma', 'slight', 'hint', 'choice', 'glass',
                    'better', 'kettle', 'emerging', 'accompanied', 'before', 'their', 'cool',
                    'second', 'true', 'also', 'characteristics', 'lightly', 'taproom',
                    'boss', 'they', 'feel', 'once', 'comes', 'over', 'built', 'great',
                    'truly', 'coindexter’s', 'year', 'older', 'super', 'talisman',
                    'delicately', 'perfectly', 'fires', 'lords', 'secret', 'them', "raven's",
                    'release', 'base', 'delicious', 'freshly', 'gives', 'copious', 'inspired',
                    'sourced', 'varietals', 'bird', 'available', 'trough', 'each', 'annual',
                    'spirit', 'various', 'annually', 'test', 'authentic', 'conditioned',
                    'role', 'ravens', 'totem', 'ancestor', 'raven', 'often', 'addressed',
                    'grandfather', 'sense', 'pomp', 'indeed', 'encourage', 'trickster',
                    'respectably', 'these', 'cars', 'fermentation', 'been',
                    'form', 'sight', 'character', 'aromas','2row', 'simcoe', 'amarillo',
                    'citra','cascade',"it's",'azacca','touch','through','chinook',
                    'magnum']

        items = [
                        item 
                        for item 
                        in items 
                        if len(item) > 3 
                        and item 
                        not in stopwords
                    ]

        words = {}
        for word in items:
            words[word] = words.get(word, 0) + 1

        keywords = [
                                v 
                                for v 
                                in words 
                                if self.FREQ_HIGH > words[v] > self.FREQ_LOW
                            ]

        return keywords

    def gen_kw_matrix(self):

        # create a matrix size items x keywords
        kw_matrix = np.zeros((len(self.keywords)+2))

        for id, line in enumerate(self.items.splitlines()):
            temp_vect = np.zeros(len(self.keywords)+2)
            temp_vect[1] = id + 1
            for word in line.split():
                for idx, key in enumerate(self.keywords):
                    if word == key:
                        temp_vect[idx + 2] = 1
                        break
            # only keep items that have >= COUNT keywords
            if np.sum(temp_vect[2:]) >= self.COUNT:
                kw_matrix = np.vstack((kw_matrix,temp_vect))

        return kw_matrix

    def distance_matrix(self):

        binary_matrix = self.kw_matrix[:,2:]

        string_length = np.size(binary_matrix, axis=1)
        num_vectors = np.size(binary_matrix, axis=0)
        distance_matrix = np.zeros((num_vectors, num_vectors))

        for idx1 in range(num_vectors):
            binary_string_1 = binary_matrix[idx1, :]
            for idx2 in range(idx1+1, num_vectors):
                binary_string_2 = binary_matrix[idx2, :]
                num_mismatches = np.sum(np.logical_xor(
                    binary_string_1, binary_string_2))
                distance_matrix[idx1, idx2] = num_mismatches / string_length
                distance_matrix[idx2, idx1] = distance_matrix[idx1, idx2]

        return distance_matrix