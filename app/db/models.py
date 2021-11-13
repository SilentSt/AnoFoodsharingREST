import uuid as uuid
from datetime import datetime
from sqlalchemy import Column, TEXT, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from misc import Base


class UsersDatabaseModel(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    role = Column(Integer, nullable=False, default=0)
    password = Column(TEXT, nullable=False)
    register_time = Column(DateTime, default=datetime.now)


class QuestionsModel(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    title = Column(TEXT, nullable=False)

    employees = relationship('AnswersModel', secondary='link')


class AnswersModel(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    title = Column(TEXT, nullable=False)

    employees = relationship('QuestionsModel', secondary='link')


class QuestionsAnswersModel(Base):
    __tablename__ = 'questions_answers'
    question_id = Column(ForeignKey('questions.id'), primary_key=True)
    answer_id = Column(ForeignKey('answers.id'), primary_key=True)
    correct_answer = Column(Boolean, nullable=True)


class OrganizationsModel(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)


class RecipientsModel(Base):
    __tablename__ = 'recipients'
    id = Column(Integer, primary_key=True)
    address = Column(String(255), nullable=False)

    delivery = relationship("RecipientsDeliveryModel", back_populates="recipients")


class RecipientsDeliveryModel(Base):
    __tablename__ = 'recipient_delivery'
    id = Column(Integer, primary_key=True)

    recipient_id = Column(Integer, ForeignKey('recipients.id'))
