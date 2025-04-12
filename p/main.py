import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 🔧 Sozlamalar
BOT_TOKEN = "7852449687:AAEr4HqTmj6wKG950XQDgpYTeZ6JzFmBEBs"
ADMIN_ID = 1520635665  # O'z Telegram ID'ingiz

# ✅ Yangi uslubda Bot yaratish
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# 🧠 Holatlar
class OrderState(StatesGroup):
    amount = State()
    name = State()
    phone = State()
    address = State()

# 🧾 Asosiy menyu
def main_menu():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="1 kg"), KeyboardButton(text="5 kg")],
        [KeyboardButton(text="10 kg"), KeyboardButton(text="🔢 O'zim yozaman")]
    ])

@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Assalomu alaykum! 🌻\nNecha kg urug' buyurtma qilmoqchisiz?", reply_markup=main_menu())
    await state.set_state(OrderState.amount)

@dp.message(OrderState.amount)
async def process_amount(message: Message, state: FSMContext):
    if message.text == "🔢 O'zim yozaman":
        await message.answer("Iltimos, kerakli miqdorni yozing. Masalan: 2.5 kg")
        return
    await state.update_data(amount=message.text)
    await message.answer("Ismingizni kiriting:")
    await state.set_state(OrderState.name)

@dp.message(OrderState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(OrderState.phone)

@dp.message(OrderState.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Manzilingiz yoki orientirni yozing:")
    await state.set_state(OrderState.address)

@dp.message(OrderState.address)
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()

    order_msg = (
        "<b>📦 Yangi buyurtma!</b>\n"
        f"🌻 <b>Miqdor:</b> {data['amount']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"📞 <b>Tel:</b> {data['phone']}\n"
        f"📍 <b>Manzil:</b> {data['address']}\n"
        f"🆔 <b>Telegram:</b> @{message.from_user.username or 'yo‘q'}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=order_msg)
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="➕ Yana buyurtma berish")]])
    await message.answer("✅ Buyurtmangiz qabul qilindi!\nTez orada bog'lanamiz.", reply_markup=markup)
    await state.clear()

@dp.message(F.text == "➕ Yana buyurtma berish")
async def repeat_order(message: Message, state: FSMContext):
    await message.answer("Yana necha kg urug' buyurtma qilmoqchisiz?", reply_markup=main_menu())
    await state.set_state(OrderState.amount)

# 🚀 Ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
