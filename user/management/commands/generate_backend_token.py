from django.core.management.base import BaseCommand

from common.infra.token.backend_token_manager import BackendAccessToken


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        token_manager = BackendAccessToken()
        token = token_manager.create_git_action_bankend_access_token()
        print("token:")
        print(token)
