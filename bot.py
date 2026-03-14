import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN") 
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# --- Main Logic for Welcome Assets ---
def get_welcome_assets(first_name):
    bold_name = f"*{first_name}*"
    
    # 1. Welcome Text
    text = (
        f"Hey, {bold_name}!\n\n"
        "👋 *Welcome to Broker Account Guide Bot!*\n\n"
        "Here you can unlock:\n"
        "📊 *Premium XAUUSD (Gold) Signals*\n"
        "🎁 *Exclusive Gifts & Giveaways*\n"
        "💎 *Access to our VIP Trading Community*\n\n"
        "Please choose an option below to continue:"
    )
    
    # 2. Inline Buttons (Inside the message)
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ])
    
    # 3. Persistent Bottom Keyboard (Always visible)
    reply_kb = ReplyKeyboardMarkup(
        [['💬 LiveChat']], 
        resize_keyboard=True
    )
    
    return text, inline_kb, reply_kb

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if this is a fresh /start or a "Back" button click (callback)
    is_callback = update.callback_query is not None
    user = update.effective_user
    first_name = user.first_name or "Trader"
    
    text, inline_markup, reply_markup = get_welcome_assets(first_name)

    if is_callback:
        # Edit existing message (for Back button flow)
        await update.callback_query.edit_message_text(
            text=text, 
            reply_markup=inline_markup, 
            parse_mode="Markdown"
        )
    else:
        # Send new message with persistent bottom keyboard
        await update.message.reply_text(
            text=text, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )
        # Edit the SAME message to add the inline buttons immediately
        await update.message.edit_reply_markup(reply_markup=inline_markup)

# ===== BUTTON HANDLER =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"*{first_name}*"

    # --- Back to Home ---
    if data == "start_again":
        await start(update, context)

    # --- New Here ---
    elif data == "new_here":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"👋 Welcome {bold_name}!\n\nTo get VIP access, please register using our official partner link below.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    # --- Old Here ---
    elif data == "old_here":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"👋 Welcome back, {bold_name}!\n\nIf you need help connecting your account, please contact our support team.\n\n"
            "💡 *Note:* VIP benefits are only for accounts registered under our Partner Code.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    # --- From Website ---
    elif data == "from_website":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"🌐 Welcome {bold_name}!\n\nPlease select your status below so we can activate your VIP benefits:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    # --- Registered ---
    elif data == "registered":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="from_website")]])
        await query.edit_message_text(
            "✅ *Registration Received!*\n\nPlease type and send your *Trading Account ID* below.\n\n"
            "⏳ Verification usually takes *1-2 hours*.\n"
            "After verification, you will receive your VIP Access.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    # --- Changed IB ---
    elif data == "changed_ib":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="from_website")]])
        await query.edit_message_text(
            "🔁 *Partner Code Change*\n\nPlease send proof of IB change and your *Trading Account ID* below.\n\n"
            "⏳ Verification takes *1-2 hours*.",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

# ===== MESSAGE HANDLER (LiveChat & Account IDs) =====
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Check if user clicked the persistent LiveChat button
    if user_text == "💬 LiveChat":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Chat Now ✅", url=SUPPORT_LINK)]])
        await update.message.reply_text(
            "Feel free to contact our customer support for any assistance.",
            reply_markup=keyboard
        )
    else:
        # Handle account IDs
        await update.message.reply_text(
            f"✅ *Received!*\n\nYour Detail: `{user_text}`\n\nOur team will verify this shortly. Thank you!",
            parse_mode="Markdown"
        )

# ===== MAIN APPLICATION =====
def main():
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
