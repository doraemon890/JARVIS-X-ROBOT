# <============================================== IMPORTS =========================================================>
import html

from telegram import (
    ChatMemberAdministrator,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ChatID, ChatMemberStatus, ChatType, ParseMode
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, filters
from telegram.helpers import mention_html

from JARVISROBO import DRAGONS, function
from JARVISROBO.plugins.disable import DisableAbleCommandHandler
from JARVISROBO.plugins.helper_funcs.alternate import send_message
from JARVISROBO.plugins.helper_funcs.chat_status import (
    ADMIN_CACHE,
    check_admin,
    connection_status,
)
from JARVISROBO.plugins.helper_funcs.extraction import extract_user, extract_user_and_text
from JARVISROBO.plugins.log_channel import loggable

# <=======================================================================================================>


# <================================================ FUNCTION =======================================================>
@connection_status
@loggable
@check_admin(permission="can_promote_members", is_both=True)
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    user_id = await extract_user(message, context, args)
    await chat.get_member(user.id)

    if message.from_user.id == ChatID.ANONYMOUS_ADMIN:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴄʟɪᴄᴋ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴀᴅᴍɪɴ.",
                            callback_data=f"admin_=promote={user_id}",
                        ),
                    ],
                ],
            ),
        )

        return

    if not user_id:
        await message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ, ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ.",
        )
        return

    try:
        user_member = await chat.get_member(user_id)
    except:
        return

    if (
        user_member.status == ChatMemberStatus.ADMINISTRATOR
        or user_member.status == ChatMemberStatus.OWNER
    ):
        await message.reply_text("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
        return

    if user_id == bot.id:
        await message.reply_text(
            "» ɪ ᴄᴀɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ᴍʏsᴇʟғ, ᴍʏ ᴏᴡɴᴇʀ ᴅɪᴅɴ'ᴛ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ᴅᴏ sᴏ."
        )
        return

    # Set the same permissions as the bot - the bot can't assign higher permissions than itself!
    bot_member = await chat.get_member(bot.id)

    if isinstance(bot_member, ChatMemberAdministrator):
        try:
            await bot.promoteChatMember(
                chat.id,
                user_id,
                can_change_info=bot_member.can_change_info,
                can_post_messages=bot_member.can_post_messages,
                can_edit_messages=bot_member.can_edit_messages,
                can_delete_messages=bot_member.can_delete_messages,
                can_invite_users=bot_member.can_invite_users,
                can_restrict_members=bot_member.can_restrict_members,
                can_pin_messages=bot_member.can_pin_messages,
                can_manage_chat=bot_member.can_manage_chat,
                can_manage_video_chats=bot_member.can_manage_video_chats,
                can_manage_topics=bot_member.can_manage_topics,
            )
        except BadRequest as err:
            if err.message == "User_not_mutual_contact":
                await message.reply_text(
                    "» ᴀs ɪ ᴄᴀɴ sᴇᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ɴᴏᴛ ᴩʀᴇsᴇɴᴛ ʜᴇʀᴇ."
                )
            else:
                await message.reply_text("» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴀᴛ ᴜsᴇʀ ʙᴇғᴏʀᴇ ᴍᴇ.")
            return

    await bot.sendMessage(
        chat.id,
        f"Successfully promoted {user_member.user.first_name or user_id}!",
        parse_mode=ParseMode.HTML,
        message_thread_id=message.message_thread_id if chat.is_forum else None,
    )

    log_message = (
        f"{html.escape(chat.title)}:\n"
        "#Promoted\n"
        f"ADMIN: {mention_html(user.id, user.first_name)}\n"
        f"USER: {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@loggable
@check_admin(permission="can_promote_members", is_both=True)
async def fullpromote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    args = context.args

    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    user_id = await extract_user(message, context, args)
    await chat.get_member(user.id)

    if message.from_user.id == ChatID.ANONYMOUS_ADMIN:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴄʟɪᴄᴋ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴀᴅᴍɪɴ.",
                            callback_data=f"admin_=promote={user_id}",
                        ),
                    ],
                ],
            ),
        )

        return

    if not user_id:
        await message.reply_text(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇᴍ ᴛᴏ ʙᴇ ʀᴇғᴇʀʀɪɴɢ ᴛᴏ ᴀ ᴜsᴇʀ, ᴏʀ ᴛʜᴇ ɪᴅ sᴘᴇᴄɪғɪᴇᴅ ɪs ɪɴᴄᴏʀʀᴇᴄᴛ.",
        )
        return

    try:
        user_member = await chat.get_member(user_id)
    except:
        return

    if (
        user_member.status == ChatMemberStatus.ADMINISTRATOR
        or user_member.status == ChatMemberStatus.OWNER
    ):
        await message.reply_text("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
        return

    if user_id == bot.id:
        await message.reply_text(
            "» ɪ ᴄᴀɴ'ᴛ ᴩʀᴏᴍᴏᴛᴇ ᴍʏsᴇʟғ, ᴍʏ ᴏᴡɴᴇʀ ᴅɪᴅɴ'ᴛ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ᴅᴏ sᴏ."
        )
        return

    # Set the same permissions as the bot - the bot can't assign higher perms than itself!
    bot_member = await chat.get_member(bot.id)

    if isinstance(bot_member, ChatMemberAdministrator):
        try:
            await bot.promoteChatMember(
                chat.id,
                user_id,
                can_change_info=bot_member.can_change_info,
                can_post_messages=bot_member.can_post_messages,
                can_edit_messages=bot_member.can_edit_messages,
                can_delete_messages=bot_member.can_delete_messages,
                can_invite_users=bot_member.can_invite_users,
                can_promote_members=bot_member.can_promote_members,
                can_restrict_members=bot_member.can_restrict_members,
                can_pin_messages=bot_member.can_pin_messages,
                can_manage_chat=bot_member.can_manage_chat,
                can_manage_video_chats=bot_member.can_manage_video_chats,
                can_manage_topics=bot_member.can_manage_topics,
            )
        except BadRequest as err:
            if err.message == "User_not_mutual_contact":
                await message.reply_text(
                    "» ᴀs ɪ ᴄᴀɴ sᴇᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ɴᴏᴛ ᴩʀᴇsᴇɴᴛ ʜᴇʀᴇ."
                )
            else:
                await message.reply_text("» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴀᴛ ᴜsᴇʀ ʙᴇғᴏʀᴇ ᴍᴇ.")
            return

    await bot.sendMessage(
        chat.id,
        f"Successfully promoted {user_member.user.first_name or user_id}!",
        parse_mode=ParseMode.HTML,
        message_thread_id=message.message_thread_id if chat.is_forum else None,
    )

    log_message = (
        f"{html.escape(chat.title)}:\n"
        "#FULLPROMOTED\n"
        f"ADMIN: {mention_html(user.id, user.first_name)}\n"
        f"USER: {mention_html(user_member.user.id, user_member.user.first_name)}"
    )

    return log_message


@connection_status
@loggable
@check_admin(permission="can_promote_members", is_both=True)
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message
    user = update.effective_user

    user_id = await extract_user(message, context, args)
    await chat.get_member(user.id)

    if message.from_user.id == ChatID.ANONYMOUS_ADMIN:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click to prove admin.",
                            callback_data=f"admin_=demote={user_id}",
                        ),
                    ],
                ],
            ),
        )

        return

    if not user_id:
        await message.reply_text(
            "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !",
        )
        return

    try:
        user_member = await chat.get_member(user_id)
    except:
        return

    if user_member.status == ChatMemberStatus.OWNER:
        await message.reply_text(
            "» ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴀɴᴅ ɪ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛᴏ ᴩᴜᴛ ᴍʏsᴇʟғ ɪɴ ᴅᴀɴɢᴇʀ."
        )
        return

    if not user_member.status == ChatMemberStatus.ADMINISTRATOR:
        await message.reply_text("» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !")
        return

    if user_id == bot.id:
        await message.reply_text("» ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴍʏsᴇʟғ, ʙᴜᴛ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ.")
        return

    try:
        await bot.promote_chat_member(
            chat.id,
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=False,
            can_manage_video_chats=False,
            can_manage_topics=False,
        )

        await bot.sendMessage(
            chat.id,
            f"» sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ᴀ ᴀᴅᴍɪɴ ɪɴ <b>{chat.title}</b>ᴅᴇᴍᴏᴛᴇᴅ : <b>{mention_html(user_member.user.id, user_member.user.first_name)}</b>ᴅᴇᴍᴏᴛᴇʀ : {mention_html(user.id, user.first_name)}",
            parse_mode=ParseMode.HTML,
            message_thread_id=message.message_thread_id if chat.is_forum else None,
        )

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#ᴅᴇᴍᴏᴛᴇᴅ\n"
            f"<b>ᴅᴇᴍᴏᴛᴇʀ :</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>ᴅᴇᴍᴏᴛᴇᴅ :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message
    except BadRequest:
        await message.reply_text(
             "» ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴍᴀʏʙᴇ ɪ'ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴀᴛ"
             " ᴜsᴇʀ !",
        )
        raise


