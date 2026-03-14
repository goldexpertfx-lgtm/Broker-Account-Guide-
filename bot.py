# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# ===== CONFIG =====
TOKEN = os.environ.get("BOT_TOKEN")  # Render env variable
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name or "User"
    # Bold using MarkdownV2
    bold_name = f"**𝗛𝗲𝘆, {first_name}!**"
    
    keyboard = [
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 From Website", callback_data='from_website')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"{bold_name}\n\n"
        "👋 **Welcome to Broker Account Guide Bot!**\n\n"
        "Here you can unlock:\n"
        "📊 **Premium XAUUSD (Gold) Signals**\n"
        "🎁 **Exclusive Gifts & Giveaways**\n"
        "💎 **Access to our VIP Trading Community**\n\n"
        "Please choose an option below to continue:"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# ===== BUTTON HANDLER =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "User"
    bold_name = f"**{first_name}**"

    if data == "new_here":
        keyboard = [
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"👋 Welcome {bold_name}!\n\n"
            "If you want to get:\n"
            "📊 **Premium XAUUSD Gold Signals**\n"
            "🎁 **Free Gifts & Giveaways**\n"
            "💎 **VIP Community Access**\n\n"
            "You must register using our official partner link.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "old_here":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"👋 Welcome back, {bold_name}!\n\n"
            "If you already have an account but need help connecting it with our Partner Code, our support team is here to help you.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "from_website":
        keyboard = [
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"🌐 Welcome {bold_name}!\n\n"
            "If you came from our website, please select the correct option below so we can activate your VIP benefits.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "registered":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text(
            "✅ **Registration Received**\n\n"
            "Please send your **Trading Account ID** so we can verify it.\n\n"
            "After verification you will receive:\n"
            "📊 **Premium XAUUSD Gold Signals**\n"
            "🎁 **Gifts & Giveaways**\n"
            "💎 **VIP Access**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "changed_ib":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text(
            "🔁 **Partner Code Change**\n\n"
            "Please send:\n"
            "📄 **Proof of IB Change**\n"
            "🆔 Your **Trading Account ID**\n\n"
            "After verification you will receive:\n"
            "📊 **Premium XAUUSD Gold Signals**\n"
            "🎁 **Gifts & Giveaways**\n"
            "💎 **VIP Access**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "start_again":
        # Send start menu again
        await start(update, context)

# ===== HANDLE USER MESSAGES =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    first_name = update.message.from_user.first_name or "User"
    bold_name = f"**{first_name}**"

    await update.message.reply_text(
        f"✅ Received your message {bold_name}:\n{user_text}\n\n"
        "Our support team will verify and send your VIP benefits shortly.",
        parse_mode="Markdown"
    )

# ===== MAIN APPLICATION =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
