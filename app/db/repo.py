from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from sqlalchemy import distinct, select, Result, update
from .models import User, FreeQuestion, Appeal, PaidQuestion, Admin, ConsultationQuiz, Order

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
    
    async def add_quiz_data(self, cur_quiz, user_tg_id, field):
        consult_quiz = ConsultationQuiz(cur_quiz = cur_quiz, field = field, user_tg_id = user_tg_id)
        self.session.add(consult_quiz)
        await self.session.commit()
        
    async def set_field_data(self, cur_quiz, user_tg_id, field):
        stmt = update(ConsultationQuiz).where(ConsultationQuiz.user_tg_id == user_tg_id).values(field = field, cur_quiz = cur_quiz)
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def get_quiz_data(self, tg_id):
        stmt = (select(ConsultationQuiz.cur_quiz, ConsultationQuiz.field).where(ConsultationQuiz.user_tg_id == tg_id))
        quiz_data : Result = await self.session.execute(stmt)
        result = quiz_data.first()
        return result
    
    async def create_order_data(self, field, user_tg_id):
        order = Order(field = field, user_tg_id = user_tg_id)
        self.session.add(order)
        await self.session.commit()
        return order
    
    async def get_order_data(self, user_tg_id):
        stmt = (select(Order.date_change_status, Order.date_create, Order.status, Order.field).where(Order.user_tg_id == user_tg_id))
        order_data : Result = await self.session.execute(stmt)
        result = order_data.first()
        return result
    
    async def get_orders(self):
        stmt = (select(User.username, Order.status, User.tg_id).join(Order.user))
        orders : Result = await self.session.execute(stmt)
        result = orders.all()
        return result 
    
    async def add_channel(self, user_id, channel_id):
        stmt = update(Order).where(Order.user_tg_id == user_id).values(private_url = channel_id, 
                                                                       status = "access", 
                                                                       date_change_status = datetime.now())
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def get_status(self, user_id):
        stmt = select(Order.status).where(Order.user_tg_id == user_id)
        status : Result = await self.session.execute(stmt)
        result = status.scalars().first()
        return result
        
    async def get_access(self, user_id):
        if await self.get_status(user_id=user_id) == 'access':
            stmt = select(Order.private_url).where(Order.user_tg_id == user_id)
            status : Result = await self.session.execute(stmt)
            result = status.scalars().first()
            return result
        else:
            return " "
    
    async def add_payment_data(self, user_id, url_pay, doc_id):
        stmt = update(Order).where(Order.user_tg_id == user_id).values(url_pay = url_pay, 
                                                                       document_id = doc_id, 
                                                                       status = "payment", 
                                                                       date_change_status = datetime.now())
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def get_payment_data(self, user_id):
        if await self.get_status(user_id=user_id) == 'payment':
            stmt = select(Order.document_id, Order.url_pay).where(Order.user_tg_id == user_id)
            status : Result = await self.session.execute(stmt)
            result = status.first()
            return result
        else:
            return (None, None)
        
    async def set_done_doc(self, user_id, doc_id):
        stmt = update(Order).where(Order.user_tg_id == user_id).values(done_document_id = doc_id)
        await self.session.execute(stmt)
        await self.session.commit()
        
    async def get_done_doc(self, user_id):
        stmt = (select(Order.done_document_id).where(Order.user_tg_id == user_id))
        users : Result = await self.session.execute(stmt)
        return users.scalars().first()