@check_admin(is_user=True)
async def refresh_admin(update, _):
    try:
        ADMIN_CACHE.pop(update.effective_chat.id)
    except KeyError:
        pass

    await update.effective_message.reply_text("» sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇғʀᴇsʜᴇᴅ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ !")


@connection_status
@check_admin(permission="can_promote_members", is_both=True)
async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    args = context.args

    chat = update.effective_chat
    message = update.effective_message

    user_id, title = await extract_user_and_text(message, context, args)

    if message.from_user.id == 1087968824:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click to prove admin.",
                            callback_data=f"admin_=title={user_id}={title}",
                        ),
                    ],
                ],
            ),
        )

        return

    try:
        user_member = await chat.get_member(user_id)
    except:
        return

    if not user_id:
        await message.reply_text(
            "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !",
        )
        return

    if user_member.status == ChatMemberStatus.OWNER:
        await message.reply_text(
            "ᴛʜɪs ᴘᴇʀsᴏɴ ᴄʀᴇᴀᴛᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴄᴀɴ ɪ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ʜɪᴍ?",
        )
        return

    if user_member.status != ChatMemberStatus.ADMINISTRATOR:
        await message.reply_text(
            "» ɪ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ᴀᴅᴍɪɴs !",
        )
        return

    if user_id == bot.id:
        await message.reply_text(
            "» ɪ ᴄᴀɴ'ᴛ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ᴍʏsᴇʟғ, ᴍʏ ᴏᴡɴᴇʀ ᴅɪᴅɴ'ᴛ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ᴅᴏ sᴏ.",
        )
        return

    if not title:
        await message.reply_text("» ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜᴀᴛ sᴇᴛᴛɪɴɢ ʙʟᴀɴᴋ ᴛɪᴛʟᴇ ᴡɪʟʟ ᴄʜᴀɴɢᴇ sᴏᴍᴇᴛʜɪɴɢ ?")
        return

    if len(title) > 16:
        await message.reply_text(
            "» ᴛʜᴇ ᴛɪᴛʟᴇ ʟᴇɴɢᴛʜ ɪs ʟᴏɴɢᴇʀ ᴛʜᴀɴ 16 ᴡᴏʀᴅs ᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀs sᴏ ᴛʀᴜɴᴄᴀᴛɪɴɢ ɪᴛ ᴛᴏ 16 ᴡᴏʀᴅs.",
        )

    try:
        await bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
    except BadRequest:
        await message.reply_text(
            "» ᴍᴀʏʙᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ɴᴏᴛ ᴩʀᴏᴍᴏᴛᴇᴅ ʙʏ ᴍᴇ ᴏʀ ᴍᴀʏʙᴇ ʏᴏᴜ sᴇɴᴛ sᴏᴍᴇᴛʜɪɴɢ ᴛʜᴀᴛ ᴄᴀɴ'ᴛ ʙᴇ sᴇᴛ ᴀs ᴛɪᴛʟᴇ."
        )
        raise

    await bot.sendMessage(
        chat.id,
        f"» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ <code>{user_member.user.first_name or user_id}</code> "
         f"ᴛᴏ <code>{html.escape(title[:16])}</code>!",
        parse_mode=ParseMode.HTML,
        message_thread_id=message.message_thread_id if chat.is_forum else None,
    )


