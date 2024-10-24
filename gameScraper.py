
from urllib.request import urlopen
from urllib.error import *
from bs4 import BeautifulSoup
import re
from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ContextTypes


# content class
class content:
    def __init__(self,webName,gameName): # will add image in future
        self.webName = webName
        self.gameName = gameName
        self.gameLink = []
    
    def __str__(self):
        if self.gameLink == []:
            return "NO LINK FOUND"
        else:
            rVal = f"Website: {self.webName}\nGame: {self.gameName}\n\n"
            for item in self.gameLink:
                rVal += item + "\n"
        return rVal

#contentStack class
class contentStack:
    def __init__(self):
        self.data = []
        self.ptr = 0
        self.key = ""
    
    def push(self,data:content,key)->None:
        # if data in self.data: # this line saves a lot of space
        #     return
        
        if self.key == key:
            self.data.append(data)
            self.ptr+=1
        else:
            self.data = [data]
            self.key = key
            self.ptr = 1

    def isExist(self,p,string) -> bool:
        if self.data[p].gameName == string:
            return True
        return False
    
    def is_empty(self)->None:
        if self.data == {}:
            return True
        return False
        


    
    

# website class
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
                
    
    async def search(self,update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
        if 'contentStack'  not in context.user_data:
            await update.message.reply_text("First start the bot!!")
            return
        
        key = update.message.text
        await update.message.reply_text(f"Searching for <b>{key}</b>\n Don't panic, It may take several minutes.",parse_mode="HTML")
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
            button = []
            start_message = f"Seaching in <b><a href='{self.webUrl}'>{self.webName}</a></b>"
            m = await update.message.reply_text(start_message,parse_mode="HTML")
            messageID = m.message_id
            chatID = update.message.chat_id

            for searchTag in searchTagList:
                try:
                    tagURL = urlopen(self.get_url(searchTag.attrs['href']))
                    
                except Exception as e:
                    pass
                else:
                    gamePageHTML = BeautifulSoup(tagURL,'html.parser')
                    gameName = str(self.get_gameName(searchTag))[:30]

                    gameINFO = content(self.webName,gameName) # content instance


                    # await update.message.reply_text(gameName)
                    button.append([InlineKeyboardButton(gameName,callback_data=f"{context.user_data['contentStack'].ptr} {gameName}")])
                    
                    await context.bot.edit_message_text(
                        message_id=messageID,
                        chat_id=chatID,
                        text=start_message,
                        reply_markup=InlineKeyboardMarkup(button),
                        parse_mode="HTML"
                    )

                    tagURL.close()
                    contentTagList = gamePageHTML.select(self.contentSelector)
                    if not self.contentFilterDict == None:
                        contentTagList = [tag for tag in contentTagList if self.contentFilter(tag)]
                    listOFlink = []
                    for item in contentTagList:
                        attrDict = item.attrs
                        if "href" in attrDict:
                            listOFlink.append(attrDict["href"])
                    gameINFO.gameLink = listOFlink
                    context.user_data['contentStack'].push(gameINFO,key)
            await update.message.reply_text(f"Done searching in <b>{self.webName}</b>",parse_mode="HTML")
            
                    
            
            
 
# apun = website("ApunKaGames","https://www.apunkagames.com","/?s=","article .entry-title a",".entry-content a",{"href":"vlink"})
# print(apun.search("god of war"))

# with open("./websiteData.csv","r") as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(dict(row[-1]))