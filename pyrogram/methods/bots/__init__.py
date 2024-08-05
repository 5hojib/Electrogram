from __future__ import annotations

from .answer_callback_query import AnswerCallbackQuery
from .answer_inline_query import AnswerInlineQuery
from .answer_web_app_query import AnswerWebAppQuery
from .delete_bot_commands import DeleteBotCommands
from .get_bot_commands import GetBotCommands
from .get_bot_default_privileges import GetBotDefaultPrivileges
from .get_bot_info import GetBotInfo
from .get_chat_menu_button import GetChatMenuButton
from .get_collectible_item_info import GetCollectibleItemInfo
from .get_game_high_scores import GetGameHighScores
from .get_inline_bot_results import GetInlineBotResults
from .request_callback_answer import RequestCallbackAnswer
from .send_game import SendGame
from .send_inline_bot_result import SendInlineBotResult
from .set_bot_commands import SetBotCommands
from .set_bot_default_privileges import SetBotDefaultPrivileges
from .set_bot_info import SetBotInfo
from .set_chat_menu_button import SetChatMenuButton
from .set_game_score import SetGameScore


class Bots(
    AnswerCallbackQuery,
    AnswerInlineQuery,
    GetInlineBotResults,
    RequestCallbackAnswer,
    SendInlineBotResult,
    SendGame,
    SetGameScore,
    GetGameHighScores,
    SetBotCommands,
    GetBotCommands,
    DeleteBotCommands,
    SetBotDefaultPrivileges,
    GetBotDefaultPrivileges,
    SetBotInfo,
    GetBotInfo,
    SetChatMenuButton,
    GetChatMenuButton,
    AnswerWebAppQuery,
    GetCollectibleItemInfo,
):
    pass
