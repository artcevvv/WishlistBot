from aiogram.types import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def menu_keyboard(hasPartner):
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    addWish = InlineKeyboardButton("Add wish", callback_data="addwish")

    if not hasPartner:
        addPartner = InlineKeyboardButton("Add partner", callback_data="addpartner")
        keyboard.add(addPartner)
    else:
        checkPartnerWishes = InlineKeyboardButton("Partner wishes", callback_data="partner")
        keyboard.add(checkPartnerWishes)
    
    keyboard.add(addWish)
    
    return keyboard
