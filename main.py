from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from bot_input import start_setproduct, first_url, second_url, budget, cancel, check_prices, PRODUCT1, PRODUCT2, BUDGET

TOKEN = "6406198312:AAHL6FYxlybcM594uvQG3tBqipnRIPYEmH4"

# Command handler for the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        Hi, I’m Robin! I’ll assist you in finding the best deals by comparing them based on your budget.
        \nTo add products and get their current prices, use the \n/addproduct command. Let’s get started! 😊
        """
    )

# Command handler for the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    """
    Hey there! I’m here to assist you with the following commands:
    \n/start: To start the bot\n
    \n/help: To access the help menu\n
    \n/addproduct: To set the required products\n
    \n/getprice: To check the prices again\n
    \n/cancel: To cancel the conversation\n
    \nI hope this helps :)
    """
    )

def main():
    # Create the Application and pass it your bot's token.
    app = Application.builder().token(TOKEN).build()

    # Define the ConversationHandler for managing the product setup conversation
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addproduct', start_setproduct)], # Entry point for the conversation
        states={
            PRODUCT1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_url)], # Handle Amazon URL input
            PRODUCT2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_url)], # Handle Flipkart URL input
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)], # Handle budget input
        },
        fallbacks=[CommandHandler('cancel', cancel)], # Fallback command to cancel the conversation
    )

    # Add handlers for the /start and /help commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Add the conversation handler to the application
    app.add_handler(conv_handler)

    # Add handler for the /getprice and /cancel command to check prices
    app.add_handler(CommandHandler("getprice", check_prices))
    app.add_handler(CommandHandler("cancel", cancel))
    # Start polling for updates from Telegram
    app.run_polling()

if __name__ == "__main__":
    main()