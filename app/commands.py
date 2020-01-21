from mybot import router
from rocketgram import commonfilters, ChatType, SendMessage
from rocketgram import context2, Message
from rocketgram import InlineKeyboard

from data import jinja
from models import User

from pprint import pprint
import datetime
from tools import get_user


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/start')
async def start_command():
    user = await get_user(context2.message.user.__dict__)

    kb = InlineKeyboard()
    kb.callback(jinja.get_template('lang/ru').render(), 'language ru')
    kb.callback(jinja.get_template('lang/en').render(), 'language en')
    kb.arrange_simple(2)

    await SendMessage(context2.message.user.user_id,
                      jinja.get_template('lang/text').render(),
                      reply_markup=kb.render()).send()


@router.handler
@commonfilters.chat_type(ChatType.private)
@commonfilters.command('/help')
def help_command():
    """Handler can also be simple function.

    But remember - in async environment you shouldn't use here hard synchronous code.

    This handler also demonstrates how to make webhook-request.

    If you use webhook executor this will be send as reply of received a webhook.
    Otherwise bot's router will fallback to send by regular call."""

    SendMessage(context2.message.user.user_id,
                "🔹 Bot's help.\n"
                "\n"
                "/start - Print welcome message.\n"
                "/help - Show this message."
                "\n"
                "\n"
                "/keyboard - Shows keyboard.\n"
                "/keyboard_location - Shows keyboard with location button.\n"
                "/keyboard_contact - Shows keyboard with contact button.\n"
                "/cancel - Removes current keyboard.\n"
                "\n"
                "/simple_inline_keyboard - Shows simple inline keyboard.\n"
                "/arranged_inline_keyboard - Shows how to arrange inline keyboard.\n"
                "/arranged_scheme_inline_keyboard - Shows how to arrange inline keyboard by scheme.\n"
                "\n"
                "/send - Shows how send files.\n"
                "\n"
                "/echo - Waiting next request in same handler.\n"
                "\n"
                "/inline - Shows how to use inline mode.\n"
                "\n"
                "/enigma - Enigma cypher machine").webhook()
