
from telegram import Update
from telegram.ext import ContextTypes
from gameScraper import contentStack
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    bot = await context.bot.get_me()
    botName = bot.first_name
    context.user_data['contentStack'] = contentStack()
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

async def contentStackItem_return(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
     
    query = update.callback_query
    await query.answer("Fetching Data")
    chatId = query.message.chat.id if query.message else query.from_user.id
    
    gameStack = context.user_data['contentStack']
    query_data = (query.data).split(' ',1) # [ptr,gameName]
    query_data[0] = int(query_data[0])

  #for debugging  
    # for item in gameStack.data:
    #     print(item)

    if gameStack.isExist(query_data[0],query_data[1]):
        gameInfo = str(gameStack.data[query_data[0]])
        await context.bot.send_message(chat_id=chatId,text=gameInfo)
    else:
        await context.bot.send_message(chat_id=chatId,text="THIS LINK HAS BEEN EXPIRED")
