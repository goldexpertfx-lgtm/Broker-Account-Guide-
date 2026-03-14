import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
TOKEN = os.environ.get("BOT_TOKEN")  # Render ya Hosting environment mein token set karein
PARTNER_LINK = "https://www.brokeraccountguide.com/"
SUPPORT_LINK = "https://t.me/MuhammadPrince7"

# --- Helper function for Main Menu ---
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

# ===== START COMMAND =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name or "Trader"
    text, reply_markup = get_welcome_content(first_name)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# ===== BUTTON HANDLER =====
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    first_name = query.from_user.first_name or "Trader"
    bold_name = f"*{first_name}*"

    # Main Menu / Back
    if data == "start_again":
        text, reply_markup = get_welcome_content(first_name)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    # New Here
    elif data == "new_here":
        keyboard = [
            [InlineKeyboardButton("🚀 Join Now", url=PARTNER_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"👋 Welcome {bold_name}!\n\n"
            "To get VIP access, you must register using our official partner link below.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Old Here
    elif data == "old_here":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Now", url=SUPPORT_LINK)],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"👋 Welcome back, {bold_name}!\n\n"
            "If you already have an account but need help connecting it with our Partner Code, contact our support team.\n\n"
            "💡 *Note:* VIP benefits only work for accounts registered using our Partner Code.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # From Website Menu
    elif data == "from_website":
        keyboard = [
            [InlineKeyboardButton("✅ Registered", callback_data="registered")],
            [InlineKeyboardButton("🔁 Changed IB", callback_data="changed_ib")],
            [InlineKeyboardButton("🔙 Back", callback_data="start_again")]
        ]
        await query.edit_message_text(
            f"🌐 Welcome {bold_name}!\n\nPlease select the correct option below:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # Registered (LiveChat link is inside text now)
    elif data == "registered":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text(
            "✅ *Registration Received!*\n\n"
            "Please type and send your *Trading Account ID* below.\n\n"
            f"💡 *Need Help?* [Chat Now ✅]({SUPPORT_LINK})\n\n"
            "⏳ Verification usually takes *1-2 hours*.\n"
            "After verification, you will receive your VIP Access.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    # Changed IB
    elif data == "changed_ib":
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="from_website")]]
        await query.edit_message_text(
            "🔁 *Partner Code Change*\n\n"
            "Please send:\n"
            "📄 *Proof of IB Change*\n"
            "🆔 Your *Trading Account ID*\n\n"
            "⏳ Verification usually takes *1-2 hours*.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

# ===== HANDLE USER MESSAGES (ID/Proof) =====
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Aap is message ko mazeed customize kar sakte hain
    await update.message.reply_text(
        f"✅ *Received!*\n\n"
        f"Your detail: `{user_text}`\n\n"
        "Our team will verify this shortly. Thank you!",
        parse_mode="Markdown"
    )

# ===== MAIN APPLICATION =====
def main():
    if not TOKEN:
        print("Error: BOT_TOKEN environment variable nahi mila!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
