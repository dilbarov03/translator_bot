from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import translators as ts

TOKEN = ""

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    rassilka = State()
word = {}


def gtrans(m, tolang):
    m = m.split('\n\n ')[0]
    text = ""
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
    btn1=InlineKeyboardButton("🇬🇧EN", callback_data="en")
    btn2=InlineKeyboardButton("🇷🇺RU", callback_data="ru")
    btn3=InlineKeyboardButton("🇺🇿UZ", callback_data="uz")
    btn4=InlineKeyboardButton("🇸🇦AR", callback_data="ar")
    btn5=InlineKeyboardButton("🇹🇷TR", callback_data="tr")
    btn6=InlineKeyboardButton("🇫🇷FR", callback_data="fr")
    btn7=InlineKeyboardButton("🇩🇪DE", callback_data="de")
    btn8=InlineKeyboardButton("🇮🇹IT", callback_data="it")
    btn9=InlineKeyboardButton("🇨🇳CN", callback_data="zh")
    btn10=InlineKeyboardButton("🇰🇷KR", callback_data="ko")
    btn11=InlineKeyboardButton("🇯🇵JP", callback_data="ja")

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



@dp.callback_query_handler()
async def callback_query(call):
    await bot.edit_message_reply_markup(call.from_user.id, call.message.message_id ,reply_markup=None)
    if call.data!="back":
        await bot.edit_message_text(gtrans(word[call.from_user.id], call.data), call.from_user.id, call.message.message_id, reply_markup=back_menu())
    else:
        await bot.edit_message_text("Choose the language below👇", call.from_user.id, call.message.message_id, reply_markup=main_menu())


@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    add_db(message.chat.id)
    await bot.send_message(message.chat.id, "<b><i>👋Hi, welcome to Google Translate Bot.\n🤖I can help you to translate your text to 11 languages.\n📝Just send something to translate.</i></b>", parse_mode='html')


@dp.message_handler(commands=["stats"])
async def send_status(message: types.Message):
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

        await bot.send_message(message.chat.id, f"👥Total number of users: {count}")
    except:
        pass

@dp.message_handler(commands=["rassilka"], state="*")
async def rassilka(message: types.Message, state: FSMContext):
    if message.from_user.username=="Young_Proger" or message.from_user.username=="Oktamjon_03":
        await bot.send_message(message.chat.id, "Jo'natmoqchi bo'lgan habaringizni yuboring(text, rasm, video...)")
        await Form.rassilka.set()


@dp.message_handler(state=Form.rassilka, content_types=["text", "photo", "video", "audio", "voice", "animation", "document", "video_note"])
async def send_messages(message: types.Message, state: FSMContext):
    if message.text in ["Cancel", "cancel", "ortga"]:
        await state.finish()
        await message.reply("Canceled")
        return
    else:
        conn = sqlite3.connect("mydata7.db") # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user2")
        Lusers = cursor.fetchall()
        users=[]
        for i in Lusers:
            users.append(list(i)[0])
        exeption_data = dict()
        for user in users:
            exeption = await send_rassilka(message, user)
            if exeption:
                if str(exeption) not in exeption_data:
                    exeption_data[str(exeption)] = 1
                else:
                    exeption_data[str(exeption)] += 1
        msg = []
        for exeption_text, number in exeption_data.items():
            msg.append(f"{exeption_text}:  {number}")
        if len(msg) != 0:
            await bot.send_message(message.chat.id, "\n".join(msg))    #sent the falty users


async def send_rassilka(message, i):
    try:
        caption_entities = message.caption_entities
        entities = message.entities
        if message.content_type == "text":
            # text
            tex = message.text
            await bot.send_message(i, tex, entities=entities)
        elif message.content_type == "photo":
            # photo
            capt = message.caption
            photo = message.photo[-1].file_id
            await bot.send_photo(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "video":
            # video
            capt = message.caption
            photo = message.video.file_id
            await bot.send_video(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "audio":
            # audio
            capt = message.caption
            photo = message.audio.file_id
            await bot.send_audio(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "voice":
            # voice
            capt = message.caption
            photo = message.voice.file_id
            await bot.send_voice(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "animation":
            # animation
            capt = message.caption
            photo = message.animation.file_id
            await bot.send_animation(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "document":
            # document
            capt = message.caption
            photo = message.document.file_id
            await bot.send_document(i, photo, caption=capt, caption_entities=caption_entities)
        elif message.content_type == "video_note":
            # rounded video
            video = message.video_note.file_id
            await bot.send_video_note(i, video)
        return
    except Exception as e:
        return e




@dp.message_handler(content_types=["text"])
async def mess(message: types.Message):
    word[message.chat.id] = message.text
    await bot.send_message(message.chat.id, "Choose the language below👇", reply_markup=main_menu())


if __name__ == '__main__':
    executor.start_polling(dp)
