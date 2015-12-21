import os
import sys
import re
import numpy
import pandas
from scipy.sparse import hstack,coo_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.metrics import confusion_matrix, f1_score

classes = ["course","department","faculty","other","project","staff","student","calendar_events","files","news","technical_support"]
tags = re.compile(r'<.*?>')

def get_document(f):
    fp = open(f,"r")
    doc = fp.read()
    return doc

def process_document(doc):
    doc = doc.lower()
    doc = trim_document(doc)
    doc = remove_tags(doc)
    return doc


def remove_tags(text):
    return tags.sub('',text)

def trim_document(doc):
    # Applies only for html documents. If we need text documents in training framework then other method needs to be applied.
    rdoc = '<'.join(doc.split("<")[1:])
    return "<" + rdoc

'''
def generate_features(dir,type):
    list_cl=[]
    list_file=[]
    list_docs = []
    for cl in classes:
        for root, subFolders, files in os.walk(os.path.join(dir,cl)):
            if len(files) <= 0:
                continue
            for f in files:
                doc = get_document(os.path.join(root,f))
                new_doc = process_document(doc)
                list_cl.append(cl)
                list_docs.append(new_doc)
                list_file.append(f)
    counts=None
    if type == "train":
        counts = count_vectorizer.fit_transform(list_docs)
    else:
        counts = count_vectorizer.transform(list_docs)
    return (counts,list_file,list_cl)

def train(dir):
    train_features,train_files,train_classes = generate_features(dir,"train")
    classifier = MultinomialNB(alpha=1)
    classifier.fit(train_features,train_classes)
    print classifier.classes_
    print classifier.class_count_
    return classifier

def test(dir,classifier):
    test_features,test_files,test_classes = generate_features(dir,"test")
    predictions = classifier.score(test_features,test_classes)
    print predictions
'''
def read_dataframe(dir):
    print "Reading data"
    numpy.random.seed(1)
    index=[]
    rows=[]
    for cl in classes:
        for root, subFolders, files in os.walk(os.path.join(dir,cl)):
            if len(files) <= 0:
                continue
            for f in files:
                doc = get_document(os.path.join(root,f))
                new_doc = process_document(doc)
                rows.append({"text":new_doc,"class":cl})
                index.append(os.path.join(root,f))
    data = pandas.DataFrame(rows, index=index)
    data = data.iloc[numpy.random.permutation(len(data))]
    return data

def print_misclassified(filenames,true_y,pred_y,label):
    dictionary_val = {"true":true_y,"predicted":pred_y,"filename":filenames}
    data = pandas.DataFrame(dictionary_val)
    new_data = data[data["true"]==label]
    new_data = new_data[new_data["predicted"]!=label]
    print new_data["filename"].iloc[0]

def cross_validation(dir):
    data = read_dataframe(dir)
    alphas=[0.1,0.2,0.25,0.3,0.35,0.4,0.5]
    alphas = [0.6]
    average_scores= []
    for alpha in alphas:
        print alpha
        scores = []
        k_fold = KFold(n=len(data), n_folds=5)
        for train_indices, test_indices in k_fold:
            train_text = data.iloc[train_indices]['text'].values
            #train_counturls =data.iloc[train_indices]['number_urls'].values
            train_y = data.iloc[train_indices]['class'].values
            test_text = data.iloc[test_indices]['text'].values
            test_y = data.iloc[test_indices]['class'].values
            #test_counturls = data.iloc[test_indices]['number_urls'].values

            filenames = data.iloc[test_indices].index.values
            count_vectorizer = CountVectorizer(decode_error ="ignore",stop_words="english")
            count_vectorizer2 = CountVectorizer(decode_error ="ignore",stop_words="english")
            #train_counturls_features = count_vectorizer2.fit_transform(train_counturls)
            train_features = count_vectorizer.fit_transform(train_text)
            test_features = count_vectorizer.transform(test_text)
            #test_counturls_features = count_vectorizer2.transform(test_counturls)
            #train_features = hstack([train_features,train_counturls_features])
            #test_features = hstack([test_features,test_counturls_features])

            #classifier = MultinomialNB(alpha=alpha)
            classifier = LogisticRegression(penalty='l1',C=alpha)
            classifier.fit(train_features,train_y)

            predictions = classifier.predict(test_features)
            confmatr = confusion_matrix(test_y,predictions)
            print confmatr
            print classifier.classes_
            for i in range(len(predictions)):
                print filenames[i],test_y[i],predictions[i]
            #print_misclassified(filenames,test_y,predictions,"student")
            sys.exit()

            score = classifier.score(test_features,test_y)
            scores.append(score)
        print('Total data classified:', len(data))
        average_scores.append(numpy.average(scores))
        print alpha,numpy.max(scores),numpy.min(scores),numpy.average(scores)
    plot_psuedocount_vs_accuracy(alphas,average_scores)

def plot_psuedocount_vs_accuracy(psuedocounts, accuracies):
    """
    A function to plot psuedocounts vs. accuries. You may want to modify this function
    to enhance your plot.
    """
    import matplotlib.pyplot as plt

    plt.plot(psuedocounts, accuracies)
    plt.xlabel('Psuedocount Parameter')
    plt.ylabel('Accuracy (%)')
    plt.grid()
    plt.title('Psuedocount Parameter vs. Accuracy Experiment')
    plt.show()

if __name__ == "__main__":
    train_directory = "/home/neha/Desktop/Independent Study/data/tac_kbp_test_data"
    test_directory = "/home/neha/Desktop/Independent Study/data/tac_kbp_test_data"
    #classifier = train(train_directory)
    #test(test_directory,classifier)
    cross_validation(train_directory)
