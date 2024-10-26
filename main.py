from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from gameScraper import website
from Command_Handlers import *
from flask import Flask
import os
import csv
import ast
from threading import Thread

app = Flask(__name__)

CSV_FILE = "./websiteData.csv"

async def enable_multiWebSearch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['Message_flag'] = True  # True means it will allow message else not
    global CSV_FILE
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            await website(row[0], row[1], row[2], row[3], row[4], ast.literal_eval(row[5]), ast.literal_eval(row[6]), ast.literal_eval(row[7])).search(update, context)
        context.user_data['SearchLoop_flag'] = True

# Flask route to check if the bot is running
@app.route('/')
def index():
    return "Bot is running!"

# Function to start the Telegram bot
async def start_bot():
    token = os.getenv("TELE_TOKEN")
    if token is None:
        raise Exception("Telegram token is not found in env-variable")
    
    bot = Application.builder().token(token).build()
    bot.add_handler(CommandHandler('start', start))
    bot.add_handler(CommandHandler('description', des))
    bot.add_handler(CommandHandler('status', status))
    bot.add_handler(CommandHandler('log', log))

    apunkagames = website("Fitgirl", "https://fitgirl-repacks.site", "/?s=", "article .entry-title a", ".entry-content ul a", {'text': 'file hoster'}, None, None)
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enable_multiWebSearch))
    bot.add_handler(CallbackQueryHandler(contentStackItem_return))

    await bot.run_polling()

if __name__ == "__main__":
    # Start the Telegram bot in a separate thread
    bot_thread = Thread(target=start_bot)
    bot_thread.start()

    # Run the Flask server
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