@loggable
@check_admin(permission="can_pin_messages", is_both=True)
async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    args = context.args

    user = update.effective_user
    chat = update.effective_chat
    message = update.effective_message

    is_group = chat.type != "private" and chat.type != "channel"
    prev_message = update.effective_message.reply_to_message

    is_silent = True
    if len(args) >= 1:
        is_silent = not (
            args[0].lower() == "notify"
            or args[0].lower() == "loud"
            or args[0].lower() == "violent"
        )

    if not prev_message:
        await message.reply_text("» ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴩɪɴ ɪᴛ !")
        return

    if message.from_user.id == 1087968824:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click to prove admin.",
                            callback_data=f"admin_=pin={prev_message.message_id}={is_silent}",
                        ),
                    ],
                ],
            ),
        )

        return

    if prev_message and is_group:
        try:
            await bot.pinChatMessage(
                chat.id,
                prev_message.message_id,
                disable_notification=is_silent,
            )
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise
        log_message = (
            f"{chat.title}:\n"
             f"ᴩɪɴɴᴇᴅ-ᴀ-ᴍᴇssᴀɢᴇ\n"
            f"<b>ᴩɪɴɴᴇᴅ ʙʏ :</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message


@loggable
@check_admin(permission="can_pin_messages", is_both=True)
async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if message.from_user.id == 1087968824:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click to prove Admin.",
                            callback_data=f"admin_=unpin",
                        ),
                    ],
                ],
            ),
        )

        return

    try:
        await bot.unpinChatMessage(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        elif excp.message == "Message to unpin not found":
            await message.reply_text("» ɪ ᴄᴀɴ'ᴛ ᴜɴᴩɪɴ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ, ᴍᴀʏʙᴇ ᴛʜᴀᴛ ᴍᴇssᴀɢᴇ ɪs ᴛᴏᴏ ᴏʟᴅ ᴏʀ ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴀʟʀᴇᴀᴅʏ ᴜɴᴩɪɴɴᴇᴅ ɪᴛ.")
            return
        else:
            raise

    log_message = (
        f"{chat.title}:\n"
        f"ᴜɴᴩɪɴɴᴇᴅ-ᴀ-ᴍᴇssᴀɢᴇ\n"
        f"<b>ᴜɴᴩɪɴɴᴇᴅ ʙʏ :</b> {mention_html(user.id, html.escape(user.first_name))}"
    )

    return log_message


@loggable
@check_admin(permission="can_pin_messages", is_both=True)
async def unpinall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    admin_member = await chat.get_member(user.id)

    if message.from_user.id == 1087968824:
        await message.reply_text(
            text="ʏᴏᴜ ᴀʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Click to prove admin.",
                            callback_data=f"admin_=unpinall",
                        ),
                    ],
                ],
            ),
        )

        return
    elif not admin_member.status == ChatMemberStatus.OWNER and user.id not in DRAGONS:
        await message.reply_text("ᴏɴʟʏ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜɴᴘɪɴ ᴀʟʟ ᴍᴇssᴀɢᴇs.")
        return

    try:
        if chat.is_forum:
            await bot.unpin_all_forum_topic_messages(chat.id, message.message_thread_id)
        else:
            await bot.unpin_all_chat_messages(chat.id)
    except BadRequest as excp:
        if excp.message == "Chat_not_modified":
            pass
        else:
            raise

    log_message = (
        f"{chat.title}:\n"
        "#Unpinned_All\n"
        f"Admin: {mention_html(user.id, user.first_name)}"
    )

    return log_message


