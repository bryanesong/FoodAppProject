from models.sql_models.user_model import User
from datetime import datetime
from repository.user_account_repository import UserAccountRepository


class UserAccountService:
    def create_user_account(self, uuid, username, email):
        new_user = User(
            uuid=uuid, username=username, email=email, created=datetime.now()
        )
        return UserAccountRepository().create_user_account(new_user)

    def get_all_users(self):
        return UserAccountRepository().get_all_users()
