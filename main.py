import telebot
import random
import requests
import sqlite3
from bs4 import BeautifulSoup

connect = sqlite3.connect('users.db', check_same_thread=False)
cursor = connect.cursor()

def db_table_val(user_id: int, user_name: str, balance: int):
    cursor.execute('INSERT OR REPLACE INTO login (user_id, user_name, balance) VALUES (?, ?, ?)',
                   (user_id, user_name, balance))
    connect.commit() 

TOKEN = '5769001050:AAEMultrMrM1V0E_MB5Mn0sfQA_A6QYfTME'
bot = telebot.TeleBot(TOKEN)
bot.can_join_groups = True

@bot.message_handler(commands=['start'])
def help_start(message):
    bot.send_message(message.chat.id, "Ведіть запит команд, якій буде виконувати бот!")          

@bot.message_handler(commands=['id'])
def help_command(message):
    bot.send_message(message.chat.id, "Ваш ID: {test}".format(test=message.chat.id)) 

@bot.message_handler(commands=['news'])
def help_news(message):
    url='https://www.liga.net/tag/frank-valter-shtaynmayer'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find('body').find_all('a', class_='title')
    rand = random.choice(headlines)
    
    for x in rand: 
        file_head=('⚡ '+x.text.strip().replace('Штайнмайер', 'Май Тієн'))
        bot.reply_to(message, file_head)
            
    
@bot.message_handler(commands=['whoiam'])
def help_test(message):
    emp = ['Хохол', 'Байрактар', 'Байдон', 'Зєлєбобік', 'Окраинец', 'Броварска макака', 'Тернопівска хвойда', 
       'Порохобот', 'Салоїд', 'Майданутий', 'Байрактар', 'Русофоб', 'Натовец', 'Джавелін', 'Мазепонець', 'Кіця', 'Пес']
    emp_text = [
        ', що намагається воскресить Бандеру',
        ', що розробляє нову біологічну зброю',
        ', що ущемля рускоговарящего',
        ', що стріляє в Кубань',
        ', що змусив Пушилина з ДНР сісти на бутилку',
        ', що пічкає ядеркою птахів з Херосонського заповідника',
        ', що копає одеське метро',
        ', що погрожує ядеркою Росії',
        ', що викопав Чорне море',
        ', що особисто з Леніним писав Енеїду в 1917 році',
        ', що донбить бомбас-бімбас',
        ', що кожен ранок спалює російські прапори у львівських школах',
        ', що розбомбив Антонівський міст',
        ', що їсть російських немовлят на сніданок',
        ', що пришиває свастику на форму ЗСУ',
        ', що підірвав автівку Дугіни',
        ', що створив бандеро мобіль',
        ', що розробляє нано-екзоскелет у Броварській нанолабораторії',
        ', що розшатує санкцією проти Росії',
        ', що їбе путліра',
        ', що їбаше сіль',
        ', що ходить в публичну качалку',
        ', що дивиться Гей порно на українському перекладі',
        ', що підпалює петарди',
        ', що лайкає базовані українські меми'
    ]
    emp_list = emp[random.randint(0, 16)]
    emp_type = emp_text[random.randint(0, 25)]
    bot.send_message(message.chat.id, "Name: {test1}\nTitle: {test2}".format(test=message.chat.username, test1=message.from_user.first_name, test2='Ви '+emp_list+emp_type))     

def get_coin():
    pow = sqlite3.connect('users.db')
    cursorPow = pow.cursor()
    cursorPow.execute('SELECT user_name, balance FROM login')
    rows = cursorPow.fetchall()
    for row in rows:
        coin = row[1]
    return coin

@bot.message_handler(commands=['bavovna']) 
def bavovna_command(message):
    url = 'https://www.unn.com.ua/uk/search?q=%D0%B1%D0%B0%D0%B2%D0%BE%D0%B2%D0%BD%D0%B0'
    res = requests.get(url)

    rd_soup = BeautifulSoup(res.text, 'html.parser')
    bv1 = rd_soup.find_all('div', class_='b-news-search-title')
    bv2 = random.choice(bv1)

    for text_bv in bv2:
        bavov = '💣 ' + text_bv.text
        bot.reply_to(message, bavov)
      
