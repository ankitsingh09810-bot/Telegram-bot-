            import os
import subprocess
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = "8926218603:AAH9YcmIRJ6hwLuvGYC-a0bQoZIKw46aC94"
SECRET_PASSWORD = "ANKIT MERA BAAP HA"

authenticated_users = set()
running_bots = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⚡ enter password / login", callback_data="ask_login")],
        [InlineKeyboardButton("📜 active hosts list", callback_data="list_hosts")],
        [InlineKeyboardButton("💡 help guide", callback_data="help_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "💻 **[ cloud matrix dashboard ]** 💻\n\n"
        "⚡ *welcome, boss ankit.*\n"
        "🔒 *status:* `secure & encrypted`\n\n"
        "👇 *select an option below:*"
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
            "🔑 **[ security gateway ]** 🔑\n\n"
            "⚠️ *system locked!* send this command in chat:\n"
            "`/login <your_password>`\n\n"
            "💡 *note:* your password message will be auto-deleted for privacy.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 back to main menu", callback_data="main_menu")]]),
            parse_mode="Markdown"
        )

    elif query.data == "list_hosts":
        if user_id not in authenticated_users:
            await query.message.edit_text(
                "❌ **[ access denied ]** ❌\n\n"
                "🔒 please login first to view hosts!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 back to menu", callback_data="main_menu")]]),
                parse_mode="Markdown"
            )
            return
        
        if not running_bots:
            active_text = "📭 **[ zero hosts ]**\n\nno python scripts running right now. upload your file! 🍃"
            keyboard = [[InlineKeyboardButton("🖥️ back to dashboard", callback_data="dashboard")]]
        else:
            active_text = "⚡ **[ running scripts matrix ]** ⚡\n\n"
            keyboard = []
            for name in running_bots.keys():
                active_text += f"• `{name}` ── `[online 🟢]`\n"
                keyboard.append([InlineKeyboardButton(f"🛑 stop {name}", callback_data=f"stop_{name}")])
            keyboard.append([InlineKeyboardButton("🖥️ back to dashboard", callback_data="dashboard")])
        
        await query.message.edit_text(active_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("stop_"):
        file_to_stop = query.data.replace("stop_", "")
        if file_to_stop in running_bots:
            try:
                running_bots[file_to_stop].terminate()
                del running_bots[file_to_stop]
                await query.message.edit_text(
                    f"✅ script **{file_to_stop}** stopped successfully!",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🖥️ back to dashboard", callback_data="dashboard")]]),
                    parse_mode="Markdown"
                )
            except Exception as e:
                await query.message.edit_text(f"⚠️ error: {str(e)}")
        else:
            await query.message.edit_text("⚠️ script is already stopped.")

    elif query.data == "help_menu":
        help_text = (
            "💡 **[ matrix guide ]** 💡\n\n"
            "1. **login:** type `/login <password>` to unlock.\n"
            "2. **privacy:** your password gets deleted automatically.\n"
            "3. **upload:** send any `.py` script directly or forwarded.\n"
            "4. **control:** stop or manage active scripts anytime."
        )
        keyboard = [[InlineKeyboardButton("🔙 back to menu", callback_data="main_menu")]]
        await query.message.edit_text(help_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data in ["main_menu", "dashboard"]:
        if user_id in authenticated_users:
            await show_dashboard(query)
        else:
            await start(update, context)

async def show_dashboard(query):
    keyboard = [
        [InlineKeyboardButton("⚡ view running hosts & stop", callback_data="list_hosts")],
        [InlineKeyboardButton("🚪 logout / lock", callback_data="logout")]
    ]
    await query.message.edit_text(
        "🌟 **[ dashboard unlocked ]** 🌟\n\n"
        "⚡ *welcome back, ankit!*\n"
        "🚀 cloud matrix is fully operational. send any `.py` script to host it!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    entered_password = " ".join(context.args) if context.args else ""

    # Auto-delete user's password message for complete privacy/hiding
    try:
        await update.message.delete()
    except Exception:
        pass

    if entered_password == SECRET_PASSWORD:
        authenticated_users.add(user_id)
        keyboard = [[InlineKeyboardButton("🌟 open dashboard", callback_data="dashboard")]]
        await update.message.reply_text(
            "🔥 **[ authentication successful ]** 🔥\n\n"
            "✨ *access granted!* system unlocked.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "❌ **[ access denied ]** ❌\n\n"
            "⚠️ wrong password! try again.",
            parse_mode="Markdown"
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in authenticated_users:
        keyboard = [[InlineKeyboardButton("🔑 unlock system", callback_data="ask_login")]]
        await update.message.reply_text(
            "🔒 **[ security lock ]** 🔒\n\n"
            "⚠️ please login first to deploy scripts!",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    document = update.message.document
    if not document or not document.file_name:
        await update.message.reply_text("⚠️ please upload a valid document file!")
        return

    file_name = document.file_name

    if not file_name.endswith('.py'):
        await update.message.reply_text("⚠️ please upload a valid `.py` python script!")
        return

    try:
        file_obj = await context.bot.get_file(document.file_id)
        file_path = os.path.abspath(file_name)
        await file_obj.download_to_drive(custom_path=file_path)

        # Auto-detect libraries and install via pip silently
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        imports = re.findall(r'^(?:import|from)\s+([a-zA-Z0-9_]+)', content, re.MULTILINE)
        standard_libs = {'os', 'sys', 'time', 'datetime', 'math', 'random', 'json', 're', 'subprocess', 'logging', 'asyncio', 'urllib', 'http', 'socket', 'threading'}
        required_packages = set(imports) - standard_libs
        
        package_mapping = {'telegram': 'python-telegram-bot', 'bs4': 'beautifulsoup4', 'cv2': 'opencv-python'}
        
        for pkg in required_packages:
            pip_name = package_mapping.get(pkg, pkg)
            try:
                subprocess.run(["pip", "install", pip_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
            except Exception:
                pass

        if file_name in running_bots:
            running_bots[file_name].terminate()

        process = subprocess.Popen(["python", file_path])
        running_bots[file_name] = process

        keyboard = [[InlineKeyboardButton("⚡ view running hosts & stop", callback_data="list_hosts")]]
        await update.message.reply_text(
            f"🚀 **[ script deployed successfully ]** 🚀\n\n"
            f"• **file:** `{file_name}`\n"
            f"• **status:** `running in background 🟢`",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ error: `{str(e)}`")

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

print("Matrix Hosting Panel Started Successfully...")
app.run_polling(drop_pending_updates=True)
                
