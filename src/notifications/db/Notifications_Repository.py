from logging import getLogger
from unittest import result
from bson import ObjectId
from ..models. Notifications import NotificationBase, NotificationCreate, NotificationView

#cómo se habla con MongoDB

logger = getLogger()

class Notifications_Repository:
 
    def __init__(self, db):
        # Colección de MongoDB donde guardamos las notificaciones
        self.collection = db["notifications"]


    async def insert_notification(self, data: NotificationBase) -> NotificationView:
        doc = data.model_dump(by_alias=True)
        result = await self.collection.insert_one(doc)

        created = await self.collection.find_one({"_id": result.inserted_id})

        created["_id"] = str(created["_id"])

        return NotificationView.model_validate(created)
    

    async def get_all_notifications(self) -> list[NotificationView]:
        cursor = self.collection.find({})
        results = []

        async for doc in cursor:
            # Convertir ObjectId → str
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            results.append(NotificationView.model_validate(doc))

        return results
    

    async def get_notifications_by_user(self, user_id: str) -> list[NotificationView]:
        cursor = self.collection.find({"userId": user_id}).sort("createdAt", -1)
        
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(NotificationView.model_validate(doc))
        return results
    
    
    async def update_notification(self, notification_id: str, data: dict):
        result = await self.collection.find_one_and_update(
        {"_id": ObjectId(notification_id)},
        {"$set": data},
        return_document=True
    )

        if not result:
            return None

        result["_id"] = str(result["_id"])
        return NotificationView.model_validate(result)


    async def delete_notification(self, notification_id: str) -> bool:
        result = await self.collection.delete_one(
            {"_id": ObjectId(notification_id)}
        )
        return result.deleted_count == 1

