from models.sql_models.user_model import User
from flask_main import db


class UserAccountRepository:
    def create_user_account(self, user: User):
        res = ""
        try:
            db.session.add(user)
            db.session.commit()  # commit database changes
            res = f"{user} was successfully created."
        except:
            res = f"Error adding {user} to database."
        return res

    def get_all_users(self):
        list_of_users = User.query.all()
        for user_item in list_of_users:
            print(user_item)
        return {"users": self._build_list_of_users_response(list_of_users)}

    def _build_list_of_users_response(self, list_of_users: list[User]):
        res = {}
        count = 0
        for user_item in list_of_users:
            res[count] = user_item.toDict()
            count = count + 1
        return res
