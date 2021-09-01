# Made with python3
# (C) @FayasNoushad
# Copyright permission under MIT License
# All rights reserved by FayasNoushad
# License -> https://github.com/FayasNoushad/Translator-Bot-V2/blob/main/LICENSE

import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

FayasNoushad = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT  =  """
Merhaba {}, ben bir google çevirmen telegram botuyum.
@kizilsancaksahibi tarafından yapılmıştır
"""
HELP_TEXT  =  """
- Sadece dil kodu içeren bir metin gönderin
- Ve çeviri için bir dil seçin
@kizilsancaksahibi tarafından yapılmıştır
"""
ABOUT_TEXT  =  """
- **Bot :** `𝙲𝙴𝚅İ𝚁𝙼𝙴𝙽 𝙱𝙴𝚈`
- **Yaratıcı :** [Fayas](https://t.me/kizilsancaksahibi)
- **Kanal :** [Fayas Noushad](https://telegram.me/kizilsancakbilgi)
- **Kaynak :** [Buraya tıklayın](https://t.me/kizilinsancagi)
- **Dil :** [Python3](https://python.org)
- **Kütüphane :** [Pyrogram](https://pyrogram.org)
- **Sunucu:** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/kizilinsancagi'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/kizilsancakbilgi')
        ],[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
TRANSLATE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/kizilinsancagi')
        ]]
    )
LANGUAGE_BUTTONS = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton("മലയാളം", callback_data="Malayalam"),
    InlineKeyboardButton("தமிழ்", callback_data="Tamil"),
    InlineKeyboardButton("हिन्दी", callback_data="Hindi")
    ],[
    InlineKeyboardButton("ಕನ್ನಡ", callback_data="Kannada"),
    InlineKeyboardButton("తెలుగు", callback_data="Telugu"),
    InlineKeyboardButton("मराठी", callback_data="Marathi")
    ],[
    InlineKeyboardButton("ગુજરાતી", callback_data="Gujarati"),
    InlineKeyboardButton("ଓଡ଼ିଆ", callback_data="Odia"),
    InlineKeyboardButton("বাংলা", callback_data="bn")
    ],[
    InlineKeyboardButton("ਪੰਜਾਬੀ", callback_data="Punjabi"),
    InlineKeyboardButton("فارسی", callback_data="Persian"),
    InlineKeyboardButton("English", callback_data="English")
    ],[
    InlineKeyboardButton("español", callback_data="Spanish"),
    InlineKeyboardButton("français", callback_data="French"),
    InlineKeyboardButton("русский", callback_data="Russian")
    ],[
    InlineKeyboardButton("עִברִית", callback_data="hebrew"),
    InlineKeyboardButton("العربية", callback_data="arabic")
    ]]
)

@FayasNoushad.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    elif update.data == "close":
        await update.message.delete()
    else:
        message = await update.message.edit_text("`Translating...`")
        text = update.message.reply_to_message.text
        language = update.data
        translator = Translator()
        try:
            translate = translator.translate(text, dest=language)
            translate_text = f"**Translated to {language}**"
            translate_text += f"\n\n{translate.text}"
            if len(translate_text) < 4096:
                translate_text += "\n\nMade by @kizilinsancagi"
                await message.edit_text(
                    text=translate_text,
                    disable_web_page_preview=True,
                    reply_markup=TRANSLATE_BUTTON
                )
            else:
                with BytesIO(str.encode(str(translate_text))) as translate_file:
                    translate_file.name = language + ".txt"
                    await update.reply_document(
                        document=translate_file,
                        caption="Made by @kizilsancaksahibi",
                        reply_markup=TRANSLATE_BUTTON
                    )
                await message.delete()
        except Exception as error:
            print(error)
            await message.edit_text("Something wrong. Contact @kizilsancak.")

@FayasNoushad.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@FayasNoushad.on_message(filters.private & filters.text)
async def translate(bot, update):
    await update.reply_text(
        text="Select a language below for translating",
        disable_web_page_preview=True,
        reply_markup=LANGUAGE_BUTTONS,
        quote=True
    )
    
FayasNoushad.run()
