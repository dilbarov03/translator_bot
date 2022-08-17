import translators as ts
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

bot = telebot.TeleBot("5362541820:AAESZ1FIRtPWTXTN1kqPPX_uyTHSbeE7w0I")
word={}

def gtrans(m, tolang):
	m = m.split('\n\n ')[0]
	if len(m)<2900:
		try:
			text = ts.google(m,to_language=tolang)
		except Exception as e:
			#bot.send_message(1348219246,f"Error in gtrans function. \nInput was : {m}\n ERROR : {e}")
			print(f"xatooo \n{m}")
	else:
		text = 'Text can not be longer than 2900 characters. \n Please try with shorter one.'
	return text

def add_db(m):
	conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
	cursor = conn.cursor()
	#try:
	cursor.execute('CREATE TABLE IF NOT EXISTS user2 (id INTEGER UNIQUE)')
	#except:
	#   pass        

	try:
		cursor.execute("""INSERT INTO user2
				  VALUES (?)""", (m,)
			   )
		conn.commit()
	except:
		pass

def main_menu():
	markup = types.ReplyKeyboardRemove()
	markup = InlineKeyboardMarkup()
	markup.row_width = 3
	btn1=InlineKeyboardButton("🇬🇧 EN", callback_data="en")
	btn2=InlineKeyboardButton("🇷🇺 RU", callback_data="ru")
	btn3=InlineKeyboardButton("🇺🇿 UZ", callback_data="uz")
	btn4=InlineKeyboardButton("🇸🇦 AR", callback_data="ar")
	btn5=InlineKeyboardButton("🇹🇷 TR", callback_data="tr")
	btn6=InlineKeyboardButton("🇫🇷 FR", callback_data="fr")
	btn7=InlineKeyboardButton("🇩🇪 DE", callback_data="de")
	btn8=InlineKeyboardButton("🇮🇹 IT", callback_data="it")
	btn9=InlineKeyboardButton("🇨🇳 CN", callback_data="zh")
	btn10=InlineKeyboardButton("🇰🇷 KR", callback_data="ko")
	btn11=InlineKeyboardButton("🇯🇵 JP", callback_data="ja")

	markup.add(btn1, btn2, btn3)
	markup.add(btn4, btn5, btn6)
	markup.add(btn7, btn8, btn9)
	markup.add(btn10, btn11)
	return markup

def back_menu():
	markup = types.ReplyKeyboardRemove()
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	btn1 = InlineKeyboardButton("🔙Back", callback_data="back")
	markup.add(btn1)
	return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	bot.edit_message_reply_markup(call.from_user.id, call.message.message_id ,reply_markup=None)
	if call.data!="back":
		bot.edit_message_text(gtrans(word[call.from_user.id], call.data), call.from_user.id, call.message.message_id, reply_markup=back_menu())
	else:
		bot.edit_message_text("Choose the language below👇", call.from_user.id, call.message.message_id, reply_markup=main_menu())

@bot.message_handler(commands=['users'])
def statistika(message):
	try:
		conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
		cursor = conn.cursor()
		try:
			cursor.execute('CREATE TABLE user2 (id INTEGER UNIQUE)')
		except:
			pass

		cursor.execute("SELECT id FROM user2")
		Lusers = cursor.fetchall()
		users=[]
		count=len(Lusers)

		bot.send_message(message.chat.id, f"👥Total number of users: {count}")
	except:
		pass

@bot.message_handler(commands=['rassilka'])
def before(message):
	try:
		if message.from_user.username=="Oktamjon03":
			f=bot.send_message(message.chat.id, "Jo'natmoqchi bo'lgan habaringizni yuboring(text, rasm, video...)")
			bot.register_next_step_handler(f, rassilka)
	except:
		pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
	try:
		bot.send_message(-1001769780058, f"{message.from_user.first_name} - Google translator botdan foydalanishni boshladi")
	except:
		pass

	add_db(message.chat.id)
	bot.send_message(message.chat.id, "<b><i>👋 Hi, welcome to Google Translate Bot.\n🤖 I can help you to translate your text to 11 languages.\n📝 Just send something to translate.</i></b>", parse_mode='html')

@bot.message_handler(content_types=['text'])
def mess(message):
	word[message.chat.id]=message.text
	bot.send_message(message.chat.id, "Choose the language below👇", reply_markup=main_menu())

def rassilka(message):
	try:
		if message.text!="cancel" and message.text!="Cancel" and message.text!="ortga":
			conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
			cursor = conn.cursor()
			cursor.execute("SELECT id FROM user2")
			Lusers = cursor.fetchall()
			users=[]
			for i in Lusers:
				users.append(list(i)[0])

			for i in users:
				try:
					if message.content_type == "text":
					#text
						tex = message.html_text
						bot.send_message(i, tex, parse_mode='html')
					elif message.content_type == "photo":
					#photo
						capt = message.html_caption
						photo = message.photo[-1].file_id
						bot.send_photo(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "video":
					#video
						capt = message.html_caption
						photo = message.video.file_id
						bot.send_video(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "audio":
					#audio
						capt = message.html_caption
						photo = message.audio.file_id
						bot.send_audio(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "voice":
					#voice
						capt = message.html_caption
						photo = message.voice.file_id
						bot.send_voice(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "animation":
					#animation
						capt = message.html_caption
						photo = message.animation.file_id
						bot.send_animation(i, photo, caption=capt, parse_mode='html')
					elif message.content_type == "document":
					#document
						capt = message.html_caption
						photo = message.document.file_id
						bot.send_document(i, photo, caption=capt, parse_mode='html')
				except Exception as e:
					re=10
					pass        
	except:
		pass


bot.polling(none_stop=True)