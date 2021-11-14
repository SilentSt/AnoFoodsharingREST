from typing import Union
from uuid import UUID

from app.db.exceptions import duplicate_pass, no_match_pass
from app.db.models import UsersDatabaseModel, DeliveryModel, OrganizationsRecipientsModel, DocumentsModel
from app.security.security import get_password_hash
from app.utils.utils import generate_link_photo


class CrudDatabase:

    @duplicate_pass
    async def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        city: str,
        address: str,
        phone: str,
        password: str):
        password_hashed = get_password_hash(password)

        created_user = UsersDatabaseModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            city=city,
            address=address,
            phone=phone,
            password=password_hashed
        )

        await created_user.save()
        return created_user

    @staticmethod
    async def get_users():
        items = await UsersDatabaseModel.objects.all()
        return items

    @no_match_pass
    async def get_user_by_uuid(self, uuid: Union[UUID, str]):
        user = await UsersDatabaseModel.objects.get(id=uuid)
        return user

    @no_match_pass
    async def patch_user(self, uuid: Union[UUID, str], **kwargs):
        if kwargs.get("password"):
            kwargs['password'] = get_password_hash(kwargs.get("password"))

        query = await UsersDatabaseModel.objects.filter(id=uuid).update(**kwargs)
        return bool(query)

    @no_match_pass
    async def get_delivery_document(self, uuid: Union[UUID, str]) -> str:
        query = await DeliveryModel.objects.filter(id=uuid).get()
        return query.path

    @no_match_pass
    async def get_user_by_email(self, email: str):
        user = await UsersDatabaseModel.objects.get(email=email)
        return user

    @staticmethod
    async def get_all_addresses():
        return await DeliveryModel.objects.all()

    @no_match_pass
    async def update_delivery_path_status_by_id(self, delivery_id: int, document_path: str) -> None:
        new_file = DocumentsModel(path=document_path)
        await new_file.save()

        delivery_model = await DeliveryModel.objects.get(id=delivery_id)
        delivery_model.document_path = new_file.id
        delivery_model.status = True
        await delivery_model.update()

    @no_match_pass
    async def get_document_path(self, document_id: str) -> str:
        doc = await DocumentsModel.objects.get(id=document_id)
        return doc.path



    @staticmethod
    async def get_all_organizations_recipients():
        rows = await OrganizationsRecipientsModel.objects.select_related(
            ["organization_id", "organization_id__address_id"]).all()

        unique_organizations = []
        organizations_values = []

        for row in rows:
            if row.organization_id.id not in unique_organizations:
                unique_organizations.append(row.organization_id.id)

                organizations_values.append(
                    {
                        "organization": {
                            "id": row.organization_id.id,
                            "address": row.organization_id.address_id.address,
                            "delivery_date": row.organization_id.delivery_date,
                            "delivery_end": str(
                                row.organization_id.delivery_date + row.organization_id.delivery_interval),
                            "status": row.organization_id.status,
                            "document_id": getattr(row.organization_id.document_path, "id", None),
                            "document_url": generate_link_photo(getattr(row.organization_id.document_path, "id", None))
                        }
                    }
                )

        for _id, value in enumerate(unique_organizations):
            recipients = await OrganizationsRecipientsModel.objects.select_related(
                ["recipient_id", "recipient_id__address_id"]
            ).filter(organization_id=value).all()

            organizations_values[_id]["recipients"] = [
                {
                    "delivery_date": str(i.recipient_id.delivery_date),
                    "delivery_end": str(i.recipient_id.delivery_date + i.recipient_id.delivery_interval),
                    "address": i.recipient_id.address_id.address,
                    "status": i.recipient_id.status,
                    "document_id": getattr(i.recipient_id.document_path, "id", None),
                    "document_url": generate_link_photo(getattr(i.recipient_id.document_path, "id", None))
            } for i in recipients]
        return organizations_values

