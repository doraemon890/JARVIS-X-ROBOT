

# <============================================== IMPORTS =========================================================>
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from JARVISROBO import function
from JARVISROBO.state import state

# <=======================================================================================================>

DOWNLOADING_STICKER_ID = (
    "CAACAgUAAxkBAAPVZgABdwwsYQ43p3HC5oa7sgr0dxJyAAKZCQAC06xgVfO2MI3ouF1cHgQ"
)
API_URL = "https://karma-api2.vercel.app/instadl"  # Replace with your actual API URL


# <================================================ FUNCTION =======================================================>
async def instadl_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /instadl [Instagram URL]")
        return

    link = context.args[0]
    try:
        downloading_sticker = await update.message.reply_sticker(DOWNLOADING_STICKER_ID)

        # Make an asynchronous GET request to the API using httpx
        response = await state.get(API_URL, params={"url": link})
        data = response.json()

        # Check if the API request was successful
        if "content_url" in data:
            content_url = data["content_url"]

            # Determine content type from the URL
            content_type = "video" if "video" in content_url else "photo"

            # Reply with either photo or video
            if content_type == "photo":
                await update.message.reply_photo(content_url)
            elif content_type == "video":
                await update.message.reply_video(content_url)
            else:
                await update.message.reply_text("Unsupported content type.")
        else:
            await update.message.reply_text(
                "Unable to fetch content. Please check the Instagram URL or try with another Instagram link."
            )

    except Exception as e:
        print(e)
        await update.message.reply_text(
            "An error occurred while processing the request."
        )

    finally:
        await downloading_sticker.delete()


function(
    CommandHandler(["instagram", "instadl"], instadl_command_handler)
)
# <================================================ END =======================================================>
