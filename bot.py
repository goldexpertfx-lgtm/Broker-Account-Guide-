import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN")
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# ===== START FUNCTION =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, from_callback=False):
    if from_callback:
        user = update.callback_query.from_user
    else:
        user = update.message.from_user

    first_name = user.first_name or "Trader"
    bold_name = f"**𝗛𝗲𝘆, {first_name}!**"

    welcome_text = (
        f"{bold_name}\n\n"
        "👋 **Welcome to Broker Account Guide Bot!**\n\n"
        "Unlock your trading benefits:\n"
        "📊 **Premium XAUUSD (Gold) Signals**\n"
        "🎁 **Exclusive Gifts & Giveaways**\n"
        "💎 **VIP Trading Access & Community**\n\n"
        "Please choose an option below:"
    )

    # Inline buttons for welcome message
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕 New Here", callback_data='new_here')],
        [InlineKeyboardButton("🔄 Old Here", callback_data='old_here')],
        [InlineKeyboardButton("🌐 Website User", callback_data='from_website')]
    ])

    if from_callback:
        await update.callback_query.edit_message_text(
            text=welcome_text,
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            text=welcome_text,
            reply_markup=inline_kb,
            parse_mode="Markdown"
        )

# ===== BUTTON HANDLER =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"**{first_name}**"

    # --- Back to Home ---
    if data == "start_again":
        await start(update, context, from_callback=True)

    # --- New Here ---
    elif data == "new_here":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ])
        await query.edit_message_text(
            f"👋 Welcome {bold_name}!\n\n"
            "To get VIP access, please register using our official partner link below.",
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
        await query.edit_message_text(
            f"🌐 Welcome {bold_name}!\n\nPlease select your status below:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

    # --- Registered ---
    elif data == "registered":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="from_website")]])
        msg = (
            "✅ **Registration Received!**\n\n"
            "Please type and send your **Trading Account ID** below.\n"
            "⏳ Verification usually takes **1-2 hours**.\n\n"
            "Once verified, you will unlock the following VIP benefits:\n\n"
            "📊 **Premium XAUUSD (Gold) Signals**\n"
            "🎁 **Exclusive Gifts & Giveaways**\n"
            "💎 **VIP Trading Access & Community**\n\n"
            "💡 **Tip:** Keep your account ID handy to speed up verification."
        )
        await query.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

    # --- Changed IB ---
    elif data == "changed_ib":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="from_website")]])
        msg = (
            "🔁 **Partner Code Change**\n\n"
            "Please send the following to complete verification:\n"
            "📄 **Proof of IB Change**\n"
            "🆔 Your **Trading Account ID**\n"
            "⏳ Verification usually takes **1-2 hours**.\n\n"
            "After verification, you will unlock all VIP benefits:\n\n"
            "📊 **Premium XAUUSD (Gold) Signals**\n"
            "🎁 **Exclusive Gifts & Giveaways**\n"
            "💎 **VIP Trading Access & Community**"
        )
        await query.edit_message_text(msg, reply_markup=kb, parse_mode="Markdown")

# ===== MESSAGE HANDLER =====
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    first_name = update.message.from_user.first_name or "Trader"
    bold_name = f"**{first_name}**"

    if user_text == "💬 LiveChat":
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("Chat Now ✅", url=SUPPORT_LINK)]])
        await update.message.reply_text("Feel free to contact our customer support ", reply_markup=kb)
    else:
        await update.message.reply_text(
            f"✅ **Received!**\n\nDetail: `{user_text}`\n\nOur team will verify this shortly. Thank you!",
            parse_mode="Markdown"
        )

# ===== MAIN APPLICATION =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
