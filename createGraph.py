import sys
import os
from bs4 import BeautifulSoup
import csv
import codecs

input_directory ="/home/neha/Desktop/Independent Study/data/spidered/"
output_directory = "/home/neha/Desktop/Independent Study/data/spidered/parsed_data"

def check_url_exists(url):
    new_path = os.path.join(input_directory,url)
    if os.path.isfile(new_path):
        return True
    return False

def get_url_list(filename,url,keyword):
    list_url =[]
    with open(filename,"r") as fp:
        content = fp.read()
        try:
            soup = BeautifulSoup(content,"lxml")
        except:
            return list_url
        for link in soup.findAll("a"):
            original_url  = link.get("href")
            if original_url==None:
                continue
            if "mailto" in original_url:
                continue
            splitted_values= original_url.split(".")
            if splitted_values[-1] != "html" and splitted_values[-1] !="htm" and splitted_values[-1] !="php" and len(splitted_values[-1]) <4:
                continue
            if ":" in original_url:
                if keyword in original_url:
                    list_url.append(original_url)
            else:
                list_url.append(url+"/"+original_url)
    return list_url

def loop_through_all_files(url,keyword):
    found_urls={}
    nfound_urls={}

    file_links = open(os.path.join(output_directory,keyword+"_links.csv"),"w")
    file_found = open(os.path.join(output_directory,keyword+"_found.csv"),"w")
    file_nfound = open(os.path.join(output_directory,keyword+"_nfound.csv"),"w")
    directory_path = os.path.join(input_directory,url)
    for root, subdirs, files in os.walk(directory_path):
        for file in files:
            filename = os.path.join(root,file)
            print filename
            list_links = get_url_list(filename,root,keyword)
            print len(list_links)
            for link in list_links:
                new_link = link
                if ".." in link:
                    new_link = os.path.normpath(link)
                try:
                    file_links.write(filename+","+new_link+"\n")
                except:
                    continue
                if check_url_exists(new_link):
                    found_urls[new_link] = 1
                else:
                    nfound_urls[new_link]=1
    for u in found_urls.keys():
        file_found.write(u+"\n")
    for u in nfound_urls.keys():
        file_nfound.write(u+"\n")
    file_links.close()
    file_found.close()
    file_nfound.close()

def read_already_done(major_directory):
    output_file = os.path.join(output_directory,major_directory+"_nodes.csv")
    fp=open(output_file,"r")
    reader = csv.reader(fp)
    all_done =[]
    for row in reader:
        all_done.append(row[0])
    fp.close()
    return all_done

def classify_stuff(major_directory,comp_files):
    directory = os.path.join(input_directory,major_directory)
    fout = open(os.path.join(output_directory,major_directory+"_nodes.csv"),"a")
    writer = csv.writer(fout,quotechar = "'")
    for root, subdirs, files in os.walk(directory):
        for file in files:
            complete_file = os.path.join(root,file)
            if complete_file in comp_files:
                print "Skipping the file",complete_file
                continue
            else:
                comp_files.append(complete_file)
            print complete_file
            fp = open(complete_file,"r")
            content=fp.read()
            fp.close()
            print content
            print complete_file
            value = sys.stdin.readline().rstrip('\n')
            if value=="exit":
                fout.close()
                sys.exit()
            writer.writerow([complete_file,value])
    fout.close()
loop_through_all_files("www.cs.purdue.edu","cs.purdue.edu")
#already_done= read_already_done("www.cs.purdue.edu")
#already_done=[]
#classify_stuff("www.cs.purdue.edu",already_done)
