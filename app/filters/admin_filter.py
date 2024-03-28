from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.db.repo import Repo

class IsAdmin(BaseFilter):
    async def __call__(self, message : Message, repo : Repo):
        admins = await repo.get_admins()
        return message.from_user.id in admins