from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Instance, Document, fields


db = AsyncIOMotorClient('mongodb://localhost:27017')['bot']
instance = Instance(db)


@instance.register
class User(Document):
    class Meta:
        collection_name = 'users'
        indexes = []

    user_id = fields.IntField(required=True, unique=True)
    created = fields.DateTimeField(required=True)
    visited = fields.DateTimeField(required=True)
    username = fields.StrField(required=True, allow_none=True)
    first_name = fields.StrField(required=True)
    last_name = fields.StrField(required=True, allow_none=True)
    language_code = fields.StrField(required=True, allow_none=True)
    language = fields.StrField(required=True)
    is_active = fields.BoolField(required=True, default=True)


async def create_indexes():
    await User.ensure_indexes()


if __name__ == '__main__':
    pass
