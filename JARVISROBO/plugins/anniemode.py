

# <============================================== IMPORTS =========================================================>
import nekos
from telethon import events

from Database.mongodb.toggle_mongo import is_anniemode_on, anniemode_off, anniemode_on
from JARVISROBO import tbot
from JARVISROBO.state import state  # Import the state function

# <=======================================================================================================>

url_sfw = "https://api.waifu.pics/sfw/"

allowed_commands = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "spank",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "hTojiy",
    "wink",
    "poke",
    "dance",
    "cringe",
    "tickle",
]


# <================================================ FUNCTION =======================================================>
@tbot.on(events.NewMessage(pattern="/wallpaper"))
async def wallpaper(event):
    chat_id = event.chat_id
    anniemode_status = await is_anniemode_on(chat_id)
    if anniemode_status:
        target = "wallpaper"
        img_url = nekos.img(
            target
        )  # Replace nekos.img(target) with the correct function call
        await event.reply(file=img_url)


@tbot.on(events.NewMessage(pattern="/annieomode on"))
async def enable_anniemode(event):
    chat_id = event.chat_id
    await anniemode_on(chat_id)
    await event.reply("Anniemode has been enabled.")


@tbot.on(events.NewMessage(pattern="/anniemode off"))
async def disable_anniemode(event):
    chat_id = event.chat_id
    await anniemode_off(chat_id)
    await event.reply("Anniemode has been disabled.")


@tbot.on(events.NewMessage(pattern=r"/(?:{})".format("|".join(allowed_commands))))
async def anniemode_commands(event):
    chat_id = event.chat_id
    anniemode_status = await is_anniemode_on(chat_id)
    if anniemode_status:
        target = event.raw_text[1:].lower()  # Remove the slash before the command
        if target in allowed_commands:
            url = f"{url_sfw}{target}"

            response = await state.get(url)
            result = response.json()
            animation_url = result["url"]

            # Send animation
            await event.respond(file=animation_url)


__help__ = """
*✨ Sends fun Gifs/Images*

➥ /anniemode on : Enables fun annie mode.
➥ /anniemode off : Disables fun annie mode

» /bully: sends random bully gifs.
» /neko: sends random neko gifs.
» /wallpaper: sends random wallpapers.
» /highfive: sends random highfive gifs.
» /tickle: sends random tickle GIFs.
» /wave: sends random wave GIFs.
» /smile: sends random smile GIFs.
» /feed: sends random feeding GIFs.
» /blush: sends random blush GIFs.
» /avatar: sends random avatar stickers.
» /waifu: sends random waifu stickers.
» /kiss: sends random kissing GIFs.
» /cuddle: sends random cuddle GIFs.
» /cry: sends random cry GIFs.
» /bonk: sends random cuddle GIFs.
» /smug: sends random smug GIFs.
» /slap: sends random slap GIFs.
» /hug: get hugged or hug a user.
» /pat: pats a user or get patted.
» /spank: sends a random spank gif.
» /dance: sends a random dance gif.
» /poke: sends a random poke gif.
» /wink: sends a random wink gif.
» /bite: sends random bite GIFs.
» /handhold: sends random handhold GIFs.
"""

__mod_name__ = "Aɴɴɪᴇ"
# <================================================ END =======================================================>
