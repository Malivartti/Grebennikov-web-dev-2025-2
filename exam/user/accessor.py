from dataclasses import asdict

from sqlalchemy import select

from exam.base.base_accessor import BaseAccessor
from exam.user.models import Role, User
from exam.user.schemas import UserCreate
from exam.user.types import RoleName


class UserAccessor(BaseAccessor):
    def get_user_by_id(self, *, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_user_by_login(self, *, login: str) -> User | None:
        query = select(User).where(User.login == login)
        res = self.session.execute(query)
        return res.scalar_one_or_none()

    def create_user(self, *, user_in: UserCreate):
        user_dict = asdict(user_in)
        password = user_dict.pop("password")

        user = User(**user_dict)
        user.set_password(password)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_role_by_id(self, *, role_id: int) -> Role | None:
        return self.session.get(Role, role_id)

    def get_role_by_name(
        self,
        *,
        role_name: RoleName,
    ) -> Role | None:
        query = select(Role).where(Role.name == role_name)
        res = self.session.execute(query)
        return res.scalar_one_or_none()
