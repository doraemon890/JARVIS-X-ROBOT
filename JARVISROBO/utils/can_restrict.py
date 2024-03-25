# <============================================== IMPORTS =========================================================>
from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from JARVISROBO import DEV_USERS, app

# <=======================================================================================================>
BAN_STICKER = "CAACAgEAAx0Cd6nKUAACAa5mAAFOIVbzyge7HtmerENUFo3SzxAAAh4BAAJRKQ05uAj2Qobm0aUeBA"


# <================================================ FUNCTION =======================================================>
def can_restrict(func: Callable) -> Callable:
    async def non_admin(_, message: Message):
        if message.from_user.id in DEV_USERS:
            return await func(_, message)

        check = await app.get_chat_member(message.chat.id, message.from_user.id)
        if check.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text(
                "» You're not an admin, Please stay in your limits."
            )

        admin = (
            await app.get_chat_member(message.chat.id, message.from_user.id)
        ).privileges
        if admin.can_restrict_members:
            return await func(_, message)
        else:
            return await message.reply_text(
                "`You don't have permissions to restrict users in this chat."
            )

    return non_admin


# <================================================ END =======================================================>