@connection_status
@check_admin(permission="can_invite_users", is_bot=True)
async def invite(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat = update.effective_chat

    if chat.username:
        await update.effective_message.reply_text(f"https://t.me/{chat.username}")
    elif chat.type in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        bot_member = await chat.get_member(bot.id)
        if (
            bot_member.can_invite_users
            if isinstance(bot_member, ChatMemberAdministrator)
            else None
        ):
            invitelink = await bot.exportChatInviteLink(chat.id)
            await update.effective_message.reply_text(invitelink)
        else:
            await update.effective_message.reply_text(
                "» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴩᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴀᴄᴄᴇss ɪɴᴠɪᴛᴇ ʟɪɴᴋs ᴛʀʏ ᴄʜᴀɴɢɪɴɢ ᴍʏ ᴘᴇʀᴍɪssɪᴏɴs!",
            )
    else:
        await update.effective_message.reply_text(
            "» ɪ ᴄᴀɴ ᴏɴʟʏ ɢɪᴠᴇ ɪɴᴠɪᴛᴇ ʟɪɴᴋs ғᴏʀ sᴜᴘᴇʀ ɢʀᴏᴜᴩs ᴀɴᴅ ᴄʜᴀɴɴᴇʟs !",
        )


@connection_status
async def adminlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    args = context.args
    bot = context.bot
    if update.effective_message.chat.type == "private":
        await send_message(
            update.effective_message, "» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴩ's ɴᴏᴛ ɪɴ ᴩᴍ."
        )
        return
    chat = update.effective_chat
    chat_id = update.effective_chat.id
    chat_name = update.effective_message.chat.title
    try:
        msg = await update.effective_message.reply_text(
            "» ғᴇᴛᴄʜɪɴɢ ᴀᴅᴍɪɴs ʟɪsᴛ...", parse_mode=ParseMode.HTML
        )
    except BadRequest:
        msg = await update.effective_message.reply_text(
            "» ғᴇᴛᴄʜɪɴɢ ᴀᴅᴍɪɴs ʟɪsᴛ...", quote=False, parse_mode=ParseMode.HTML
        )
    administrators = await bot.get_chat_administrators(chat_id)
    administrators_list = list(administrators)  # Convert to a list
    text = "「 ᴀᴅᴍɪɴs ɪɴ <b>{}</b>:".format(html.escape(update.effective_chat.title))
    bot_admin_list = []
    for admin in administrators_list:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title
        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id, html.escape(user.first_name + " " + (user.last_name or ""))
                )
            )
        if user.is_bot:
            bot_admin_list.append(name)
            administrators_list.remove(admin)
            continue
        if status == "creator":
            text += "\n\n 🥀 <b>ᴏᴡɴᴇʀ:</b>"
            text += "\n<code> ╰─➽ </code>{}\n".format(name)
            if custom_title:
                text += f"<code> ┗━ {html.escape(custom_title)}</code>\n"
    text += "\n💫 <b>ᴀᴅᴍɪɴs:</b>"
    custom_admin_list = {}
    normal_admin_list = []
    for admin in administrators_list:
        user = admin.user
        status = admin.status
        custom_title = admin.custom_title
        if user.first_name == "":
            name = "☠ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛ"
        else:
            name = "{}".format(
                mention_html(
                    user.id, html.escape(user.first_name + " " + (user.last_name or ""))
                )
            )
        if status == "administrator":
            if custom_title:
                try:
                    custom_admin_list[custom_title].append(name)
                except KeyError:
                    custom_admin_list.update({custom_title: [name]})
            else:
                normal_admin_list.append(name)
    for admin in normal_admin_list:
        text += "\n<code> • </code>{}".format(admin)
    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += "\n<code> • </code>{} | <code>{}</code>".format(
                custom_admin_list[admin_group][0], html.escape(admin_group)
            )
            custom_admin_list.pop(admin_group)
    text += "\n"
    for admin_group in custom_admin_list:
        text += "\n🚨 <code>{}</code>".format(admin_group)
        for admin in custom_admin_list[admin_group]:
            text += "\n<code> • </code>{}".format(admin)
        text += "\n"
    text += "\n🤖 <b>Bots:</b>"
    for each_bot in bot_admin_list:
        text += "\n<code> • </code>{}".format(each_bot)
    try:
        await msg.edit_text(text, parse_mode=ParseMode.HTML)
    except BadRequest:  # if the original message is deleted
        return


