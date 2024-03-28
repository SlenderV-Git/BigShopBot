from sqlalchemy import Column, BigInteger, String, DATE, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    
    tg_id = Column(BigInteger, primary_key=True)
    lang = Column(String(2), default="ru")
    fullname = Column(String)
    username = Column(String)
    is_active = Column(Boolean, default=True)
    date_registration = Column(DATE, default=func.current_date())
    orders = relationship("Order", back_populates="user")
    appeals = relationship("Appeal", back_populates="user")
    questions = relationship("FreeQuestion", back_populates="user")
    paid_questions = relationship("PaidQuestion", back_populates="user")
    purchases = relationship("CoursePurchase", back_populates="user")

class ConsultationQuiz(Base):
    __tablename__ = "consultation_quiz"

    cur_quiz = Column(BigInteger, default= 0)
    field = Column(String, default=" ")
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"), primary_key=True)
    
class Order(Base):
    __tablename__ = "orders"
    
    oder_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_create = Column(DATE, default=func.current_date())
    date_change_status = Column(DATE, default=func.current_date())
    status = Column(String, default="Create")
    field = Column(String)
    document_id = Column(String)
    done_document_id = Column(String)
    url_pay = Column(String)
    private_url = Column(String)
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    user = relationship("User", back_populates="orders")
    
class Admin(Base):
    __tablename__ = "admin"
    
    admin_id = Column(BigInteger, autoincrement=True, primary_key=True)
    tg_id = Column(BigInteger, primary_key=True)
    
class Appeal(Base):
    __tablename__ = "appeal"
    
    appeal_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_create = Column(DATE, default=func.current_date())
    appeal_field = Column(String)
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    user = relationship("User", back_populates="appeals")
    
class Course(Base):
    __tablename__ = "course"
    
    course_id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String, nullable=False)
    cost = Column(BigInteger)

class CoursePurchase(Base):
    __tablename__ = "cource_purchases"
    
    purchase_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_create = Column(DATE, default=func.current_date)
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    user = relationship("User", back_populates="purchases")
    
    
class FreeQuestion(Base):
    __tablename__ = "free_question"
    
    question_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_create = Column(DATE, default=func.current_date())
    field = Column(String)
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    user = relationship("User", back_populates="questions")
    
class PaidQuestion(Base):
    __tablename__ = "paid_question"
    
    paid_question_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_create = Column(DATE, default=func.current_date())
    field = Column(String)
    user_tg_id = Column(BigInteger, ForeignKey("users.tg_id"))
    user = relationship("User", back_populates="paid_questions")