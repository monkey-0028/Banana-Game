from telegram.ext import Application, CommandHandler, MessageHandler,filters,CallbackQueryHandler
from gameScraper import website
from Command_Handlers import *
import os



   
# main code
if __name__ == "__main__":
    token = os.getenv("TELE_TOKEN")
    if token == None:
        raise Exception("Telegram token is not found in env-variable")
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('description',des))
    app.add_handler(CommandHandler('status',status))
    app.add_handler(CommandHandler('log',log))

    apunkagames = website("Fitgirl","https://fitgirl-repacks.site","/?s=","article .entry-title a",".entry-content ul a",{'text' : 'file hoster'},None,None)
    gamestack = contentStack
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,apunkagames.search))

    app.add_handler(CallbackQueryHandler(contentStackItem_return))

    app.run_polling()

   

'''
1. change the structure of game content (make it pure list)
2. store the ptr in function(search) itself. and make sure everytime search runs, it start from 0
3. make sure that contentStack also became empty as search runs.
4. Handle the click of previous inlineButtons, whose data have been removed.
5. but search is specific to one website only. if more than one website is run. it will wipe the previous daata from website
6. but if you choose to keep the data then it'll keep the data from very old search as well.
'''