@loggable
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    bot = context.bot
    message = update.effective_message
    chat = update.effective_chat
    admin_user = query.from_user

    splitter = query.data.replace("admin_", "").split("=")

    if splitter[1] == "promote":
        promoter = await chat.get_member(admin_user.id)

        if (
            not (
                promoter.can_promote_members
                if isinstance(promoter, ChatMemberAdministrator)
                else None or promoter.status == ChatMemberStatus.OWNER
            )
            and admin_user.id not in DRAGONS
        ):
            await query.answer(
                "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True
            )
            return

        try:
            user_id = int(splitter[2])
        except ValueError:
            user_id = splitter[2]
            await message.edit_text(
                "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !."
            )
            return

        try:
            user_member = await chat.get_member(user_id)
        except:
            return

        if (
            user_member.status == ChatMemberStatus.ADMINISTRATOR
            or user_member.status == ChatMemberStatus.OWNER
        ):
            await message.edit_text(
                "» ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ᴀɴ ᴀᴅᴍɪɴ ʜᴇʀᴇ !"
            )
            return

        bot_member = await chat.get_member(bot.id)

        if isinstance(bot_member, ChatMemberAdministrator):
            try:
                await bot.promoteChatMember(
                    chat.id,
                    user_id,
                    can_change_info=bot_member.can_change_info,
                    can_post_messages=bot_member.can_post_messages,
                    can_edit_messages=bot_member.can_edit_messages,
                    can_delete_messages=bot_member.can_delete_messages,
                    can_invite_users=bot_member.can_invite_users,
                    can_restrict_members=bot_member.can_restrict_members,
                    can_pin_messages=bot_member.can_pin_messages,
                    can_manage_chat=bot_member.can_manage_chat,
                    can_manage_video_chats=bot_member.can_manage_video_chats,
                )
            except BadRequest as err:
                if err.message == "User_not_mutual_contact":
                    await message.edit_text(
                        "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !"
                    )
                else:
                    await message.edit_text("» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴀᴛ ᴜsᴇʀ ʙᴇғᴏʀᴇ ᴍᴇ.")
                return

        await message.edit_text(
            f"Successfully promoted <b>{user_member.user.first_name or user_id}</b>!",
            parse_mode=ParseMode.HTML,
        )
        await query.answer("Done")

        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#ᴩʀᴏᴍᴏᴛᴇᴅ\n"
            f"<b>ᴩʀᴏᴍᴏᴛᴇʀ :</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>ᴜsᴇʀ :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
        )

        return log_message

    elif splitter[1] == "demote":
        demoter = await chat.get_member(admin_user.id)

        if not (
            demoter.can_promote_members
            if isinstance(demoter, ChatMemberAdministrator)
            else None or demoter.status == ChatMemberStatus.OWNER
        ):
            await query.answer(
                "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True
            )
            return

        try:
            user_id = int(splitter[2])
        except:
            user_id = splitter[2]
            await message.edit_text(
                "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !"
            )
            return

        try:
            user_member = await chat.get_member(user_id)
        except:
            return

        if user_member.status == ChatMemberStatus.OWNER:
            await message.edit_text(
                "» ᴛʜᴀᴛ ᴜsᴇʀ ɪs ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀᴛ ᴀɴᴅ ɪ ᴅᴏɴ'ᴛ ᴡᴀɴᴛ ᴛᴏ ᴩᴜᴛ ᴍʏsᴇʟғ ɪɴ ᴅᴀɴɢᴇʀ."
            )
            return

        if not user_member.status == ChatMemberStatus.ADMINISTRATOR:
            await message.edit_text("ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴡʜᴀᴛ ᴡᴀsɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ!")
            return

        if user_id == bot.id:
            await message.edit_text(
                "» ɪ ᴄᴀɴ'ᴛ ᴅᴇᴍᴏᴛᴇ ᴍʏsᴇʟғ, ʙᴜᴛ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ɪ ᴄᴀɴ ʟᴇᴀᴠᴇ."
            )
            return

        try:
            await bot.promoteChatMember(
                chat.id,
                user_id,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            )

            await message.edit_text(
                f"Successfully demoted <b>{user_member.user.first_name or user_id}</b>!",
                parse_mode=ParseMode.HTML,
            )
            await query.answer("Done")

            log_message = (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"#ᴅᴇᴍᴏᴛᴇᴅ\n"
                f"<b>ᴅᴇᴍᴏᴛᴇʀ :</b> {mention_html(user.id, user.first_name)}\n"
                f"<b>ᴅᴇᴍᴏᴛᴇᴅ :</b> {mention_html(user_member.user.id, user_member.user.first_name)}"
            )

            return log_message
        except BadRequest:
            await message.edit_text(
               "» ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴇᴍᴏᴛᴇ ᴍᴀʏʙᴇ ɪ'ᴍ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴍᴀʏʙᴇ sᴏᴍᴇᴏɴᴇ ᴇʟsᴇ ᴩʀᴏᴍᴏᴛᴇᴅ ᴛʜᴀᴛ"
            " ᴜsᴇʀ !",
            )
            return

    elif splitter[1] == "title":
        title = splitter[3]

        admin_member = await chat.get_member(admin_user.id)

        if (
            not (
                (
                    admin_member.can_promote_members
                    if isinstance(admin_member, ChatMemberAdministrator)
                    else None
                )
                or admin_member.status == ChatMemberStatus.OWNER
            )
            and admin_user.id not in DRAGONS
        ):
            await query.answer("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!")
            return

        try:
            user_id = int(splitter[2])
        except:
            await message.edit_text(
                "» ɪ ᴅᴏɴ'ᴛ ᴋɴᴏᴡ ᴡʜᴏ's ᴛʜᴀᴛ ᴜsᴇʀ, ɴᴇᴠᴇʀ sᴇᴇɴ ʜɪᴍ ɪɴ ᴀɴʏ ᴏғ ᴛʜᴇ ᴄʜᴀᴛs ᴡʜᴇʀᴇ ɪ ᴀᴍ ᴩʀᴇsᴇɴᴛ !.",
            )
            return

        try:
            user_member = await chat.get_member(user_id)
        except:
            return

        if user_member.status == ChatMemberStatus.OWNER:
            await message.edit_text(
                "ᴛʜɪs ᴘᴇʀsᴏɴ ᴄʀᴇᴀᴛᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ, ʜᴏᴡ ᴄᴀɴ ɪ sᴇᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴛʟᴇ ғᴏʀ ʜɪᴍ?",
            )
            return

        if user_member.status != ChatMemberStatus.ADMINISTRATOR:
            await message.edit_text(
                "» ɪ ᴄᴀɴ ᴏɴʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ᴀᴅᴍɪɴs !",
            )
            return

        if user_id == bot.id:
            await message.edit_text(
                "» ɪ ᴄᴀɴ'ᴛ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ ᴍʏsᴇʟғ, ᴍʏ ᴏᴡɴᴇʀ ᴅɪᴅɴ'ᴛ ᴛᴏʟᴅ ᴍᴇ ᴛᴏ ᴅᴏ sᴏ.",
            )
            return

        if not title:
            await message.edit_text("» ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜᴀᴛ sᴇᴛᴛɪɴɢ ʙʟᴀɴᴋ ᴛɪᴛʟᴇ ᴡɪʟʟ ᴄʜᴀɴɢᴇ sᴏᴍᴇᴛʜɪɴɢ ?")
            return

        if len(title) > 16:
            await message.edit_text(
                "» ᴛʜᴇ ᴛɪᴛʟᴇ ʟᴇɴɢᴛʜ ɪs ʟᴏɴɢᴇʀ ᴛʜᴀɴ 16 ᴡᴏʀᴅs ᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀs sᴏ ᴛʀᴜɴᴄᴀᴛɪɴɢ ɪᴛ ᴛᴏ 16 ᴡᴏʀᴅs.",
            )

        try:
            await bot.setChatAdministratorCustomTitle(chat.id, user_id, title)
        except BadRequest:
            await message.edit_text(
                "ᴇɪᴛʜᴇʀ ᴛʜᴇʏ ᴀʀᴇɴ'ᴛ ᴘʀᴏᴍᴏᴛᴇᴅ ʙʏ ᴍᴇ ᴏʀ ʏᴏᴜ sᴇᴛ ᴀ ᴛɪᴛʟᴇ ᴛᴇxᴛ ᴛʜᴀᴛ ɪs ɪᴍᴘᴏssɪʙʟᴇ ᴛᴏ sᴇᴛ."
            )
            return

        await message.edit_text(
            text=f"» sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ ᴛɪᴛʟᴇ ғᴏʀ <code>{user_member.user.first_name or user_id}</code> "
           f"ᴛᴏ <code>{html.escape(title[:16])}</code>!",
            parse_mode=ParseMode.HTML,
        )

    elif splitter[1] == "pin":
        admin_member = await chat.get_member(admin_user.id)

        if (
            not (
                (
                    admin_member.can_pin_messages
                    if isinstance(admin_member, ChatMemberAdministrator)
                    else None
                )
                or admin_member.status == ChatMemberStatus.OWNER
            )
            and admin_user.id not in DRAGONS
        ):
            await query.answer(
                "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!", show_alert=True
            )
            return

        try:
            message_id = int(splitter[2])
        except:
            return

        is_silent = bool(splitter[3])
        is_group = chat.type != "private" and chat.type != "channel"

        if is_group:
            try:
                await bot.pinChatMessage(
                    chat.id,
                    message_id,
                    disable_notification=is_silent,
                )
            except BadRequest as excp:
                if excp.message == "Chat_not_modified":
                    pass
                else:
                    raise

            await message.edit_text("sᴜᴄᴄᴇssғᴜʟʟʏ ᴩɪɴɴᴇᴅ")

            log_message = (
                 f"<b>{html.escape(chat.title)}:</b>\n"
                 f"ᴩɪɴɴᴇᴅ-ᴀ-ᴍᴇssᴀɢᴇ\n"
                 f"<b>ᴩɪɴɴᴇᴅ ʙʏ :</b> {mention_html(user.id, html.escape(user.first_name))}"
            )

            return log_message

    elif splitter[1] == "unpin":
        admin_member = await chat.get_member(admin_user.id)

        if (
            not (
                (
                    admin_member.can_pin_messages
                    if isinstance(admin_member, ChatMemberAdministrator)
                    else None
                )
                or admin_member.status == ChatMemberStatus.OWNER
            )
            and admin_user.id not in DRAGONS
        ):
            await query.answer(
                "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ɴᴇᴄᴇssᴀʀʏ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜᴀᴛ!",
                show_alert=True,
            )
            return

        try:
            await bot.unpinChatMessage(chat.id)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            elif excp.message == "ᴍᴇssᴀɢᴇ_ᴛᴏ_ᴜɴᴘɪɴ_ɴᴏᴛ_ғᴏᴜɴᴅ":
                await message.edit_text("ɴᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ғᴏᴜɴᴅ")
                return
            else:
                raise

        log_message = (
             f"<b>{html.escape(chat.title)}:</b>\n"
             f"ᴜɴᴩɪɴɴᴇᴅ-ᴀ-ᴍᴇssᴀɢᴇ\n"
             f"<b>ᴜɴᴩɪɴɴᴇᴅ ʙʏ :</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

        return log_message

    elif splitter[1] == "unpinall":
        admin_member = await chat.get_member(admin_user.id)

        if (
            not admin_member.status == ChatMemberStatus.OWNER
            and admin_user.id not in DRAGONS
        ):
            await query.answer("ᴏɴʟʏ ᴄʜᴀᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜɴᴘɪɴ ᴀʟʟ ᴍᴇssᴀɢᴇs.")
            return

        try:
            if chat.is_forum:
                await bot.unpin_all_forum_topic_messages(
                    chat.id, message.message_thread_id
                )
            else:
                await bot.unpin_all_chat_messages(chat.id)
        except BadRequest as excp:
            if excp.message == "Chat_not_modified":
                pass
            else:
                raise

        await message.edit_text("ᴅᴏɴᴇ ᴜɴᴘɪɴɴɪɴɢ ᴀʟʟ ᴍᴇssᴀɢᴇs.")
        log_message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"#UNPINNED-ALL\n"
            f"<b>ADMIN:</b> {mention_html(admin_user.id, html.escape(admin_user.first_name))}"
        )

        return log_message


