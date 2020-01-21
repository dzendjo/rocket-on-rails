from models import User
import asyncio

import os
import datetime, pytz


async def create_user(user_dict):
    if 'is_bot' in user_dict:
        del user_dict['is_bot']
    user_dict['is_active'] = True
    user_dict['created'] = datetime.datetime.now()
    user_dict['visited'] = datetime.datetime.now()
    user_dict['language'] = 'en'
    user = User(**user_dict)

    if await user.commit():
        return user
    else:
        return None


async def get_user(request_user):
    user = await User.find_one({'user_id': request_user['user_id']})
    if user:
        user.visited = datetime.datetime.now()
        await user.commit()
        return user
    else:
        return await create_user(request_user)


if __name__ == '__main__':
    pass
