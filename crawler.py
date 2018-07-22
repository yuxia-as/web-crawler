# -*- coding: utf-8 -*-

"""
This project is created to crawl those hyperlinks for definitions
in a wikipedia page. In order to reduce running time, only five links 
will be randomly selected in each page.
In the first layer, crawl the target page and randomly get 5 hyperlinks;
In the second layer, crawl the 5 hyperlinks and get another 5 hyperlinks
from each;
In the next layer, do the same thing. And this can keep going on and on.
"""


from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

base_url = "https://en.wikipedia.org"
page="/wiki/Language"

#crawl a single page and randomly get 5 links
def get_sub_url(page):
    full_url = base_url+page    
    html = urlopen(full_url).read().decode("utf-8")
	# using beautifulsoup to get html contents    
    soup = BeautifulSoup(html, features='lxml')
    #get the current page title from h1 tag
    title = soup.find('h1').get_text()
    #find all the a tag which has the format of /wiki/ + letters/_        
    sub_urls = soup.find_all('a',{'href':re.compile('^(/wiki/)[A-Za-z_]+$')})
    sub_list=[]
    #loop 5 times to get 5 links and store them into a list
    for i in range(5):
        sub_list.append((random.sample(sub_urls,1)[0])['href'])
    #put title and urls into a list. this is the basic data structure:
    #[title,[url1,url2,...url5]]
    sub_url_content = [title,sub_list]
    return sub_url_content

#craw the target page and take it as first layer 
def get_first_layer(page):
    return get_sub_url(page)
#crawl the first layer by loop through 5 links to get second layer. 
#Now the data structure becomes:[[tile,[url1...url5]],[title,[url1,...url5]]...]        
def get_second_layer(layer):
    new_layer = []
    for url in layer[1]:
        new_layer.append(get_sub_url(url))
    return new_layer
        
#loop through the second layer. the new layer data has
#the same data structure as the second layer            
def get_new(layer):
    new_layer = []
    for l in layer:
        for url in l[1]:
            new_layer.append(get_sub_url(url))
    return new_layer


#first layer has slightly different data structure from other layers, 
#so write them to a file in different functions   
def write_first_layer(layer1):    
    name='layer1.txt'
    text_file = open(name,'w',encoding="utf8")
    for item in layer1:
        #check if item is a list,if not, item will be a title
        if type(item)==type([]):
            for content in item:
                #write full urls to a file
                text_file.write("\t"+base_url+content+"\n")
        else:
            text_file.write(item+":\n") 
    text_file.close()

#write function for all other layers 
def write_other_layer(layer,i):
    #use i to name file as layer3,layer4...
    name='layer'+i.__str__()+'.txt'
    text_file = open(name,'w',encoding="utf8")
    for wrapper_item in layer:
        for item in wrapper_item:
            if type(item)==type([]):
                for content in item:
                    text_file.write("\t"+base_url+content+"\n")
            else:
                text_file.write(item+":\n") 
    text_file.close()

#from layer3,all the following use same data structure,crawling and writing function
#every next layer is got by crawling the previous layer
def get_next(layer2,depth,i):
    while depth>2:
        #get the next layer
        next_layer = get_new(layer2)
        #write to a file
        write_other_layer(next_layer,i)
        #change i and depth to control layer name and loop counts
        i += 1
        depth -= 1
        #using recursive loop to get next layer on and on until the target depth
        get_next(next_layer,depth,i)
        break
        

#crawl layers based on the depth. Get each layer and write it to a file.            
def crawl_layers(first_page,depth):
    if depth<1:
        return
    elif depth==1:
        layer1 = get_first_layer(first_page)
        write_first_layer(layer1)
    elif depth==2:
        layer1 = get_first_layer(first_page)
        write_first_layer(layer1)
        layer2 = get_second_layer(layer1)
        write_other_layer(layer2,2)
    else:
        layer1 = get_first_layer(first_page)
        write_first_layer(layer1)
        layer2 = get_second_layer(layer1)
        write_other_layer(layer2,2)
        get_next(layer2,depth,3)

#crawl the target page and go into 5 depth        
crawl_layers(page,5)       
          
        




   
    
        
        
        