import base64
import hashlib
import hmac
import os

from lab4.base.accessor import BaseAccessor
from lab4.user.models import Role, User


class UserAccessor(BaseAccessor):
    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000
        )
        storage = salt + key
        return base64.b64encode(storage).decode("utf-8")

    def verify_password(self, password: str, hashed: str) -> bool:
        storage = base64.b64decode(hashed.encode("utf-8"))
        salt = storage[:16]
        key = storage[16:]
        new_key = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, 100000
        )
        return hmac.compare_digest(new_key, key)

    def get_user_by_id(self, user_id: int) -> User:
        return self.app.db.session.get(User, user_id)

    def get_user_by_login(self, login: str) -> User | None:
        return self.app.db.session.query(User).filter_by(login=login).first()

    def get_users(self) -> list[User]:
        return self.app.db.session.query(User).all()

    def create_user(self, user_data: dict) -> User:
        error_text = "Ошибка при создании пользователя: "
        try:
            new_user = User(
                login=user_data["login"],
                password=user_data["password"],
                last_name=user_data.get("last_name", ""),
                first_name=user_data["first_name"],
                middle_name=user_data.get("middle_name"),
                role_id=user_data.get("role_id"),
            )
            self.app.db.session.add(new_user)
            self.app.db.session.commit()
        except Exception as err:
            self.app.db.session.rollback()
            raise Exception(error_text + str(err)) from err
        else:
            return new_user

    def update_user(self, user_id: int, user_updates: dict):
        error_text = "Ошибка при обновлении пользователя: "
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise Exception(error_text + "Пользователь не найден")
            
            role_id = user_updates.get("user_updates")
            if role_id:
                role = self.get_role_by_id(role_id)
                if not role:
                    raise Exception(error_text + "Роль не найдена")

            for key, value in user_updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            self.app.db.session.commit()
        except Exception as err:
            self.app.db.session.rollback()
            raise Exception(error_text + str(err)) from err

    def delete_user(self, user_id: int):
        error_text = "Ошибка при удалении пользователя: "
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise Exception(error_text + "Пользователь не найден")

            self.app.db.session.delete(user)
            self.app.db.session.commit()
        except Exception as err:
            self.app.db.session.rollback()
            raise Exception(error_text + str(err)) from err
        
    def get_role_by_id(self, role_id: int) -> Role:
        return self.app.db.session.get(Role, role_id)

    def get_roles(self) -> list[Role]:
        return self.app.db.session.query(Role).all()
    
    def create_role(self, role_data: dict) -> Role:
        error_text = "Ошибка при создании роли: "
        try:
            new_role = Role(
                name=role_data["name"],
                description=role_data["description"],
            )
            self.app.db.session.add(new_role)
            self.app.db.session.commit()
        except Exception as err:
            self.app.db.session.rollback()
            raise Exception(error_text + str(err)) from err
        else:
            return new_role