import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN")
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# --- Main Welcome Content Generator ---
def get_welcome_content(first_name):
    bold_name = f"**𝗛𝗲𝘆, {first_name}!**"
    text = (
        f"{bold_name}\n\n"
        "👋 **Welcome to Broker Account Guide Bot!**\n\n"
        "Unlock your trading benefits:\n"
        "📊 **Premium XAUUSD (Gold) Signals**\n"
        "🎁 **Exclusive Gifts & Giveaways**\n"
        "💎 **Access to VIP Community**\n\n"
        "Please choose an option below:"
    )
    # Inline buttons connected to the message
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ])
    # Permanent bottom button (Reply Keyboard)
    reply_kb = ReplyKeyboardMarkup([['💬 LiveChat']], resize_keyboard=True)
    
    return text, inline_kb, reply_kb

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    first_name = user.first_name or "Trader"
    text, inline_markup, reply_markup = get_welcome_content(first_name)

    # Sending text, persistent keyboard, AND inline buttons in one go
    await update.message.reply_text(
        text=text,
        reply_markup=reply_markup, # Permanent bottom button
        parse_mode="Markdown"
    )
    # Update same message to include inline buttons immediately
    await update.message.edit_reply_markup(reply_markup=inline_markup)

# ===== BUTTON HANDLER (Includes Navigation/Back Logic) =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"**{first_name}**"

    # --- Back to Home ---
    if data == "start_again":
        text, inline_markup, _ = get_welcome_content(first_name)
        await query.edit_message_text(text=text, reply_markup=inline_markup, parse_mode="Markdown")

    # --- New Here ---
    elif data == "new_here":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"👋 Welcome {bold_name}!\n\nTo get VIP access, please register using our official partner link below.",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    # --- Old Here ---
    elif data == "old_here":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"👋 Welcome back, {bold_name}!\n\nIf you need help connecting your account, please contact our support team.",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    # --- From Website ---
    elif data == "from_website":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(f"🌐 Welcome {bold_name}!\n\nPlease select your status below:", reply_markup=kb, parse_mode="Markdown")

    # --- Verification Flow ---
    elif data in ["registered", "changed_ib"]:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="from_website")]])
        msg = "✅ **Registration Received!**\n\nPlease send your **Trading Account ID** below.\n\n⏳ Verification takes **1-2 hours**."
        await query.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

# ===== MESSAGE HANDLER =====
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if user_text == "💬 LiveChat":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Chat Now ✅", url=SUPPORT_LINK)]])
        await update.message.reply_text("Contact our support for assistance:", reply_markup=kb)
    else:
        # User sending ID or other info
        await update.message.reply_text(
            f"✅ **Received!**\n\nDetail: `{user_text}`\n\nOur team will verify this shortly. Thank you!",
            parse_mode="Markdown"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
