from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from tracker import find_price,convert_to_numeric

# Defining the states for the conversation handler
PRODUCT1, PRODUCT2, BUDGET = range(3)

# Handler for the /addproduct command to start setting the products
async def start_setproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send the first product (from Amazon or Flipkart) URL.")
    return PRODUCT1

# Handler to store the URL of the first product
async def first_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['first_url'] = update.message.text
    await update.message.reply_text("Thank you! Now please send the second product (from Amazon or Flipkart) URL.")
    return PRODUCT2

# Handler to store the URL of second product
async def second_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['second_url'] = update.message.text
    await update.message.reply_text("Great! Please send your budget.")
    return BUDGET

# Handler to store the budget and initiate price comparison
async def budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        budget_str = update.message.text
        budget = convert_to_numeric(budget_str)
        if budget is None:
            await update.message.reply_text("Please provide a valid number for the budget.")
            return BUDGET
        context.user_data['budget'] = budget
        await check_prices(update, context)
    except ValueError:
        await update.message.reply_text("Please provide a valid number for the budget.")
        return BUDGET
    return ConversationHandler.END

# Function to compare prices of the two products and provide responses
async def check_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_url = context.user_data.get('first_url')
    second_url = context.user_data.get('second_url')
    budget = context.user_data.get('budget')

    #Check if URLs and budget are set
    if not first_url or not second_url or not budget:
        await update.message.reply_text("Please set the products first using /addproduct.")
        return

    # Retrieve prices for both the products
    first_price = find_price(first_url)
    second_price = find_price(second_url)

    # Respond with product 1 details
    if first_price is not None:
        if first_price <= budget:
            await update.message.reply_text(f"First Product is within your budget: ₹{first_price}\n\nBuy Now:\n{first_url}")
        else:
            await update.message.reply_text(f"First Product is currently ₹{first_price-budget} more over your budget, priced at ₹{first_price}. You can try again later using the command: /getprice.")
    else:
        await update.message.reply_text("Could not retrieve the price for the first product. Please check the URL.")

    # Respond with product 2 details
    if second_price is not None:
        if second_price <= budget:
            await update.message.reply_text(f"Second Product is within your budget: ₹{second_price}\n\nBuy Now:\n{second_url}")
        else:
            await update.message.reply_text(f"Second Product is currently ₹{second_price-budget} more over your budget, priced at ₹{second_price}. You can try again later using the command: /getprice.")
    else:
        await update.message.reply_text("Could not retrieve the price for the second product. Please check the URL.")

    #Compare prices between product 1 and product 2
    try:
        if not None and first_price<second_price and first_price<budget:
            await update.message.reply_text(f"First Product is currently ₹{float(second_price)-float(first_price)} cheaper than Second Product.")
        elif not None and first_price>second_price and second_price<budget:
            await update.message.reply_text(f"Second Product is currently ₹{float(first_price)-float(second_price)} cheaper than First Product.")
        else:
            await update.message.reply_text(f"Prices of both the products are same")
    except:
        await update.message.reply_text("Error Comparing the prices")

# Handler to cancel the operation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END