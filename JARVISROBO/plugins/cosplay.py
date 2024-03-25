

# <============================================== IMPORTS =========================================================>
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from JARVISROBO import function
from JARVISROBO.state import state

# <=======================================================================================================>


# <================================================ FUNCTIONS =====================================================>
async def get_cosplay_data():
    cosplay_url = "https://sugoi-api.vercel.app/cosplay"
    response = await state.get(cosplay_url)
    return response.json()


async def cosplay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        data = await get_cosplay_data()
        photo_url = data.get("url")  # Corrected key: "url" instead of "cosplay_url"
        if photo_url:
            await update.message.reply_photo(photo=photo_url)
        else:
            await update.message.reply_text("Could not fetch photo URL.")
    except state.FetchError:
        await update.message.reply_text("Unable to fetch data.")


# <================================================ HANDLER =======================================================>
function(CommandHandler("cosplay", cosplay, block=False))
# <================================================ END =======================================================>
