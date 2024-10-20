from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from gameScraper import website, content
import os

# --- handling BOT ---
# Command Handlers function
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    bot = await context.bot.get_me()
    botName = bot.first_name
    await update.message.reply_text(f"Hi, I am {botName}\nI will search games for you!😁")

# /description
async def des(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text(f"Text me name of the game and i will scrape the download-links for you")

# /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    await update.message.reply_text("NOT COMPLETE")

# /log
async def log(update: Update,context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text("This command is not completed yet! wait for updates.🙏")
   
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

    app.run_polling()

   
'''
1. Provide Click and download link (for this i have to make my script crawl through link; make a general system applicable for most website)
2. Also do the checking wether the link is dead or not
3. Error handeling including void field
4. Expand the search (crawl through the whole website to find all search) # Create a "Crawler" method to manage this work
5. Handle additional information if available (eg. platform(ps4/ps3/pc), region: Jap/US etc)
'''
