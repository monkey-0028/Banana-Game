from telegram.ext import Application, CommandHandler, MessageHandler,filters,CallbackQueryHandler
from gameScraper import website
from Command_Handlers import *
import os
import csv
import ast

CSV_FILE = "./websiteData.csv"
async def enable_multiWebSearch(update:Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['contentStack'] = contentStack()
    context.user_data['SearchLoop_flag'] = False 
    context.user_data['Message_flag'] = True # True means it will allow message else not

    key = update.message.text

    global CSV_FILE
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            await website(row[0],row[1],row[2],row[3],row[4],ast.literal_eval(row[5]),ast.literal_eval(row[6]),ast.literal_eval(row[7])).search(update,context)
        context.user_data['SearchLoop_flag'] = True
        


   
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,enable_multiWebSearch))

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

