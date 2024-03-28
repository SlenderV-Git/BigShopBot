from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import distinct, select, Result
from .models import User, FreeQuestion, Appeal, PaidQuestion, Admin

class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_id: int, fullname : str, username : str) -> User:
        user = User(tg_id=user_id,
                    fullname = fullname,
                    username = username)
        
        self.session.add(user)
        await self.session.commit()
        return user

    async def get_user(self, user_id: int) -> User:
        return await self.session.get(User, user_id)

    async def change_user_lang(self, user_id: int, lang: str) -> User:
        user = await self.session.get(User, user_id)
        if user.lang != lang:
            user.lang = lang
            await self.session.commit()
        return user
    
    async def create_free_question(self, field : str, user_tg_id : int):
        free_question = FreeQuestion(field = field, user_tg_id = user_tg_id)
        self.session.add(free_question)
        await self.session.commit()
        return free_question
    
    async def create_appeal(self, field : str, user_tg_id : int):
        appeal = Appeal(appeal_field = field, user_tg_id = user_tg_id)
        self.session.add(appeal)
        await self.session.commit()
        return appeal
    
    async def create_paid_question(self, field : str, user_tg_id : int):
        paid_question = PaidQuestion(field = field, user_tg_id = user_tg_id)
        self.session.add(paid_question)
        await self.session.commit()
        return paid_question
    
    async def get_admins(self):
        result : Result = await self.session.execute(select(Admin.tg_id))
        names = result.scalars().all()
        return names
    
    async def get_users(self):
        result : Result = await self.session.execute(select(User.tg_id))
        names = result.scalars().all()
        return names
    
    async def get_free_req(self):
        req : Result = await self.session.execute(select(FreeQuestion.field, FreeQuestion.user_tg_id))
        return req.all()
    
    async def get_paid_req(self):
        req : Result = await self.session.execute(select(PaidQuestion.field, PaidQuestion.user_tg_id))
        return req.all()
    
    async def tech_supp_req(self):
        req : Result = await self.session.execute(select(Appeal.appeal_field, Appeal.user_tg_id))
        return req.all()
    
    async def user_reg_day(self):
        one_day_ago = datetime.now() - timedelta(days=1)
        stmt = (select(User).where(User.date_registration >= one_day_ago))
        users : Result = await self.session.execute(stmt)
        return users.scalars().all()

    async def user_reg_week(self):
        one_week_ago = datetime.now() - timedelta(weeks=1)
        stmt = (select(User).where(User.date_registration >= one_week_ago))
        users : Result = await self.session.execute(stmt)
        return users.scalars().all()

    async def user_reg_month(self):
        one_month_ago = datetime.now() - timedelta(days=30)
        stmt = (select(User).where(User.date_registration >= one_month_ago))
        users : Result = await self.session.execute(stmt)
        return users.scalars().all()
    
    async def active_users(self):
        stmt = (select(User).where(User.is_active))
        users : Result = await self.session.execute(stmt)
        return users.scalars().all()
    
    async def get_free_quest_data(self):
        result : Result = await self.session.execute(select(FreeQuestion.field))
        quest = result.scalars().all()
        return quest
    
    async def get_paid_quest_data(self):
        result : Result = await self.session.execute(select(PaidQuestion.field))
        quest = result.scalars().all()
        return quest
    
    async def get_appeal_data(self):
        result : Result = await self.session.execute(select(Appeal.appeal_field))
        quest = result.scalars().all()
        return quest