@bot.message_handler(commands=['maicredit'])
def maicredit_command(message):
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    rn = random.randint(1,6)
   
    if rn == 1:
        bale = random.randint(15, 200)
        db_table_val(user_id=us_id, user_name=us_name, balance=get_coin() - bale)
        bot.reply_to(message, "*{name}*, ти розчарувати великий вождь! Святослав зробить пуля тобі в лоб вогонь! Ти втратив -{num} МайКредіт".format(name = message.from_user.first_name, num=bale), parse_mode="Markdown")
    
    if rn == 2:
        bale = random.randint(15, 100)
        db_table_val(user_id=us_id, user_name=us_name, balance=get_coin() - bale)
        bot.reply_to(message, "Нажаль *{name}*, твій рейтинг впав на -{num} МайКредіт".format(name = message.from_user.first_name, num=bale), parse_mode="Markdown") 
    
    if rn >= 3:
        bale = random.randint(15, 250)
        db_table_val(user_id=us_id, user_name=us_name, balance=get_coin() + bale)
        bot.reply_to(message, "Вітаю *{name}*, твій рейтинг піднявся на +{num} МайКредіт".format(name = message.from_user.first_name, num=bale), parse_mode="Markdown") 

@bot.message_handler(commands=['balance']) 
def bl_command(message):
    con = sqlite3.connect('users.db')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT user_name, balance FROM login ORDER BY balance DESC')
    rows = cursorObj.fetchall()
    balance_info = {}
    
    for row in rows:
        user_name = row[0]
        balance = row[1]
        
        # Додаємо користувача до списку з таким балансом
        if balance in balance_info:
            balance_info[balance].append(user_name)
        else:
            balance_info[balance] = [user_name]
    
    result_text = "Баланс користувачів:\n"
    
    for balance, users in balance_info.items():
        user_list = ", ".join(users)
        result_text += f"💸 Баланс {balance} МайКредіт: {user_list}\n"
    
    bot.reply_to(message, result_text)

@bot.message_handler(commands=['sneak']) 
def sneak_command(message):
    from_user_id = message.from_user.id
    from_user_name = message.from_user.first_name
    
    # Визначаємо користувача, у якого будуть вкрадені МайКредіт
    # Наприклад, можемо вибирати його випадково з бази даних
    con = sqlite3.connect('users.db')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT user_id, user_name, balance FROM login WHERE user_id != ?', (from_user_id,))
    rows = cursorObj.fetchall()
    
    if len(rows) == 0:
        bot.reply_to(message, "На жаль, немає інших користувачів для крадіжки МайКредіт.")
        return
    
    # Випадково вибираємо користувача, від якого будуть вкрадені МайКредіт
    to_user_id, to_user_name, to_user_balance = random.choice(rows)
    
    # Генеруємо випадкову подію з ймовірністю 1/3 для вкрадення МайКредіт
    if random.randint(1, 3) == 1:
        # Якщо вкрадення сталося
        stolen_amount = random.randint(1, to_user_balance)  # Вкрадемо випадкову суму з балансу користувача
        db_table_val(user_id=to_user_id, user_name=to_user_name, balance=to_user_balance - stolen_amount)
        db_table_val(user_id=from_user_id, user_name=from_user_name, balance=get_coin() + stolen_amount)
        bot.reply_to(message, f"{from_user_name} вкрав {stolen_amount} МайКредіт у {to_user_name}! 😈")
    if random.randint(1, 3) == 2:
        bot.reply_to(message, f"{from_user_name} Ти піпався, тобі зроблять великій Fisting!")
    else:
        # Якщо вкрадення не сталося
        bot.reply_to(message, f"{from_user_name}, ви намагалися вкрасти МайКредіт у {to_user_name}, але вас впіймали! 🚓")


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("Помилка: ", e)