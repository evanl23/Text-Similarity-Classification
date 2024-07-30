#
# Final Project
#
# Partner email: ryadav14@bu.edu
#

import math

def clean_text(txt):
    """ takes a string of text and splits it into individual words without capitalization and punctuation
    """
    for symbol in """.,?"'!;:""": 
        txt = txt.replace(symbol, '')
    txt = txt.lower()
    word_list = txt.split()
    return word_list 


def sentence_len_helper(txt):
    for symbol in """.?!""":
        txt = txt.replace(symbol, '.')
    sentence_list = txt.split('.') 
    if sentence_list[-1] == '':
        sentence_list = sentence_list[:-1]
    return sentence_list 


def stem(s):
    """ takes a string and reduces the string down to its root word
    """
    if s[-3:] == 'ing': 
        return s[:-3]
    elif s[-2:] == 'ed':
        return s[:-2]
    elif s[-2:] == 'er':
        return s[:-2]
    elif s[-3:] == 'ies':
        return s[:-3]
    elif s[-2:] == 'es':
        return s[:-2]
    elif s[-1] == 's': 
        return s[:-1]
    elif s[-2:] == 'ly':
        return s[:-2]
    elif s[-2:] == "'s":
        return s[:-2]
    else:
        return s


def compare_dictionaries(d1, d2):
    """ takes 2 dictionaries and compares how similar d2 is to d1
    """
    total = 0
    score = 0
    if d1 == {}:
        return -50
    for key in d1:
        total += d1[key]
    for key in d2:
        if key in d1:
            score += (math.log(d1[key]/total) * d2[key])
        else: 
            score += (math.log(0.5/total) * d2[key])
    return score


class TextModel:
    """ a data type for text model 
    """
    
    def __init__(self, model_name):
        """ initializing the text model
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.num_punc = {}
        
    
    def __repr__(self):
        """ Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n' 
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n' 
        s += '  number of punctutation marks: ' + str(len(self.num_punc))
        return s
    
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces
        to all of the dictionaries in this text model.
        """
        
        sentence_list = sentence_len_helper(s)
        for sentence in sentence_list: 
            words = sentence.split()
            if len(words) in self.sentence_lengths:
                self.sentence_lengths[len(words)] += 1
            else: 
                self.sentence_lengths[len(words)]= 1
                
        
        for punc in """,?"'!;:""":
            num_punc = s.count(punc)
            if num_punc != 0:
                self.num_punc[punc] = num_punc
         
        
        word_list = clean_text(s) 
    
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else: 
                self.words[w] = 1
         
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] = 1 
                
            if stem(w) in self.stems:
                self.stems[stem(w)] += 1
            else:
                self.stems[stem(w)] = 1
            
    
    def add_file(self, filename): 
        """ takes a file and adds all of the text in the file to the text model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore') 
        file = f.read()
        self.add_string(file) 
        
        
    def save_model(self):
        """ writes the dictionaries in the TextModel object into separate files
        """
        w = self.words     
        file_name = self.name + '_' + 'words'
        f = open(file_name, 'w') 
        f.write(str(w)) 
        f.close() 
        
        wl = self.word_lengths
        file_name2 = self.name + '_' + 'word_lengths'
        f = open(file_name2, 'w') 
        f.write(str(wl)) 
        f.close()
        
        stems = self.stems
        file_name3 = self.name + '_' + 'stems'
        f = open(file_name3, 'w') 
        f.write(str(stems)) 
        f.close()
        
        sl = self.sentence_lengths
        file_name4 = self.name + '_' + 'sentence_lengths'
        f = open(file_name4, 'w') 
        f.write(str(sl)) 
        f.close()
        
        np = self.num_punc
        file_name5 = self.name + '_' + 'num_punc'
        f = open(file_name5, 'w') 
        f.write(str(np)) 
        f.close()
        
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from their files and assigns them to the attributes of the called TextModel
        """
        file_name = self.name + '_' + 'words'
        f = open(file_name, 'r')
        d_str = f.read()           
        f.close()
        self.words = dict(eval(d_str)) 
        
        file_name2 = self.name + '_' + 'word_lengths'
        f = open(file_name2, 'r')
        d_str = f.read()           
        f.close()
        self.word_lengths = dict(eval(d_str)) 
        
        file_name3 = self.name + '_' + 'stems'
        f = open(file_name3, 'r')
        d_str = f.read()           
        f.close()
        self.stems = dict(eval(d_str)) 
        
        file_name4 = self.name + '_' + 'sentence_lengths'
        f = open(file_name4, 'r')
        d_str = f.read()           
        f.close()
        self.sentence_lengths = dict(eval(d_str)) 
        
        file_name5 = self.name + '_' + 'num_punc'
        f = open(file_name5, 'r')
        d_str = f.read()           
        f.close()
        self.num_punc = dict(eval(d_str)) 
        
        
    def similarity_scores(self, other): 
        """ takes another TextModel object and determines the similarities scores between the self TextModel object and the other object
        """
        score = []
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        num_punc_score = compare_dictionaries(other.num_punc, self.num_punc)
        
        score += [word_score] + [word_lengths_score] + [stems_score] + [sentence_lengths_score] + [num_punc_score]
        
        return score
    
    
    def classify(self, source1, source2):
        """ takes two other TextModel objects and compares the self object to them, and determines to which one the self is more similar to
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        
        #print('scores for ' + str(source1.name) + ': ' + str(scores1))
        #print('scores for ' + str(source2.name) + ': ' + str(scores2))
        
        score_compare1 = 0
        score_compare2 = 0
        
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                score_compare1 += 1
            else:
                score_compare2 += 1
                
        if score_compare1 > score_compare2:
            print(self.name + ' is more likely to have come from ' + source1.name)
        else:
            print(self.name + ' is more likely to have come from ' + source2.name)


def test():
    """ compares a mystery text to two simple TextModel objects """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ compares my wr120 paper, a work by tolkien, the deathly hallows, and the bible against rowling and shakespeare """
    source1 = TextModel('JK Rowling')
    source1.add_file('jkrowling.txt')

    source2 = TextModel('Shakespeare')
    source2.add_file('shakespeare.txt')

    new1 = TextModel('Personal Oped')
    new1.add_file('oped_final.txt')
    new1.classify(source1, source2)

    new2 = TextModel('The Silmarillion')
    new2.add_file('silmarillion.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('The Deathly Hallows')
    new3.add_file('deathly_hallows.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('The Bible')
    new4.add_file('kingjames_bible.txt')
    new4.classify(source1, source2)


def Main():

    print("Welcome to text classification! ")

    while True:
        try:
            BaseSource1Name = input("Enter a text file to compare against (make sure it is a .txt file): ") 
            BaseSource1 = TextModel(BaseSource1Name)
            BaseSource1.add_file(BaseSource1Name)

            BaseSource2Name = input("Enter another text file to compare against (make sure it is a .txt file): ") 
            BaseSource2 = TextModel(BaseSource2Name)
            BaseSource2.add_file(BaseSource2Name)
            break
        except FileNotFoundError:
            print("Error! Your file was not found.")

    print("\nNow time to compare!")
    while True:
        try:
            CompareSource = input("Enter a text file you would like to be compared (make sure it is a .txt file) or enter QUIT to quit: ") 
            if CompareSource == "QUIT":
                print("Goodbye!")
                break
            CSource = TextModel(CompareSource)
            CSource.add_file(CompareSource)

            CSource.classify(BaseSource1, BaseSource2)
            print()
        except FileNotFoundError:
            print("Error! Your file was not found.\n")

Main()