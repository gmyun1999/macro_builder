from django.core.management.base import BaseCommand

from common.service.token.i_token_manager import ITokenManager
from user.infra.token.user_token_manager import UserTokenManager

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        token_manager: ITokenManager = UserTokenManager()
        user_access = token_manager.create_user_refresh_token(user_id='1')
        print(user_access)

