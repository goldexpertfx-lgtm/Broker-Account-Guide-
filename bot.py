import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN") 
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# --- Main Menu & Keyboard Logic ---
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
    # These are the WORKING buttons that appear inside the message
    inline_kb = [
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ]
    # This is the button at the very bottom
    reply_kb = ReplyKeyboardMarkup(
        [['🎁 Claim Your FREE Premium Gold VIP Access Now']], 
        resize_keyboard=True
    )
    return text, InlineKeyboardMarkup(inline_kb), reply_kb

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name or "Trader"
    text, inline_markup, reply_markup = get_welcome_content(first_name)
    # This sends the message WITH the buttons
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    await update.message.reply_text("Select an option:", reply_markup=inline_markup)

# ===== BUTTON HANDLER (Working Links & Actions) =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"*{first_name}*"

    if data == "start_again":
        text, inline_markup, _ = get_welcome_content(first_name)
        await query.edit_message_text(text, reply_markup=inline_markup, parse_mode="Markdown")

    elif data == "new_here":
        keyboard = [
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(f"👋 Welcome {bold_name}!\n\nTo get VIP access, please register using our official partner link below.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "old_here":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(f"👋 Welcome back, {bold_name}!\n\nIf you need help connecting your account, contact our support team.\n\n💡 *Note:* VIP benefits are only for partner accounts.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "from_website":
        keyboard = [
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(f"🌐 Welcome {bold_name}!\n\nPlease select the correct option below:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "registered":
        keyboard = [
            [InlineKeyboardButton("💬 LiveChat", callback_data="live_chat")],
            [InlineKeyboardButton("🔙 Back", callback_data="from_website")]
        ]
        await query.edit_message_text(
            "✅ *Registration Received!*\n\n"
            "Please type and send your *Trading Account ID* below.\n"
            "⏳ Verification usually takes *1-2 hours*.\n\n"
            "After verification, you will receive your VIP Access.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "live_chat":
        keyboard = [[InlineKeyboardButton("Chat Now ✅", url=SUPPORT_LINK)], [InlineKeyboardButton("🔙 Back", callback_data="registered")]]
        await query.edit_message_text("Feel free to contact our customer support for any assistance.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "changed_ib":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text("🔁 *Partner Code Change*\n\nPlease send proof of IB change and your Trading Account ID.\n⏳ Verification takes *1-2 hours*.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# ===== HANDLE USER MESSAGES =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if "Claim Your FREE Premium" in user_text:
        await update.message.reply_text("To claim your VIP access, please make sure you have registered via our link and then send your Account ID here.")
    else:
        await update.message.reply_text(
            f"✅ *Received!*\n\nYour Detail: `{user_text}`\n\nOur team will verify this shortly. Thank you!",
            parse_mode="Markdown"
        )

def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
