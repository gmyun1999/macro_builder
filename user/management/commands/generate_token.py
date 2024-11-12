from django.core.management.base import BaseCommand

from common.service.token.i_token_manager import ITokenManager
from user.infra.token.user_token_manager import UserTokenManager


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        token_manager: ITokenManager = UserTokenManager()
        user_refresh = token_manager.create_user_refresh_token(
            user_id="7673a900-4f76-4e8b-b740-18d8146e9a3b"
        )
        user_access = token_manager.create_user_access_token(
            user_id="7673a900-4f76-4e8b-b740-18d8146e9a3b"
        )
        print("user_refresh:")
        print(user_refresh)
        print("")
        print("")
        print("user_access:")
        print(user_access)
