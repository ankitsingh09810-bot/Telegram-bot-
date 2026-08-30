import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

# 🔥 Desi Bot Configuration & Credentials
TELEGRAM_BOT_TOKEN = "8926218603:AAH9YcmIRJ6hwLuvGYC-a0bQoZIKw46aC94"
SECRET_PASSWORD = "ANKIT MERA BAAP HA"

authenticated_users = set()
running_bots = {}

# 🇮🇳 Main Desi Dashboard / Start Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔥 ENTER PASSWORD / LOGIN 🔥", callback_data="ask_login")],
        [InlineKeyboardButton("⚡ ACTIVE HOSTS LIST", callback_data="list_hosts")],
        [InlineKeyboardButton("👑 DESI HELP GUIDE", callback_data="help_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🔥 **[ DESI CLOUD HOSTING PANEL ]** 🔥\n\n"
        "👑 **Ram Ram, Boss Ankit!** 👑\n\n"
        "🚀 *Welcome to the Ultimate Python Hosting Matrix.*\n"
        "🛡️ *Security:* `Password Protected`\n\n"
        "👇 *Neeche diye gaye buttons ka istemaal karein:*"
    )
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# 🎛️ Callback Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "ask_login":
        await query.message.edit_text(
            "🔑 **[ SECURITY GATEWAY ]** 🔑\n\n"
            "⚠️ System locked hai! Chat mein yeh command bhejein:\n"
            "`/login <Aapka_Password>`\n\n"
            "✨ *Example:* `/login ANKIT MERA BAAP HA`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK TO MAIN MENU", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )

    elif query.data == "list_hosts":
        if user_id not in authenticated_users:
            await query.message.edit_text(
                "❌ **[ ACCESS DENIED ]** ❌\n\n"
                "🔒 Pehle password dalkar login karein!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK TO MENU", callback_data="main_menu")]]),
                parse_mode="Markdown"
            )
            return
        
        if not running_bots:
            active_text = "📭 **[ ZERO HOSTS ]**\n\nFilhaal koi bhi Python script active nahi hai. Apni file bhejein! 🍃"
            keyboard = [[InlineKeyboardButton("🖥️ BACK TO DASHBOARD", callback_data="dashboard")]]
        else:
            active_text = "⚡ **[ RUNNING SCRIPTS MATRIX ]** ⚡\n\n"
            keyboard = []
            for name in running_bots.keys():
                active_text += f"• `{name}` ── `[ONLINE 🚀]`\n"
                keyboard.append([InlineKeyboardButton(f"🛑 STOP {name}", callback_data=f"stop_{name}")])
            keyboard.append([InlineKeyboardButton("🖥️ BACK TO DASHBOARD", callback_data="dashboard")])
        
        await query.message.edit_text(active_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("stop_"):
        file_to_stop = query.data.replace("stop_", "")
        if file_to_stop in running_bots:
            try:
                running_bots[file_to_stop].terminate()
                del running_bots[file_to_stop]
                await query.message.edit_text(
                    f"✅ Script **{file_to_stop}** ko successfully stop kar diya gaya hai!",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥️ BACK TO DASHBOARD", callback_data="dashboard")]]),
                    parse_mode="Markdown"
                )
            except Exception as e:
                await query.message.edit_text(f"⚠️ Error: {str(e)}")
        else:
            await query.message.edit_text("⚠️ Yeh script pehle se hi band hai.")

    elif query.data == "help_menu":
        help_text = (
            "👑 **[ DESI GUIDE ]** 👑\n\n"
            "1. **Login:** `/login <password>` type karke unlock karein.\n"
            "2. **Upload:** Unlocking ke baad koi bhi `.py` script chat mein bhejein (direct ya forward karke).\n"
            "3. **Control:** Active hosts menu se kisi bhi script ko kabhi bhi stop kar sakte hain!"
        )
        keyboard = [[InlineKeyboardButton("🔙 BACK TO MENU", callback_data="main_menu")]]
        await query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data in ["main_menu", "dashboard"]:
        if user_id in authenticated_users:
            await show_dashboard(query)
        else:
            await start(update, context)

# 🌟 Unlocked Dashboard UI
async def show_dashboard(query):
    keyboard = [
        [InlineKeyboardButton("⚡ VIEW RUNNING HOSTS & STOP", callback_data="list_hosts")],
        [InlineKeyboardButton("🚪 LOGOUT / LOCK", callback_data="logout")]
    ]
    await query.message.edit_text(
        "🌟 **[ DESI DASHBOARD UNLOCKED ]** 🌟\n\n"
        "👑 *Welcome, Boss Ankit!* \n"
        "🚀 Aapka cloud system poori tarah ready hai. Ab apni koi bhi `.py` script direct is chat mein upload ya forward kar dein!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# 🔐 Password Handler
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    entered_password = " ".join(context.args) if context.args else ""

    if entered_password == SECRET_PASSWORD:
        authenticated_users.add(user_id)
        keyboard = [[InlineKeyboardButton("🌟 OPEN DESI DASHBOARD", callback_data="dashboard")]]
        await update.message.reply_text(
            "🔥 **[ AUTHENTICATION SUCCESSFUL ]** 🔥\n\n"
            "👑 *Sahi hai Boss!* System unlock ho gaya hai. ✨",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ **[ ACCESS DENIED ]** ❌\n\n"
            "⚠️ Galat password hai! Sahi password ke sath dubara try karein.",
            parse_mode="Markdown"
        )

# 📂 Python Script Handler (Supports Direct & Forwarded Files)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in authenticated_users:
        keyboard = [[InlineKeyboardButton("🔑 UNLOCK SYSTEM", callback_data="ask_login")]]
        await update.message.reply_text(
            "🔒 **[ SECURITY LOCK ]** 🔒\n\n"
            "⚠️ Pehle password dalkar login karein, tabhi script run hogi!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    document = update.message.document
    if not document or not document.file_name:
        await update.message.reply_text("⚠️ Kripya valid file document upload karein!")
        return

    file_name = document.file_name

    if not file_name.endswith('.py'):
        await update.message.reply_text("⚠️ Kripya sirf valid `.py` python script hi upload karein!")
        return

    try:
        file_obj = await context.bot.get_file(document.file_id)
        file_path = os.path.abspath(file_name)
        await file_obj.download_to_drive(custom_path=file_path)

        if file_name in running_bots:
            running_bots[file_name].terminate()

        process = subprocess.Popen(["python", file_path])
        running_bots[file_name] = process

        keyboard = [[InlineKeyboardButton("⚡ VIEW RUNNING HOSTS & STOP", callback_data="list_hosts")]]
        await update.message.reply_text(
            f"🚀 **[ SCRIPT DEPLOYED SUCCESSFULLY ]** 🚀\n\n"
            f"• **File Name:** `{file_name}`\n"
            f"• **Status:** `Running in Background 🟢`",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: `{str(e)}`")

# 🔓 Logout Handler
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id in authenticated_users:
        authenticated_users.remove(query.from_user.id)
    await start(update, context)

# 🚀 App Initialization
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", login))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("Desi Hosting Matrix Started Successfully...")
app.run_polling(drop_pending_updates=True)
