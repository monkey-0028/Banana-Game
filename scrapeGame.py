from urllib.request import urlopen
from urllib.error import *
from bs4 import BeautifulSoup
import re

class website:
    def __init__(self,name,url,searchUrl,resultUrl,contentSelector,contentFilterDict=None,gameNameSelector=None,addOnInfo=None):
        self.webName = name
        self.webUrl = url
        self.webSearchUrl = searchUrl
        self.webResultUrl = resultUrl
        self.contentSelector = contentSelector
        self.contentFilterDict = contentFilterDict
        self.gameNameSelector = gameNameSelector
        self.addOnInfo = addOnInfo

    def r_pattern(self,key,searchString):
        p = ".*"
        for item in key:
            if item  == " ":
                p += "[.,/:;_=|\\-+\\s]*"
            else:
                p += f"({item.upper()}|{item.lower()})"
        if re.match(p,searchString):
            return True
        else:
            return False
    
    def get_url(self,url):
        pattern = self.webUrl + ".*"
        if re.match(pattern,url):
            return url
        else:
            return self.webUrl+url
    
    def get_gameName(self,tag_OR_html):
        if self.gameNameSelector == None:
            try:
                return tag_OR_html.get_text()
            except Exception as e:
                return "NA"
        else:
            try:
                return tag_OR_html.select(self.gameNameSelector).get_text()
            except Exception as e:
                return "NA"

    def contentFilter(self,tag):
        # AND principle
        tagAttrDict = tag.attrs
        for item in self.contentFilterDict:
            if item == "text":
                if not (self.r_pattern(str(self.contentFilterDict[item]),str(tag.get_text()))):
                        return False
            else:
                if item in tagAttrDict:
                    if not (self.r_pattern(str(self.contentFilterDict[item]),str(tagAttrDict[item]))):
                        return False
        return True
                
    
    def search(self,key):
        try:
            url = urlopen(self.webUrl+self.webSearchUrl+(key.replace(" ","+")))
        except HTTPError as e0:
            print("webpage is not found\n")
            print(e0)
        except URLError as e1:
            print("wrong website url\n\n")
            print(e1)
        else:
            html = BeautifulSoup(url,'html.parser')
            url.close()
            searchTagList = html.select(selector=self.webResultUrl)
            try:
                searchTagList = [tag for tag in searchTagList if self.r_pattern(key,tag.get_text())] # Filtered the "Result Tags"
            except Exception as e:
                pass

            #iterating each link
            contentDict = dict()
            for searchTag in searchTagList:
                try:
                    tagURL = urlopen(self.get_url(searchTag.attrs['href']))
                    
                except Exception as e:
                    pass
                else:
                    gamePageHTML = BeautifulSoup(tagURL,'html.parser')
                    gameName = self.get_gameName(searchTag)
                    tagURL.close()
                    contentTagList = gamePageHTML.select(self.contentSelector)
                    if not self.contentFilterDict == None:
                        contentTagList = [tag for tag in contentTagList if self.contentFilter(tag)]
                    listOFlink = []
                    for item in contentTagList:
                        attrDict = item.attrs
                        if "href" in attrDict:
                            listOFlink.append(attrDict["href"])
                    contentDict[gameName] = listOFlink
            
            return content(self.webName,contentDict)
                    
                   



            
            
                    
                    
                


    
    

    
class content:
    def __init__(self,webName,contentDict):
        self.webName = webName
        self.contentDict = contentDict # {gameName: [link-tag]}
    
    def __str__(self):
        m = f"Website: {self.webName}\n\n"
        for element in self.contentDict:
            m += "\t"+element
            for link in self.contentDict[element]:
                m += f"\n\t\t{link}"
            m += "\n\n"
        return m
        

        
# name,url,searchUrl,resultUrl,contentSelector,contentFilterDict=Non
fitgirl = website("Fitgirl","https://fitgirl-repacks.site","/?s=","article .entry-title a",".entry-content ul a",{"text" : "file hoster"})
apunkagames = website("ApunKaGames","https://www.apunkagames.com","/?s=","article .entry-title a",".entry-content a",{"href":"vlink"})


print(fitgirl.search("God of war"))
print(apunkagames.search("God of war"))


# -- require update -- ##
'''
1. Provide Click and download link (for this i have to make my script crawl through link; make a general system applicable for most website)
2. Also do the checking wether the link is dead or not
3. Error handeling including void field
4. Expand the search (crawl through the whole website to find all search) # Create a "Crawler" method to manage this work
5. Handle additional information if available (eg. platform(ps4/ps3/pc), region: Jap/US etc)
'''
