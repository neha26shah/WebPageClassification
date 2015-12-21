import os
import random
import sys
import shutil

def split_folders(train_dir,test_dir):
    data_dir="/home/neha/Desktop/Independent Study/data/webkb"
    for root, subFolders, files in os.walk(data_dir):
        print root,subFolders,files
        parent_root = root.split("webkb")
        print "Parent root",parent_root
        parent_root_test=test_dir
        parent_root_train=train_dir
        print train_dir,parent_root[1]
        if len(parent_root) > 1:
            parent_root_train = train_dir+parent_root[1]
            parent_root_test  =test_dir+parent_root[1]
        print "train",parent_root_train
        print "test",parent_root_test
        for folder in subFolders:
            try:
                os.stat(os.path.join(parent_root_train,folder))
            except:
                os.mkdir(os.path.join(parent_root_train,folder))
            try:
                os.stat(os.path.join(parent_root_test, folder))
            except:
                os.mkdir(os.path.join(parent_root_test,folder))
        for f in files:
            coin = random.randint(1,10)
            if coin <= 8:
                dest = os.path.join(parent_root_train,f)
                print "DEEESY",dest
                shutil.copy(os.path.join(root,f),dest)
            else:
                dest= os.path.join(parent_root_test,f)
                print "DEEEEST",dest
                shutil.copy(os.path.join(root,f),dest)


def generate_folders(train_dir,output_dir):
    for root,subFolders,files in os.walk(train_dir):
        print root
        print subFolders
        print files
        print len(subFolders)
        for folder in subFolders:
            list_files = os.listdir(os.path.join(root,folder))
            chosen_file = random.choice(list_files)
            shutil.copy(os.path.join(root,folder,chosen_file),output_dir)
            chosen_file = random.choice(list_files)
            shutil.copy(os.path.join(root,folder,chosen_file),output_dir)
            chosen_file = random.choice(list_files)
            shutil.copy(os.path.join(root,folder,chosen_file),output_dir)
            chosen_file = random.choice(list_files)
            shutil.copy(os.path.join(root,folder,chosen_file),output_dir)
            print folder
        break

def move_classify(train_dir):
    list_files = os.listdir(train_dir)
    print list_files
    print len(list_files)
    for item in list_files:
        new_full_path = os.path.join(train_dir,item)
        if os.path.isdir(new_full_path):
            continue
        prelude = "PENN_SAS_ENG_"
        numbers =item.split("_")[3].split(".")[0]
        varied_path = os.path.join("/home/neha/Desktop/Independent Study/data/tac_kbp/TAC_2012_KBP_Cold_Start_Evaluation_Corpus_v1.3/data/xml",numbers[0:2],prelude+numbers+".xml")
        fp = open(varied_path)
        lines= fp.readlines()
        fp.close()
        print lines
        value = sys.stdin.read(2)
        value = value[0]
        print value
        destination=""
        if value=="c":
            print "Course"
            destination=os.path.join(train_dir,"course")
        elif value=="d":
            print "department"
            destination=os.path.join(train_dir,"department")
        elif value=="f":
            print "faculty"
            destination=os.path.join(train_dir,"faculty")
        elif value =="o":
            print "Other"
            destination=os.path.join(train_dir,"other")
        elif value =="e":
            print "Calendar"
            destination=os.path.join(train_dir,"other","calendar_events")
        elif value=="t":
            print "Technical Support"
            destination=os.path.join(train_dir,"other","technical_support")
        elif value=="i":
            print "Hub Page"
            destination=os.path.join(train_dir,"other","hub_pages")
        elif value=="b":
            print "Attachements"
            destination=os.path.join(train_dir,"other","files")
        elif value=="n":
            print "News"
            destination=os.path.join(train_dir,"other","news")
        elif value=="m":
            print "masters"
            destination=os.path.join(train_dir,"other","programs")
        elif value=="h":
            print "Course Help"
            destination=os.path.join(train_dir,"other","courses_help")
        elif value=="p":
            print "Project"
            destination=os.path.join(train_dir,"project")
        elif value=="a":
            destination=os.path.join(train_dir,"staff")
            print "staff"
        elif value=="u":
            print "student"
            destination=os.path.join(train_dir,"student")
        else:
            sys.exit()
        shutil.move(new_full_path,destination)
train_dir= "/home/neha/Desktop/Independent Study/data/tac_kbp/TAC_2012_KBP_Cold_Start_Evaluation_Corpus_v1.3/data/html"
output_dir="/home/neha/Desktop/Independent Study/data/tac_kbp/test_classification_data"
#generate_folders(train_dir,output_dir)
move_classify(output_dir)


