import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN")
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# --- Main Menu Function ---
def get_welcome_content(first_name):
    bold_name = f"*{first_name}*"
    text = (
        f"Hey, {bold_name}!\n\n"
        "👋 *Welcome to Broker Account Guide Bot!*\n\n"
        "Please choose an option below to continue:"
    )
    keyboard = [
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ]
    # Niche wala button (Reply Keyboard)
    reply_kb = ReplyKeyboardMarkup([['🎁 Claim Your FREE Premium Gold VIP Access Now']], resize_keyboard=True)
    return text, InlineKeyboardMarkup(keyboard), reply_kb

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name or "Trader"
    text, inline_markup, reply_markup = get_welcome_content(first_name)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown") # Pehle ReplyKeyboard bhejega
    await update.message.reply_text("Select an option:", reply_markup=inline_markup)

# ===== BUTTON HANDLER =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"

    if data == "start_again":
        text, inline_markup, _ = get_welcome_content(first_name)
        await query.edit_message_text(text, reply_markup=inline_markup, parse_mode="Markdown")

    elif data == "new_here":
        keyboard = [[InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)], [InlineKeyboardButton("🔙 Back", callback_data="start_again")]]
        await query.edit_message_text("👋 *Welcome!*\n\nTo get VIP access, please register using our official partner link below.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif data == "from_website":
        keyboard = [[InlineKeyboardButton("✅ Registered", callback_data="registered")], [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")], [InlineKeyboardButton("🔙 Back", callback_data="start_again")]]
        await query.edit_message_text("🌐 *Website User*\n\nPlease select your status:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    # --- Registered (Ab simple hai) ---
    elif data == "registered":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text(
            "✅ *Registration Received!*\n\n"
            "Please type and send your *Trading Account ID* below.\n\n"
            "⏳ Verification usually takes *1-2 hours*.\n"
            "After verification, you will receive your VIP Access.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

# ===== HANDLE USER MESSAGES (ID & Bottom Button) =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Agar user niche wale button par click kare
    if "Claim Your FREE Premium" in user_text:
        await update.message.reply_text(
            "To claim your VIP access, make sure you have registered via our link and then send your Account ID here."
        )
    else:
        # Agar user ID send kare
        await update.message.reply_text(
            f"✅ *Received!*\n\nYour ID: `{user_text}`\n\nOur team will verify this shortly. Thank you!",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
    
