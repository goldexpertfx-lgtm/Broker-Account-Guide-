import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") 
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

def get_welcome_content(first_name):
    bold_name = f"*{first_name}*"
    text = (
        f"Hey, {bold_name}!\n\n"
        "👋 *Welcome to Broker Account Guide Bot!*\n\n"
        "Here you can unlock:\n"
        "📊 *Premium XAUUSD (Gold) Signals*\n"
        "🎁 *Exclusive Gifts & Giveaways*\n"
        "💎 *Access to our VIP Trading Community*\n\n"
        "Please choose an option below to continue:"
    )
    keyboard = [
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ]
    return text, InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name or "Trader"
    text, reply_markup = get_welcome_content(first_name)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"*{first_name}*"

    if data == "start_again":
        text, reply_markup = get_welcome_content(first_name)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    elif data == "new_here":
        keyboard = [[InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)], [InlineKeyboardButton("🔙 Back", callback_data="start_again")]]
        await query.edit_message_text(f"👋 Welcome {bold_name}!\n\nIf you want VIP access, you must register using our official partner link.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "old_here":
        keyboard = [[InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Back", callback_data="start_again")]]
        await query.edit_message_text(f"👋 Welcome back, {bold_name}!\n\nIf you need help connecting your account, contact support.\n\n💡 *Note:* VIP benefits are for partner accounts only.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "from_website":
        keyboard = [[InlineKeyboardButton("✅ Registered", callback_data="registered")], [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")], [InlineKeyboardButton("🔙 Back", callback_data="start_again")]]
        await query.edit_message_text(f"🌐 Welcome {bold_name}!\n\nPlease select the correct option below.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "registered":
        keyboard = [[InlineKeyboardButton("💬 LiveChat", callback_data="live_chat")], [InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text("✅ *Registration Received!*\n\nPlease type and send your *Trading Account ID* below.\n⏳ Verification usually takes *1-2 hours*.\n\nAfter verification, you will receive your VIP Access.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "live_chat":
        keyboard = [[InlineKeyboardButton("Chat Now ✅", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Back", callback_data="registered")]]
        await query.edit_message_text("Feel free to contact our customer support for any assistance.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "changed_ib":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text("🔁 *Partner Code Change*\n\nPlease send proof of IB change and your Trading Account ID.\n⏳ Verification takes *1-2 hours*.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"✅ *Received!*\n\nYour ID: `{user_text}`\n\nOur team will verify this shortly. Thank you!", parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
        
