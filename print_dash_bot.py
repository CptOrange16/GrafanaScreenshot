import logging
import yaml
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from print_dashboard import get_screenshot

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def get_screencap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # Check if args exist
    if len(context.args) < 2:
        print(f"Bad args")
        await update.message.reply_text("Bad args. Use /start <dashboard> <range>. Eg. /start mtg_test now-6h")
        return 0
        
    # Check if args are valid
    try:
        dashboard = context.args[0]
        all_dashboards = context.bot_data['dashboards']
        if dashboard not in all_dashboards:
            print(f"Dashboard {dashboard} is not available")
            await update.message.reply_text(f"Dashboard {dashboard} is not available")
            return 0
        time_range = context.args[1]
    except Exception as e:
        print(e)
        await update.message.reply_text(f"Bad args or configs")
        return 0
    
    #TODO: for dates instead of range
    #url = temp_dashboard_dict[dashboard] + f"&from={datetime.timestamp(current_date)*1000}&to={datetime.timestamp(end_date)*1000}"
    
    try:
        url = all_dashboards[dashboard] + f"&from={time_range}&to=now"
        get_screenshot(url, "./image.png", context.bot_data['browser_path'], context.bot_data['browser_driver_path'], 
                       context.bot_data['grafana_user'], context.bot_data['grafana_password'], context.bot_data['sleep'])
    except Exception as e:
        print(e)
        await update.message.reply_text("Failed to generate image. Try again.")
        return 0
        
    if not os.path.isfile("./image.png"):
        print("Image not found on the server")
        update.message.reply_text("Image not found on the server")
        return 0
     
    with open("./image.png", 'rb') as screenshot:
        await update.message.reply_photo(screenshot) 
   
        
def main() -> None:
    
    with open('config.yml') as f:
        configs = yaml.safe_load(f)
        
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(configs['bot_api_token']).build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("get", get_screencap))
    
    # add configs to bot
    application.bot_data = configs
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
