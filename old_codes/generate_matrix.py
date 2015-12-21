import os
import re
import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import stopwords

data_dir= "/home/neha/Desktop/Independent Study/data/webkb"
stopwords_file ="/home/neha/Desktop/Independent Study/codes/additional-stopwords.txt"

all_documents=[]
all_classes= []
all_files=[]
tags = re.compile(r'<.*?>')
special_characters = re.compile(r'[^A-Za-z0-9 ]+')
classes = ["course","department","faculty","other","project","staff","student"]

def tokenize_document(doc):
    return doc.split()

def remove_tags(text):
    return tags.sub('',text)

def trim_document(doc):
    # Applies only for html documents. If we need text documents in training framework then other method needs to be applied.
    rdoc = '<'.join(doc.split("<")[1:])
    return "<" + rdoc

def remove_special(doc):
    return special_characters.sub(' ',doc)

def process_document(f,cl):
    global vocab_index
    print f
    fp = open(f,"r")
    doc = fp.read().lower()
    #print doc
    number_newlines = doc.count('\n')
    new_doc = trim_document(doc)
    new_doc = remove_tags(new_doc)
    #new_doc = remove_special(new_doc)
    #tokens = tokenize_document(new_doc)
    #tokens = stopwords_obj.remove_stopwords(tokens)
    all_documents.append(new_doc)
    all_classes.append(cl)
    all_files.append(f)

def output_document_matrix(filename):
    #print all_documents
    #print all_classes
    #print all_files
    return
    print ""
    print len(vocab)
    print vocab_index
    print vocab.keys()
    fout = open(filename,"w")
    writer = csv.writer(fout)
    for file,doc in all_documents.items():
        row = []
        row.append(file)
        row.append(doc["class"])
        original_counts = [0]*vocab_index
        for t in doc["tokens"]:
            position = vocab[t]
            original_counts[position] = original_counts[position] +1
        row = row + original_counts
        writer.writerow(row)
    fout.close()

def train_model():
    count_vectorizer = CountVectorizer(decode_error ="ignore",stop_words="english")
    counts = count_vectorizer.fit_transform(all_documents)
    classifier = MultinomialNB(alpha=1)
    classifier.fit(counts,all_classes)
    prediction = classifier.score(counts,all_classes)
    print prediction
    return classifier

if __name__ == "__main__":
    stopwords_obj = stopwords.Stopwords(stopwords_file)
    for cl in classes:
        print cl
        for root, subFolders, files in os.walk(os.path.join(data_dir,cl)):
            if len(files) <= 0:
                continue
            for f in files:
                process_document(os.path.join(root,f),cl)
                #break
            #break
        #break
    output_document_matrix("trial.txt")
    classifier= train_model()

