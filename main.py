import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

# 🌸 Bot Configuration & Security Credentials
TELEGRAM_BOT_TOKEN = "8926218603:AAH9YcmIRJ6hwLuvGYC-a0bQoZIKw46aC94"
SECRET_PASSWORD = "ANKIT MERA BAAP HA"

authenticated_users = set()
running_bots = {}

# ⛩️ Main Matrix Dashboard / Start Menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💎 𝙆𝙀𝙔 𝘼𝙐𝙏𝙃𝙀𝙉𝙏𝙄𝘾𝘼𝙏𝙄𝙊𝙉 💎", callback_data="ask_login")],
        [InlineKeyboardButton("📜 𝘼𝘾𝙏𝙄𝙑𝙀 𝙃𝙊𝙎𝙏𝙎 𝙈𝘼𝙏𝙍𝙄𝙓", callback_data="list_hosts")],
        [InlineKeyboardButton("⛩️ 𝘾𝙔𝘽𝙀𝙍 𝙂𝙐𝙄𝘿𝙀 / 𝙃𝙀𝙇𝙋", callback_data="help_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "✨ ── **[ 𝓝𝓔𝓞 - 𝓣𝓞𝓚𝓨𝓞  𝓗𝓞𝓢𝓣𝓘𝓝𝓖 ]** ── ✨\n\n"
        "🌸 **Kon'nichiwa, Master Ankit!** 🌸\n\n"
        "⚡ *Welcome to the Elite Python Cloud Matrix.*\n"
        "🔒 *Status:* `Secure & Protected`\n\n"
        "👇 *Neeche diye gaye interactive buttons ka upyog karein:*"
    )
    
    if update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# 🎛️ Interactive Callback Controller
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "ask_login":
        await query.message.edit_text(
            "🔑 **[ 𝓢𝓔𝓒𝓤𝓡𝓘𝓣𝓨  𝓖𝓐𝓣𝓔𝓦𝓐𝓨 ]** 🔑\n\n"
            "⚠️ *Access Restricted!* Auto-unlocking disabled.\n\n"
            "💬 *Kripya chat mein password enter karne ke liye yeh command use karein:*\n"
            "`/login <Aapka_Password>`\n\n"
            "✨ *Example:* `/login ANKIT MERA BAAP HA`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝑹𝑬𝑻𝑼𝑹𝑵 𝑻𝑶 𝑴𝑨𝑰𝑵", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )

    elif query.data == "list_hosts":
        if user_id not in authenticated_users:
            await query.message.edit_text(
                "❌ **[ 𝓐CCESS  DENIED ]** ❌\n\n"
                "🔒 Pehle password dalkar system unlock karein!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 𝑩𝑨𝑪𝑲 𝑻𝑶 𝑴𝑬𝑵𝑼", callback_data="main_menu")]]),
                parse_mode="Markdown"
            )
            return
        
        if not running_bots:
            active_text = "📭 **[ 𝓩𝓔𝓡𝓞  𝓗𝓞𝓢𝓣𝓢 ]**\n\nFilhaal koi bhi `.py` script live matrix par active nahi hai. 🍃"
        else:
            active_text = "⚡ **[ 𝓐𝘾𝓣𝙄𝙑𝙀  𝙎𝘾𝑹𝙄𝙷𝓣𝓢 ]** ⚡\n\n" + "\n".join([f"✨ `• {name}` ── `[ONLINE 🚀]`" for name in running_bots.keys()])
        
        keyboard = [[InlineKeyboardButton("🖥️ 𝑩𝑨𝑪𝑲 𝑻𝑶 𝑫𝑨𝑺𝑯𝑩𝑶𝑨𝑹𝑫", callback_data="dashboard")]]
        await query.message.edit_text(active_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "help_menu":
        help_text = (
            "🌸 **[ 𝓝𝓔𝓞 - 𝓣𝓞𝓚𝓨𝓞  𝓖𝓤𝓘𝓓𝓔 ]** 🌸\n\n"
            "1. **Unlock:** `/login <password>` command bhej kar system unlock karein.\n"
            "2. **Upload:** Unlocked dashboard ke baad apni koi bhi `.py` script chat mein bhejein.\n"
            "3. **Execution:** Bot automatic background matrix mein script run kar dega! 🚀"
        )
        keyboard = [[InlineKeyboardButton("🔙 𝑩𝑨𝑪𝑲 𝑻𝑶 𝑴𝑬𝑵𝑼", callback_data="main_menu")]]
        await query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data in ["main_menu", "dashboard"]:
        if user_id in authenticated_users:
            await show_dashboard(query)
        else:
            await start(update, context)

# 🌟 Unlocked Cyber Dashboard UI
async def show_dashboard(query):
    keyboard = [
        [InlineKeyboardButton("📁 𝓤𝓟𝓛𝓞𝓐𝓓 .𝓅𝓎 𝓢𝓒𝓡𝓘𝓟𝓣", callback_data="list_hosts")],
        [InlineKeyboardButton("⚡ 𝓥𝓘𝓔𝓝 𝓡𝓤𝓝𝓝𝓘𝓝𝓖 𝓗𝓞𝓢𝓣𝓢", callback_data="list_hosts")],
        [InlineKeyboardButton("⛩️ 𝓛𝓞𝓖𝓞𝓤𝓣 / 𝓛𝓞𝓒𝓚", callback_data="logout")]
    ]
    await query.message.edit_text(
        "🌟 **[ 𝓓𝓐𝓢𝓗𝓑𝓞𝓐𝓡𝓓  𝓤𝓝𝓛𝓞𝓒𝓚𝓔𝓓 ]** 🌟\n\n"
        "🌸 *Access Granted, Master Ankit!* \n"
        "⚡ Aapka cloud environment fully operational hai. Ab apni koi bhi `.py` script direct is chat mein upload karein! 🚀",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

# 🔐 Strict Password Authentication Handler
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    entered_password = " ".join(context.args) if context.args else ""

    if entered_password == SECRET_PASSWORD:
        authenticated_users.add(user_id)
        keyboard = [[InlineKeyboardButton("🌟 𝑶𝑷𝑬𝑵 𝑪𝒀𝑩𝑬𝑹 𝑫𝑨𝑺𝑯𝑩𝑶𝑨𝑹𝑫", callback_data="dashboard")]]
        await update.message.reply_text(
            "⛩️ **[ 𝓐𝓤𝓣𝓗𝓔𝓝𝓣𝓘CATION  𝓢𝓤𝓒𝓒𝓔𝓢𝓢𝓕𝓤𝓛 ]** ⛩️\n\n"
            "🌸 *Omedetou!* Password ekdum sahi hai. Matrix unlocked! ✨",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ **[ 𝓐𝘾𝘾𝓔𝓢𝓢  𝓡𝓔𝓥𝓞𝓚𝓔𝓓 ]** ❌\n\n"
            "⚠️ Sugoi... Galat password hai! Sahi password ke sath dubara koshish karein.",
            parse_mode="Markdown"
        )

# 📂 Python Script Compiler & Background Executor
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in authenticated_users:
        keyboard = [[InlineKeyboardButton("🔑 𝑼𝑵𝑳𝑶𝑪𝑲 𝑺𝒀𝑺𝑻𝑬𝑴", callback_data="ask_login")]]
        await update.message.reply_text(
            "🔒 **[ 𝓢𝓔𝓒𝓤𝓡𝓘𝓣𝓨  𝓑𝓡𝓔𝓐𝓚 ]** 🔒\n\n"
            "⚠️ Pehle password dalkar system unlock karein tabhi script deploy hogi!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    file = await update.message.document.get_file()
    file_name = update.message.document.file_name

    if not file_name.endswith('.py'):
        await update.message.reply_text("⚠️ **[ 𝓔𝓡𝓡𝓞𝓡 ]** Kripya sirf valid `.py` script hi upload karein!")
        return

    file_path = os.path.join(".", file_name)
    await file.download_to_drive(file_path)

    try:
        if file_name in running_bots:
            running_bots[file_name].terminate()

        process = subprocess.Popen(["python", file_path])
        running_bots[file_name] = process

        keyboard = [[InlineKeyboardButton("⚡ 𝑽𝑰𝑬𝑾 𝑳𝑰𝑽𝑬 𝑺𝑻𝑨𝑻𝑼𝑺", callback_data="list_hosts")]]
        await update.message.reply_text(
            f"🌸 **[ 𝓢𝓒𝓡𝓘𝓟𝓣  𝘿𝓔𝓟𝓛𝓞𝙔𝓔𝓓 ]** 🌸\n\n"
            f"• **File:** `{file_name}`\n"
            f"• **Status:** `Running in Background Matrix 🚀`",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ **[ 𝓔𝓡𝓡𝓞𝓡 ]** `{str(e)}`")

# 🔓 Logout & Lock Session
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.from_user.id in authenticated_users:
        authenticated_users.remove(query.from_user.id)
    await start(update, context)

# 🚀 Core Application Initialization with Conflict Protection
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("login", login))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("Neo-Tokyo Secure Hosting Matrix Started Successfully...")
app.run_polling(drop_pending_updates=True)
