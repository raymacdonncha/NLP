#Downloading packages, and text, cleaning data.
from nltk import *
data = []
lines = open("holbrook.txt").readlines()
array = []
for line in lines:
    array.append(line.strip())  
    
sent = [word_tokenize(words) for words in array]

#Creating a function that splits sentence on '|'
#Creates new lists with typo and corrected words and the index of the split.
def sent_split(sent):  
    typo = []
    correction = []
    index = []
    counter= 0
    
    for word in words:
        if '|' in word:
            split_point = word.split('|')
            correction.append(split_point[1])
            typo.append(split_point[0])
            index.append(counter)
        else:
            typo.append(word)
            correction.append(word)
        counter += 1
        
    sent_dict = {'original': typo
                  ,'corrected': correction
                  ,'indexes': index}
    
    return sent_dict

for words in sent:
    data.append(sent_split(words))
    
 #splitting the test and trainig data into corrected and original lists
test = data[:100]
train = data[100:]

train_corrected = []
train_original = []
test_corrected = []
test_original = []

for word in train:
        train_corrected.append(word['corrected'])
        train_original.append(word['original'])

for word in test:
        test_corrected.append(word['corrected'])
        test_original.append(word['original'])

assert(data[2] == {
    'original': ['I', 'have', 'four', 'in', 'my', 'Family', 'Dad', 'Mum', 'and', 'siter', '.'], 
    'corrected': ['I', 'have', 'four', 'in', 'my', 'Family', 'Dad', 'Mum', 'and', 'sister', '.'], 
    'indexes': [9]
})


#creating a new list of the corrected words from training set
train_corrected_words = []
for word in train_corrected:
    train_corrected_words.append(" ".join(word).lower())
    
train_corrected_words = " ".join(train_corrected_words)    
train_corrected_words = word_tokenize(train_corrected_words)
counter = Counter(train_corrected_words)

#creating the unigram function
def unigram(word):
    count = counter.get(word)
    return count


#creating the probability function
#counting every instance of each word as the numerator with the sum of all word as the denominator
def prob(word):
    count = counter.get(word)
    sum_all_words = sum(counter.values())
    
    #if the word doesn't already exist in our traning set, the  probabilitiy will be 0
    if word not in train_corrected_words:
        return_value = 0
    else:
        return_value =  count / sum_all_words
        
    return return_value

prob('me')

#creating a list of each unique word by coverting the corrected words from traning into a set, then back into a list
unique_words = set(train_corrected_words)
unique_words = list(unique_words)
unique_words

def get_candidates(token):
    
    #create a list for every word and its distinance from whatever the fuction input is
    min_dist_words = []
    for word in unique_words:
        distance = edit_distance(word, token)
        min_dist_words.append(distance)

    #creating a dictionairy with the min distance words 
    distance_dict = dict(zip(unique_words, min_dist_words))
    min_dist = min(distance_dict.values())
    #creating a list for the min dist words 
    min_key_list = []
    distance_dict
    for key in distance_dict.keys():
        if distance_dict[key] == min_dist:
            min_key_list.append(key)
    return min_key_list

def correct(sentence):

    corrected_sent = []
    new_word_list = []
   
    for word in sentence:
        # If the word does not already exist in our set of words, add it to a new word list
        if word.lower() not in unique_words:
            new_word_list.append(word)
            
            #get the candidate for each word and list of probabilities
            candidates = get_candidates(word)
            
            #if there is only one candidate, just use it
            if len(candidates) == 1:
                corrected_sent.append(candidates[0])
            #otherwise just use the word from unique words list   
            else:
                corrected_sent.append(word)
        
        #otherwise just use the word from unique words list
        else:
            corrected_sent.append(word)
        
    return corrected_sent

#creating a list of the predicted sentences from the original test set
test_predicted = []
for sent in test_original:
    test_predicted.append(correct(sent))

def accuracy(test):
    #creating new 'flat' lists to make the divsion easier at the end 
    test_predicted_flat = []
    test_corrected_flat = []
    for sent in test_predicted:
        for item in sent:
            test_predicted_flat.append(item)       
    for sent in test:
        for item in sent:
            test_corrected_flat.append(item)
    
    #coverting them into sets so we get one instacnce of every unique word
    set_predicted = set(test_predicted_flat)
    set_corrected = set(test_corrected_flat)
    
    #matches wil be the list of matching values between the predicted corrections and actual corrections
    matches = set_predicted & set_corrected
    
    #calculation for accuracy % will be the length the matching values / length of actual corrections *100
    result = float(len(matches)) / len(set_corrected) * 100
    #adding % at the end
    return print(round(result,2), '%')

accuracy(test_corrected)