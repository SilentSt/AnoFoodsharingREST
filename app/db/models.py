import uuid as uuid
from datetime import datetime
from app.db.deps import Interval
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
import ormar
import databases

from misc import metadata, database


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class UsersDatabaseModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format='string')
    first_name: str = ormar.String(max_length=100, nullable=False)
    last_name: str = ormar.String(max_length=100, nullable=False)
    city: str = ormar.String(max_length=100, nullable=False)
    address: str = ormar.String(max_length=100, nullable=False)
    phone: str = ormar.String(max_length=100, nullable=False)
    email: str = ormar.String(max_length=100, nullable=False, unique=True)
    role: int = ormar.Integer(nullable=False, default=0)
    password: str = ormar.Text(nullable=False)
    register_time: datetime = ormar.DateTime(default=datetime.now)


#
# class QuestionsModel(Base):
#     __tablename__ = 'questions'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(TEXT, nullable=False)
#
#     employees = relationship('AnswersModel', secondary='link')
#
#
# class AnswersModel(Base):
#     __tablename__ = 'answers'
#
#     id = Column(Integer, primary_key=True)
#     title = Column(TEXT, nullable=False)
#
#     employees = relationship('QuestionsModel', secondary='link')
#
#
# class QuestionsAnswersModel(Base):
#     __tablename__ = 'questions_answers'
#
#     question_id = Column(ForeignKey('questions.id'), primary_key=True)
#     answer_id = Column(ForeignKey('answers.id'), primary_key=True)
#     correct_answer = Column(Boolean, nullable=True)

# class DeliveryRecipientsModel(Base):
#     __tablename__ = 'delivery_recipients'
#
#     delivery_id = Column(ForeignKey('organizations_delivery.id'), primary_key=True)
#     answer_id = Column(ForeignKey('answers.id'), primary_key=True)
#     correct_answer = Column(Boolean, nullable=True)
#


class AddressesModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "addresses"

    id = ormar.Integer(primary_key=True)
    address = ormar.String(max_length=255, nullable=False)
    shop = ormar.Boolean(nullable=False)  # 0 - получатель, 1 - магазин.


class DocumentsModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "documents"

    id: UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format='string')
    path = ormar.String(max_length=255, nullable=False)


class DeliveryModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "delivery"

    id = ormar.Integer(primary_key=True)
    address_id = ormar.ForeignKey(AddressesModel)
    delivery_date = ormar.DateTime(nullable=False)
    delivery_interval = Interval(minutes=0)

    document_path = ormar.ForeignKey(DocumentsModel, nullable=True)
    status = ormar.Boolean(nullable=False, default=False)


class OrganizationsRecipientsModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "organizations_recipients"

    id = ormar.Integer(primary_key=True)
    organization_id = ormar.ForeignKey(DeliveryModel, related_name="organization")
    recipient_id = ormar.ForeignKey(DeliveryModel, related_name="recipient")



