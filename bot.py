# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# ====== CONFIG ======
TOKEN = os.environ.get("BOT_TOKEN")  # Set this in Render environment variable

PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# ====== START COMMAND ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 From Website", callback_data='from_website')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to VIP Gold Signals Bot!\n\nHere you can unlock:\n📊 Premium XAUUSD (Gold) Signals\n🎁 Exclusive Gifts & Giveaways\n💎 Access to our VIP Trading Community\n\nPlease choose an option below to continue:",
        reply_markup=reply_markup
    )

# ====== BUTTON HANDLER ======
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name

    if data == "new_here":
        keyboard = [[InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)]]
        await query.edit_message_text(
            "👋 Welcome!\n\nIf you want to get:\n📊 Premium XAUUSD Gold Signals\n🎁 Free Gifts & Giveaways\n💎 VIP Community Access\n\nYou must register using our official partner link.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "old_here":
        keyboard = [[InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)]]
        await query.edit_message_text(
            f"👋 Welcome back, {first_name}!\n\nIf you already have an account but need help connecting it with our Partner Code, our support team is here to help you.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "from_website":
        keyboard = [
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")]
        ]
        await query.edit_message_text(
            "🌐 Welcome!\n\nIf you came from our website, please select the correct option below so we can activate your VIP benefits.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "registered":
        await query.edit_message_text(
            "✅ Registration Received\n\nPlease send your Trading Account ID so we can verify it.\n\nAfter verification you will receive:\n📊 Premium XAUUSD Gold Signals\n🎁 Gifts & Giveaways\n💎 VIP Access"
        )

    elif data == "changed_ib":
        await query.edit_message_text(
            "🔁 Partner Code Change\n\nPlease send:\n📄 Proof of IB Change\n🆔 Your Trading Account ID\n\nAfter verification you will receive:\n📊 Premium XAUUSD Gold Signals\n🎁 Gifts & Giveaways\n💎 VIP Access"
        )

# ====== HANDLE USER MESSAGES ======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Simple echo for user messages or account IDs / proof submission
    user_text = update.message.text
    await update.message.reply_text(
        f"✅ Received your message:\n{user_text}\n\nOur support team will verify and send your VIP benefits shortly."
    )

# ====== MAIN APPLICATION ======
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
