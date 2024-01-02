from .ask import Ask
from .get_listener_matching_with_data import GetListenerMatchingWithData
from .get_listener_matching_with_identifier_pattern import GetListenerMatchingWithIdentifierPattern
from .get_many_listeners_matching_with_data import GetManyListenersMatchingWithData
from .get_many_listeners_matching_with_identifier_pattern import GetManyListenersMatchingWithIdentifierPattern
from .listen import Listen
from .register_next_step_handler import RegisterNextStepHandler
from .remove_listerner import RemoveListener
from .stop_listener import StopListener
from .stop_listening import StopListening
from .wait_for_callback_query import WaitForCallbackQuery
from .wait_for_message import WaitForMessage

class Pyromod(
    Ask,
    GetListenerMatchingWithData,
    GetListenerMatchingWithIdentifierPattern,
    GetManyListenersMatchingWithData,
    GetManyListenersMatchingWithIdentifierPattern,
    Listen,
    RegisterNextStepHandler,
    RemoveListener,
    StopListener,
    StopListening,
    WaitForCallbackQuery,
    WaitForMessage
):
    pass