# <=================================================== HELP ====================================================>


__help__ = """
» /adminlist: List of admins in the chat.

➠ *Admins only:*

» /pin: Silently pins the message replied to. Add 'loud' or 'notify' to give notifications to users.

» /unpin: Unpins the currently pinned message.

» /unpinall: Unpins all the pinned messages. Works in topics too (only OWNER can do this).

» /invitelink: Get an invite link.

» /promote: Promotes the user replied to.

» /fullpromote: FullPromotes the user replied to.

» /demote: Demotes the user replied to.

» /title <Title here>: Sets a custom title for an admin that the bot promoted.

» /admincache: Force refresh the admins list.
"""

# <================================================ HANDLER =======================================================>
ADMINLIST_HANDLER = DisableAbleCommandHandler("adminlist", adminlist, block=False)

PIN_HANDLER = CommandHandler("pin", pin, filters=filters.ChatType.GROUPS, block=False)
UNPIN_HANDLER = CommandHandler(
    "unpin", unpin, filters=filters.ChatType.GROUPS, block=False
)
UNPINALL_HANDLER = CommandHandler(
    "unpinall", unpinall, filters=filters.ChatType.GROUPS, block=False
)

INVITE_HANDLER = DisableAbleCommandHandler("invitelink", invite, block=False)

