import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

# Aapka Bot Token
TELEGRAM_BOT_TOKEN = "8926218603:AAH9YcmIRJ6hwLuvGYC-a0bQoZIKw46aC94"
SECRET_PASSWORD = "ANKIT MERA BAAP HA"

authenticated_users = set()
running_bots = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⛩️ Login to System", callback_data="ask_login")],
        [InlineKeyboardButton("📜 View Active Hosts", callback_data="list_hosts")],
        [InlineKeyboardButton("🌸 Help / Guide", callback_data="help_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "✨ **[ SYSTEM ONLINE ]** ✨\n"
        "Kon'nichiwa, Master Ankit! 🌸\n\n"
        "Welcome to the **Neo-Tokyo Python Hosting Matrix**. "
        "Type karne ki koi zaroorat nahi hai—neeche diye gaye buttons ka upyog karein! 👇"
    )
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "ask_login":
        await query.message.edit_text(
            "🔑 **Authentication Required**\n\n"
            "System unlock karne ke liye niche button dabayein:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔓 Auto-Unlock System", callback_data="auto_login")],
                                               [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )

    elif query.data == "auto_login":
        authenticated_users.add(user_id)
        await show_dashboard(query)

    elif query.data == "list_hosts":
        if user_id not in authenticated_users:
            await query.message.edit_text("🔒 Pehle system unlock karein!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]))
            return
        
        if not running_bots:
            active_text = "📭 Filhaal koi bhi `.py` script live nahi hai."
        else:
            active_text = "⚡ **Active Scripts Matrix:**\n" + "\n".join([f"• `{name}`" for name in running_bots.keys()])
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Dashboard", callback_data="dashboard")]]
        await query.message.edit_text(active_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "help_menu":
        help_text = (
            "🌸 **Neo-Tokyo Host Guide** 🌸\n\n"
            "1. **Unlock:** Button click karke access lein.\n"
            "2. **Upload:** Koi bhi `.py` file chat mein bhej dein.\n"
            "3. **Run:** Bot automatic background mein execute kar dega!"
        )
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]
        await query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data in ["main_menu", "dashboard"]:
        if user_id in authenticated_users:
            await show_dashboard(query)
        else:
            await start(update, context)

async def show_dashboard(query):
    keyboard = [
        [InlineKeyboardButton("📁 Upload .py Script", callback_data="info_upload")],
        [InlineKeyboardButton("⚡ Check Running Scripts", callback_data="list_hosts")],
        [InlineKeyboardButton("⛩️ Logout / Lock", callback_data="logout")]
    ]
    await query.message.edit_text(
        "🌟 **[ DASHBOARD UNLOCKED ]** 🌟\n"
        "Aapka system fully operational hai. Ab apni `.py` file direct yahan bhej sakte hain! 🚀",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    entered_password = " ".join(context.args) if context.args else ""

    if entered_password == SECRET_PASSWORD:
        authenticated_users.add(user_id)
        keyboard = [[InlineKeyboardButton("🌟 Open Dashboard", callback_data="dashboard")]]
        await update.message.reply_text("⛩️ **Omedetou!** Password sahi hai. System unlocked.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Sugoi... Galat password hai!")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in authenticated_users:
        keyboard = [[InlineKeyboardButton("🔓 Unlock System Now", callback_data="ask_login")]]
        await update.message.reply_text("🔒 **Access Denied!** Pehle system unlock karna hoga.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        return

    file = await update.message.document.get_file()
    file_name = update.message.document.file_name

    if not file_name.endswith('.py'):
        await update.message.reply_text("⚠️ Kripya sirf valid `.py` file hi bhejein!")
        return

    file_path = os.path.join(".", file_name)
    await file.download_to_drive(file_path)

    try:
        if file_name in running_bots:
            running_bots[file_name].terminate()

        process = subprocess.Popen(["python", file_path])
        running_bots[file_name] = process

        keyboard = [[InlineKeyboardButton("⚡ View Running Status", callback_data="list_hosts")]]
        await update.message.reply_text(
            f"🌸 **File Deployed Successfully!**\n"
            f"• File: `{file_name}`\n"
            f"• Status: `Running in background 🚀`",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id in authenticated_users:
        authenticated_users.remove(query.from_user.id)
    await start(update, context)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", login))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("Password-Protected Hosting Bot Started...")
app.run_polling()
      
