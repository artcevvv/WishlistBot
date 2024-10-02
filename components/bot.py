import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from components.database import *
from components.cfg import *
from components.keyboards import *


class PartnerUsername(StatesGroup):
    waiting_for_partner_username = State()


@dp.message_handler(commands=["start"])
async def handleStart(message: types.Message):
    user_id = message.chat.id
    user_username = message.chat.username

    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_user_id == user_id).first()

        if user:
            await message.reply(user_id)
        else:
            await message.reply(
                "Hi! I'm bot, that will simplify the way you can make wishes to the love of your life!.\n"
                "Send me '/register' command, so you can use all features with your partner!"
            )


@dp.message_handler(commands=["register"])
async def handleRegistration(message: types.Message):
    user_id = message.chat.id
    user_username = message.chat.username

    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_user_id == user_id).first()

        if user:
            hasPartner = bool(user.partner_user_name)  
            await message.reply("You are already registered!", reply_markup=menu_keyboard(hasPartner))
        else:
            # Register new user
            user = User(telegram_user_id=user_id, telegram_user_name=user_username)
            session.add(user)
            session.commit()

            await message.reply(
                "Registration successful! Choose your next action below:",
                reply_markup=menu_keyboard(hasPartner=False),
            )



@dp.message_handler(commands=["menu"])
async def menuHandler(message: types.Message):
    user_id = message.chat.id
    
    with SessionLocal() as session:
        user = session.query(User).filter(User.telegram_user_id == user_id).first()

        if user:
            hasPartner = bool(user.partner_user_name)  
            await message.reply("Choose your next action below:", reply_markup=menu_keyboard(hasPartner))


@dp.callback_query_handler(lambda c: c.data == "addwish")
async def addWishQHandler(callback_query=types.CallbackQuery):
    return


@dp.callback_query_handler(lambda c: c.data == "addpartner")
async def addPartnerQHandler(callback_query: types.CallbackQuery, state: FSMContext):
    chat_id = callback_query.message.chat.id
    original_message_id = callback_query.message.message_id
        
    await bot.edit_message_text(
        "Enter your partner Telegram username:",
        chat_id=chat_id,
        message_id=original_message_id,
        reply_markup=None,
    )

    await state.set_state(PartnerUsername.waiting_for_partner_username.state)
    logger.info(f"State set to PartnerUsername.waiting_for_partner_username for user {chat_id}")


@dp.message_handler(commands="cancel", state="*")
async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)

    if current_state is None:
        await message.reply("❓ Nothing to cancel.")

    await state.finish()
    await message.reply("✅ Operation successfully cancelled.")


@dp.message_handler(state=PartnerUsername.waiting_for_partner_username)
async def store_partner_username(message: types.Message, state: FSMContext):
    telegram_user_id = message.chat.id
    partner_username = message.text

    with SessionLocal() as session:
        user = (
            session.query(User)
            .filter(User.telegram_user_id == telegram_user_id)
            .first()
        )
        
        if user:
            user.partner_user_name = partner_username
            session.commit()
            await message.reply("✅ Partner successfully added")
        else:
            await message.reply("❌ User not found in the database.")
    
    await state.finish()