PROMOTE_HANDLER = DisableAbleCommandHandler("promote", promote, block=False)
FULLPROMOTE_HANDLER = DisableAbleCommandHandler("fullpromote", fullpromote, block=False)
DEMOTE_HANDLER = DisableAbleCommandHandler("demote", demote, block=False)

SET_TITLE_HANDLER = CommandHandler("title", set_title, block=False)
ADMIN_REFRESH_HANDLER = CommandHandler(
    "admincache", refresh_admin, filters=filters.ChatType.GROUPS, block=False
)
ADMIN_CALLBACK_HANDLER = CallbackQueryHandler(
    admin_callback, block=False, pattern=r"admin_"
)

function(ADMINLIST_HANDLER)
function(PIN_HANDLER)
function(UNPIN_HANDLER)
function(UNPINALL_HANDLER)
function(INVITE_HANDLER)
function(PROMOTE_HANDLER)
function(FULLPROMOTE_HANDLER)
function(DEMOTE_HANDLER)
function(SET_TITLE_HANDLER)
function(ADMIN_REFRESH_HANDLER)
function(ADMIN_CALLBACK_HANDLER)

__mod_name__ = "ᴀᴅᴍɪɴ"
__command_list__ = [
    "adminlist",
    "admins",
    "invitelink",
    "promote",
    "demote",
    "admincache",
    "fullpromote",
    "setgpic",
    "delgpic",
]
__handlers__ = [
    ADMINLIST_HANDLER,
    PIN_HANDLER,
    UNPIN_HANDLER,
    INVITE_HANDLER,
    PROMOTE_HANDLER,
    DEMOTE_HANDLER,
    SET_TITLE_HANDLER,
    ADMIN_REFRESH_HANDLER,
]
# <================================================ END =======================================================>
