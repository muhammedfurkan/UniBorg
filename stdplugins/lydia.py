# import asyncio
# import logging
# from time import time

# from telethon import events

# import coffeehouse as cf
# from coffeehouse.api import API
# from coffeehouse.lydia import LydiaAI
# from coffeehouse.exception import CoffeeHouseError
# from pymongo import MongoClient
# from sample_config import Config


# logging.basicConfig(level=logging.INFO)

# if Config.MONGO_DB_URI is not None:
#     cl = MongoClient(Config.MONGO_DB_URI)
#     db = cl['Userbot']
#     lydia = db.lydia

# if Config.LYDIA_API is not None:
#     api_key = Config.LYDIA_API
#     # Create the CoffeeHouse API instance
#     coffeehouse_api = API(api_key)
#     # Create Lydia instance
#     lydia_session = LydiaAI(coffeehouse_api)


# @borg.on( admin_cmd(pattern="cf", allow_sudo=True))
# async def lydia_enable(event):
#     if event.fwd_from:
#         return
#     if Config.MONGO_DB_URI and Config.LYDIA_API is None:
#         await event.edit("Make Sure You've added MONGO_URI and LYDIA_API env vars Correctly.")
#         return
#     if event.reply_to_msg_id is not None:
#         await event.edit("Reply To A User's Message to Add him/her in Lydia Auto-Chat.")
#         return
#     reply_msg = await event.get_reply_message()
#     user_id = reply_msg.sender_id
#     chat_id = event.chat_id
#     await event.edit("Processing...")
#     cursors = lydia.find({})
#     try:
#         for c in cursors:
#             if c['user_id'] == user_id and c['chat_id'] == chat_id:
#                 await event.edit("User is already in Lydia Auto-Chat.")
#                 return
#     except:
#         pass
#     session = lydia_session.create_session()
#     ses = {'id': session.id, 'expires': session.expires}
#     logging.info(ses)
#     lydia.insert_one({'user_id': user_id, 'chat_id': chat_id, 'session': ses})
#     await event.edit("Lydia AI Turned On for User: "+str(user_id))


# @borg.on( admin_cmd(pattern="delcf", allow_sudo=True))
# async def lydia_disable(event):
#     if event.fwd_from:
#         return
#     if Config.MONGO_DB_URI and Config.LYDIA_API is None:
#         await event.edit("Make Sure You've added MONGO_URI and LYDIA_API env vars Correctly.")
#         return
#     if event.reply_to_msg_id is not None:
#         await event.edit("Reply To A User's Message to Remove him/her from Lydia Auto-Chat.")
#         return
#     reply_msg = await event.get_reply_message()
#     user_id = reply_msg.sender_id
#     chat_id = event.chat_id
#     await event.edit("Processing...")
#     cursors = lydia.find({})
#     for c in cursors:
#         if c['user_id'] == user_id and c['chat_id'] == chat_id:
#             lydia.delete_one(c)
#     await event.edit("Lydia AI Turned OFF for User: "+str(user_id))


# @borg.on( admin_cmd(pattern="listcf", allow_sudo=True))
# async def lydia_list(event):
#     if event.fwd_from:
#         return
#     if Config.MONGO_DB_URI and Config.LYDIA_API is None:
#         await event.edit("Make Sure You've added MONGO_URI and LYDIA_API env vars Correctly.")
#         return
#     await event.edit("Processing...")
#     msg = "**Auto-Chat:**"
#     cur = lydia.find({})
#     for c in cur:
#         user_id = str(c['user_id'])
#         msg += "\n__User:__ [{}](tg://user?id={})".format(user_id, user_id)
#         msg += "\n__Chat:__ `{}`\n".format(str(c['chat_id']))
#     await event.edit(msg)


# @borg.on(events.NewMessage())
# async def Lydia_bot_update(event):
#     if event.fwd_from:
#         return
#     if Config.MONGO_DB_URI and Config.LYDIA_API is None:
#         return
#     if event.media is not None:
#         cursor = lydia.find({})
#         for c in cursor:
#             if c['user_id'] == event.sender_id and c['chat_id'] == event.chat_id:
#                 query = event.text
#                 ses = c['session']

#         # Check if the session is expired
#         # If this method throws an exception at this point, then there's an issue with the API, Auth or Server.
#                 if ses['expires'] < time():
#                     session = lydia_session.create_session()
#                     ses = {'id': session.id, 'expires': session.expires}
#                     logging.info(ses)
#                     lydia.update_one(
#                         c, {'$set': {'user_id': event.sender_id, 'chat_id': event.chat_id, 'session': ses}})

#         # Try to think a thought.
#                 try:
#                     async with borg.action(event.chat_id, "typing"):
#                         await asyncio.sleep(1)
#                         output = lydia_session.think_thought(ses['id'], query)
#                         await event.reply(output)
#                 except CoffeeHouseError as e:
#                     # CoffeeHouse related issue, session issue most likely.
#                     logging.error(str(e))

#     # Create a new session
#                     session = lydia_session.create_session()
#                     ses = {'id': session.id, 'expires': session.expires}
#                     logging.info(ses)
#                     lydia.update_one(
#                         c, {'$set': {'user_id': event.sender_id, 'chat_id': event.chat_id, 'session': ses}})

#     # Reply again, if this method fails then there's a other issue.
#                     async with borg.action(event.chat_id, "typing"):
#                         await asyncio.sleep(1)
#                         output = lydia_session.think_thought(ses['id'], query)
#                         await event.reply(output)
