import requests
import json
from bs4 import BeautifulSoup
import telebot
from telebot import types
token = "2040711572:AAGtJEVPKjvQLDE7RtH3g86qkb7Ja3CBP2o"
tb = telebot.TeleBot(token)
a = []
def send_msg(data_1,chat_id):
    dic = {}
    link = 'https://www.oriens.uz/media/posters/photo_2021-10-05_09-30-24.jpg'
    inlineBtn = types.InlineKeyboardMarkup()
    print(data_1[2]['name'])
    # for d in data_1:
    #     inlineBtn.add(telebot.types.InlineKeyboardButton(text='like', callback_data=f'{d["name"]}'))
    #     break
    # btn1 = types.InlineKeyboardButton('👍🏻',callback_data='1')
    # btn2 = types.InlineKeyboardButton('👎',callback_data='no')
    # inlineBtn.add(btn1,btn2)
    for text in data_1:
        data = f"<b>Name</b>:{text['name']}\n<b>Description</b>:{text['description']}\n<b>Published date</b>:{text['pub_date']}\n<b>Link:</b>{text['link']}\n" \
               f"{text['link_img']}"
        tb.send_photo(chat_id,link,data,parse_mode='HTML',reply_markup=inlineBtn)
with open('save.json','r',encoding="utf8") as data:
    data = json.load(data)
@tb.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
    item1 = types.KeyboardButton('🇺🇿Uzbek')
    item2 = types.KeyboardButton('🇷🇺Russian')
    item3 = types.KeyboardButton('🇺🇸English')
    markup.add(item1,item2,item3)
    tb.send_message(message.chat.id, "Assalomu aleykum!\nBotga kelibsiz\nMarhamat tilni tanlang:", reply_markup=markup)
@tb.message_handler(content_types='text')
def message_reply(message):
    markup1 = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
    for s in data['uz']:
        item = types.KeyboardButton(f'{s["name"]}')
        markup1.add(item)
    if message.text == "🇺🇿Uzbek":
        msg = tb.send_message(message.chat.id, 'O\'zbek Tili Tanlandi',reply_markup=markup1)
        tb.register_next_step_handler(msg, process_step)
        return send_msg(data['uz'], message.chat.id)

    if message.text == '🇷🇺Russian':
       msg = tb.send_message(message.chat.id,'Русский язык',reply_markup=markup1)
       tb.register_next_step_handler(msg, process_step_ru)
       return send_msg(data['ru'], message.chat.id)

    if message.text == '🇺🇸English':
       msg = tb.send_message(message.chat.id,'English',reply_markup=markup1)
       tb.register_next_step_handler(msg, process_step_en)
       return send_msg(data['en'], message.chat.id)

def process_step(message):
    chat_id = message.chat.id
    for g in data['uz']:
        if message.text == g['name']:
            kirish(g['link'],chat_id)
def process_step_ru(message):
    chat_id = message.chat.id
    for g in data['ru']:
        if message.text == g['name']:
            kirish(g['link'],chat_id)
def process_step_en(message):
    chat_id = message.chat.id
    for g in data['en']:
        if message.text == g['name']:
            kirish(g['link'],chat_id)
def kirish(link,chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton('🔙')
    markup.add(item1)
    url = str(link)
    chat_id = "702471868"
    response = requests.get(url)
    ja = []
    html = BeautifulSoup(response.content,'html.parser')
    items3 = html.select('.article')
    try:
        for item in items3:
            d = {
                'link':item.select('a')[0]['href'],
                'title':item.select('a')[0].text.strip()
            }
            ja.append(d)
        msg = tb.send_message(chat_id,'Maqolalar',parse_mode='HTML',reply_markup=markup)
        tb.register_next_step_handler(msg, restart)
        return send(ja,chat_id)
    except Exception as e:
        msg = tb.send_message(chat_id,"Maqola mavjud emas", parse_mode='HTML', reply_markup=markup)
        tb.register_next_step_handler(msg, restart)
@tb.message_handler(content_types='text')
def restart(message):
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    for s in data['uz']:
        item = types.KeyboardButton(f'{s["name"]}')
        markup1.add(item)
    if message.text == "🔙":
        msg = tb.send_message(message.chat.id, 'Marhamat kerakli maqolani tanlang', reply_markup=markup1)
        tb.register_next_step_handler(msg, process_step)

    if message.text == 'Russian':
        msg = tb.send_message(message.chat.id, 'Rus tili tanlandi', reply_markup=markup1)
        tb.register_next_step_handler(msg, process_step_ru)
def send(data,id):
    for d in data:
        tb.send_message(id,f"name:{d['title']}\nlink:{'https://www.oriens.uz'+d['link']}",parse_mode='HTML')
@tb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    pass
    # d = {}
    # a = []
    # c = {call.message.caption}
    # d = json.loads(c)
    # print(type(d))
    # if call.data == 'yes':
    #     d['article'] = call.message.caption
    #     d['result'] = 1
    #     with open('results.json', 'w', encoding='utf-8') as f:
    #         (json.dump(d, f, ensure_ascii=False, indent=4))
tb.polling()