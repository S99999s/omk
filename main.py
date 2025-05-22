import requests
import telebot
import time
import random
from telebot import types
from gatet import Tele
import os

token = '7833360133:AAFmP1jYjsdqk8jQLccbB8ZOS04xYe9Glsg'
bot = telebot.TeleBot(token, parse_mode="HTML")
subscriber = '6832492482'
SLEEP_TIME = random.uniform(15, 40)

@bot.message_handler(commands=["start"])
def start(message):
    if not str(message.chat.id) == subscriber:
        bot.reply_to(message, "Only for KoKo Bhone Pyae Thu🙄💗")
        return
    bot.reply_to(message, "Send CC or use /chk [card]")

@bot.message_handler(commands=["chk"])
def check_card(message):
    if not str(message.chat.id) == subscriber:
        bot.reply_to(message, "Only for KoKo Bhone Pyae Thu🙄💗")
        return

    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, "Usage: /chk [card] (e.g., /chk 4193050602220331|06|2028|363)")
        return

    card = ' '.join(command_parts[1:]).strip()
    if not card or "|" not in card:
        bot.reply_to(message, "Invalid format! Use: /chk 4193050602220331|06|2028|363")
        return

    ko = bot.reply_to(message, "Checking Card...⌛").message_id

    try:
        # Get BIN info
        bin_data = requests.get(f'https://lookup.binlist.net/{card[:6]}', headers={'Accept-Version': '3'}).json()
        bank = bin_data.get('bank', {}).get('name', 'Unknown')
        cn = bin_data.get('country', {}).get('name', 'Unknown')
        emj = bin_data.get('country', {}).get('emoji', '🌐')
        scheme = bin_data.get('scheme', 'Unknown')
        typ = bin_data.get('type', 'Unknown')

        # Process payment
        gateway_response = Tele(card)
        last = str(gateway_response)

        # Determine status
        if 'success' in last or 'redirect' in last or 'Ture' in last:
            status = "✅ APPROVED (CVV LIVE)"
            result = "Charged 5$"
        elif 'security code is incorrect' in last:
            status = "✅ APPROVED (CCN LIVE)"
            result = "Bad CVV"
        elif 'Failed' in last or 'declined' in last:
            status = "❌ DECLINED"
            result = "Card Failed"
        else:
            status = "⚠️ UNKNOWN"
            result = "Check Manually"

        # Build message
        msg = f"""
💳 <b>CARD CHECKER</b> ━━━━━━━━━━━━━━
│
├ <b>Card:</b> <code>{card}</code>
├ <b>Status:</b> <b>{status}</b>
├ <b>Result:</b> <b>{result}</b>
│
├ <b>BIN Info:</b>
│  ├ <b>BIN:</b> {card[:6]} | {scheme} | {typ}
│  ├ <b>Country:</b> {cn} {emj}
│  └ <b>Bank:</b> {bank}
│
└ <b>Gateway Response:</b>
<code>{gateway_response}</code>

<b>Checked By:</b> @xosold | <b>Proxy:</b> ✅ Live
<b>Time:</b> {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=msg)

    except Exception as e:
        error_msg = f"<b>⚠️ Error Processing Card:</b>\n<code>{str(e)}</code>"
        bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=error_msg)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    if "|" in message.text:
        check_card(message)

print("Bot is running...")
bot.polling()