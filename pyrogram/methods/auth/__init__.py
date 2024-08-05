from __future__ import annotations

from .accept_terms_of_service import AcceptTermsOfService
from .check_password import CheckPassword
from .connect import Connect
from .disconnect import Disconnect
from .get_active_sessions import GetActiveSessions
from .get_password_hint import GetPasswordHint
from .initialize import Initialize
from .log_out import LogOut
from .recover_password import RecoverPassword
from .resend_code import ResendCode
from .reset_session import ResetSession
from .reset_sessions import ResetSessions
from .send_code import SendCode
from .send_recovery_code import SendRecoveryCode
from .sign_in import SignIn
from .sign_in_bot import SignInBot
from .sign_up import SignUp
from .terminate import Terminate


class Auth(
    AcceptTermsOfService,
    CheckPassword,
    Connect,
    Disconnect,
    GetActiveSessions,
    GetPasswordHint,
    Initialize,
    LogOut,
    ResetSession,
    ResetSessions,
    RecoverPassword,
    ResendCode,
    SendCode,
    SendRecoveryCode,
    SignIn,
    SignInBot,
    SignUp,
    Terminate,
):
    pass
