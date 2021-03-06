from mybot import router
from rocketgram import InlineKeyboard
from rocketgram import SendMessage, AnswerCallbackQuery, DeleteMessage
from rocketgram import commonfilters, ChatType, context2

from tools import get_user
from data import jinja
import re


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('language')
async def reaction_on_lang_keyboard():
    await AnswerCallbackQuery(context2.update.callback_query.query_id).send()

    user = await get_user(context2.update.callback_query.user.__dict__)
    language_code = context2.update.callback_query.data.split()[1]
    user.language = language_code
    await user.commit()

    message_text = jinja.get_template(f'{language_code}/start_message').render()
    await SendMessage(user.user_id, message_text).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/simple_inline_keyboard')
async def simple_inline_keyboard():
    """Shows how to create inline keyboard."""

    kb = InlineKeyboard()
    kb.callback("😃 Super", 'simple 1').row()
    kb.callback("🙃 Great", 'simple 2').row()
    kb.callback("🤨 Not bad", 'simple 3').row()
    kb.callback("😖 All bad", 'simple 4').row()
    kb.callback("❌ Close", 'simple close')

    await SendMessage(context2.message.user.user_id,
                      '🔹 How are you filling?',
                      reply_markup=kb.render()).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('simple')
async def reaction_on_simple_keyboard():
    """Reaction on simple keyboard."""

    variant = context2.update.callback_query.data.split()[1]

    if variant == 'close':
        await AnswerCallbackQuery(context2.update.callback_query.query_id).send()
        await DeleteMessage(context2.update.callback_query.message.chat.chat_id,
                            context2.update.callback_query.message.message_id).send()
        return

    answers = {
        '1': '🔹 Super, Ok!',
        '2': '🔹 Great, Ok!',
        '3': '🔹 Ok!',
        '4': '🔹 Sad!',

    }

    msg = answers[variant]

    await AnswerCallbackQuery(context2.update.callback_query.query_id, msg, show_alert=True).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/arranged_inline_keyboard')
async def arranged_simple_inline_keyboard():
    """Shows how to arrange inline keyboard."""

    kb = InlineKeyboard()

    for i in range(30):
        kb.callback("%s" % i, 'arranged %s' % i)

    kb.callback("❌ Close", 'arranged close')

    kb.arrange_simple(5)

    await SendMessage(context2.message.user.user_id,
                      '🔹 Select number.',
                      reply_markup=kb.render()).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('arranged')
async def reaction_on_simple_keyboard():
    """Reaction on arranged simple keyboard"""

    variant = context2.update.callback_query.data.split()[1]

    if variant == 'close':
        await AnswerCallbackQuery(context2.update.callback_query.query_id).send()
        await DeleteMessage(context2.update.callback_query.message.chat.chat_id,
                            context2.update.callback_query.message.message_id).send()
        return

    msg = '🔹 Selected: %s' % variant

    await AnswerCallbackQuery(context2.update.callback_query.query_id, msg).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/arranged_scheme_inline_keyboard')
async def arranged_simple_inline_keyboard():
    """Shows how to arrange inline keyboard by scheme."""

    kb = InlineKeyboard()

    kb.callback("⏪ Prev", 'scheme prev')
    kb.callback("✅ Do!", 'scheme do')
    kb.callback("Next ⏩", 'scheme next')

    for i in range(60):
        kb.callback("%s" % i, 'scheme %s' % i)

    kb.callback("❌ Close", 'scheme close')

    kb.arrange_scheme(3, 6, 1)

    await SendMessage(context2.message.user.user_id,
                      '🔹 Select number.',
                      reply_markup=kb.render()).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.callback('scheme')
async def reaction_on_simple_keyboard():
    """Reaction on arranged simple keyboard."""

    variant = context2.update.callback_query.data.split()[1]

    if variant == 'close':
        await AnswerCallbackQuery(context2.update.callback_query.query_id).send()
        await DeleteMessage(context2.update.callback_query.message.chat.chat_id,
                            context2.update.callback_query.message.message_id).send()
        return

    if variant == 'do':
        await AnswerCallbackQuery(context2.update.callback_query.query_id, '🔹 Doing something',
                                  show_alert=True).send()
        return

    if variant == 'prev':
        await AnswerCallbackQuery(context2.update.callback_query.query_id, '🔹 Showing previous page',
                                  show_alert=True).send()
        return

    if variant == 'next':
        await AnswerCallbackQuery(context2.update.callback_query.query_id, '🔹 Showing next page',
                                  show_alert=True).send()
        return

    msg = '🔹 Selected: %s' % variant

    await AnswerCallbackQuery(context2.update.callback_query.query_id, msg).send()
