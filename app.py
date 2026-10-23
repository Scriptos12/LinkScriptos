import telebot
from telebot import types
import os

# --- НАСТРОЙКИ ---
# Токен берется из переменной окружения FadeHost
BOT_TOKEN = os.environ.get("8829249881:AAESFtd6XcYwcH6TPj4jQYfNbvx7qgf4e-Y")

CHANNEL_1 = "@linkscriptos" 
CHANNEL_2 = "@Scriptols" 
# ----------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

SCRIPTS_DATA = {
    "scr_1": {
        "button_name": "💪 +1 Mog Evolution", 
        "text": "📜 <b>Скрипт на +1 Mog Evolution:</b>\n\n<code>loadstring(game:HttpGet(\"https://githubusercontent.com\"))()</code>"
    },
    "scr_2": {
        "button_name": "👑 Rivals (Z3US)", 
        "text": "📜 <b>Скрипт на Rivals:</b>\n\n<code>loadstring(game:HttpGet(\"https://blackowl1231/Z3US/refs/heads/main/main.lua\"))()</code>"
    },
    "scr_3": {
        "button_name": "🥚 Steal An Egg", 
        "text": "📜 <b>Скрипт на Steal An Egg (Luarmor):</b>\n\n<code>loadstring(game:HttpGet(\"https://luarmor.net\"))()</code>"
    },
    "scr_4": {
        "button_name": "⚡ Steal An Egg (Pulse)", 
        "text": "📜 <b>Второй скрипт на Steal An Egg (Pulse):</b>\n\n<code>loadstring(game:HttpGet(\"https://githubusercontent.com\"))()</code>"
    },
    "scr_5": {
        "button_name": "🏃 Evade", 
        "text": "📜 <b>Скрипт на Evade:</b>\n\n<code>loadstring(game:HttpGet(\"https://githubusercontent.com\"))()</code>"
    },
    "scr_6": {
        "button_name": "💥 Fling Thing and People", 
        "text": "📜 <b>Скрипт на Fling Thing and People:</b>\n\n<code>loadstring(game:HttpGet(\"https://dpdns.org\"))()</code>"
    },
    "scr_7": {
        "button_name": "🔨 Break and Steal An Egg", 
        "text": "📜 <b>Скрипт на Break and Steal An Egg:</b>\n\n<code>loadstring(game:HttpGet(\"https://githubusercontent.com\"))()</code>"
    },
    "scr_8": {
        "button_name": "⭐ Мой Скрипт 6.1 (LinkScripts)", 
        "text": "📜 <b>Твой скрипт LinkScripts v6.1:</b>\n\n<code>loadstring(game:HttpGet(\"https://pastebin.com\"))()</code>"
    }
}

def is_user_subscribed(user_id, channel_id):
    try:
        member = bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Ошибка проверки канала {channel_id}: {e}")
        return False

def check_all_subscriptions(user_id):
    return is_user_subscribed(user_id, CHANNEL_1) and is_user_subscribed(user_id, CHANNEL_2)

def get_sub_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    btn_sub1 = types.InlineKeyboardButton(text="📢 Подписаться на LinkScripts", url="https://t.me/linkscriptos")
    btn_sub2 = types.InlineKeyboardButton(text="📢 Подписаться на Scriptols", url="https://t.me/Scriptols")
    btn_check = types.InlineKeyboardButton(text="✅ Я подписался на оба!", callback_data="check_sub")
    keyboard.add(btn_sub1)
    keyboard.add(btn_sub2)
    keyboard.add(btn_check)
    return keyboard

def get_scripts_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key, val in SCRIPTS_DATA.items():
        btn = types.InlineKeyboardButton(text=val["button_name"], callback_data=f"get_{key}")
        keyboard.add(btn)
    return keyboard

@bot.message_handler(commands=['start'])
def start_command(message):
    if check_all_subscriptions(message.from_user.id):
        bot.send_message(
            message.chat.id, 
            "🎉 Подписка подтверждена! Выберите нужный скрипт из списка:", 
            reply_markup=get_scripts_menu()
        )
    else:
        bot.send_message(
            message.chat.id, 
            "👋 Привет! Чтобы получить доступ к базе скриптов, тебе нужно подписаться на ОБА наших канала.", 
            reply_markup=get_sub_keyboard()
        )

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def process_check_sub(call):
    if check_all_subscriptions(call.from_user.id):
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.send_message(
            call.message.chat.id, 
            "🎉 Спасибо за подписки! Вот меню со всеми скриптами. Нажимай на любой, бот выдаст лоадстринг:", 
            reply_markup=get_scripts_menu()
        )
    else:
        bot.answer_callback_query(call.id, text="❌ Вы всё еще не подписались на какой-то из каналов!", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("get_scr_"))
def process_get_script(call):
    if not check_all_subscriptions(call.from_user.id):
        bot.answer_callback_query(call.id, text="🔒 Ошибка! Похоже, вы отписались от каналов.", show_alert=True)
        return
        
    script_key = call.data.replace("get_", "")
    script_info = SCRIPTS_DATA.get(script_key)
    
    if script_info:
        try:
            bot.send_message(call.message.chat.id, script_info["text"], parse_mode="HTML")
            bot.answer_callback_query(call.id, text="Скрипт отправлен!")
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            bot.answer_callback_query(call.id, text="Ошибка отправки.", show_alert=True)
    else:
        bot.answer_callback_query(call.id, text="Ошибка: скрипт не найден.")

if __name__ == "__main__":
    print("Бот успешно запущен!")
    # remove_webhook на всякий случай, чтобы не было конфликтов при перезапуске
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
