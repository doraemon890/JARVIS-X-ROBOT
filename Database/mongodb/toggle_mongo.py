from Database.mongodb.db import *

dwelcomedb = dbname.dwelcome
nsfwdb = dbname.nsfw
anniemodedb = dbname.anniemode


async def is_dwelcome_on(chat_id: int) -> bool:
    chat = await dwelcomedb.find_one({"chat_id_toggle": chat_id})
    return not bool(chat)


async def dwelcome_on(chat_id: int):
    await dwelcomedb.delete_one({"chat_id_toggle": chat_id})


async def dwelcome_off(chat_id: int):
    await dwelcomedb.insert_one({"chat_id_toggle": chat_id})


async def is_nsfw_on(chat_id: int) -> bool:
    chat = await nsfwdb.find_one({"chat_id": chat_id})
    return chat


async def nsfw_on(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if is_nsfw:
        return
    return await nsfwdb.insert_one({"chat_id": chat_id})


async def nsfw_off(chat_id: int):
    is_nsfw = await is_nsfw_on(chat_id)
    if not is_nsfw:
        return
    return await nsfwdb.delete_one({"chat_id": chat_id})


async def is_anniemode_on(chat_id: int) -> bool:
    chat = await anniemodedb.find_one({"chat_id_toggle": chat_id})
    return not bool(chat)


async def anniemode_on(chat_id: int):
    await anniemodedb.delete_one({"chat_id_toggle": chat_id})


async def anniemode_off(chat_id: int):
    await anniemodedb.insert_one({"chat_id_toggle": chat_id})
