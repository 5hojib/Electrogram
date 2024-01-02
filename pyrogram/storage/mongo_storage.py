import asyncio
import inspect
import time
from typing import List, Tuple, Any

from .dummy_client import DummyMongoClient
from pymongo import MongoClient, UpdateOne, DeleteMany
from pyrogram.storage.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer


class MongoStorage(Storage):
    lock: asyncio.Lock
    USERNAME_TTL = 8 * 60 * 60

    def __init__(
        self,
        name: str,
        connection: DummyMongoClient,
        remove_peers: bool = False
    ):
        super().__init__(name=name)
        database = None

        if isinstance(connection, DummyMongoClient):
            if isinstance(connection, MongoClient):
                raise Exception("Pymongo MongoClient object is not supported! please use async mongodb driver such as async_pymongo and motor.")
            database = connection[name]
        else:
            raise Exception("Wrong connection object type! please pass valid connection object to connection parameter!")

        self.lock = asyncio.Lock()
        self.database = database
        self._peer = database['peers']
        self._session = database['session']
        self._usernames = database['usernames']
        self._remove_peers = remove_peers

    async def open(self):
        if await self._session.find_one({'_id': 0}, {}):
            return
        await self._session.insert_one(
            {
                '_id': 0,
                'dc_id': 2,
                'api_id': None,
                'test_mode': None,
                'auth_key': b'',
                'date': 0,
                'user_id': 0,
                'is_bot': 0,

            }
        )

    async def save(self):
        pass

    async def close(self):
        pass

    async def delete(self):
        try:
            await self._session.delete_one({'_id': 0})
            if self._remove_peers:
                await self._peer.remove({})
        except Exception as _:
            return

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        s = int(time.time())
        bulk = [
            UpdateOne(
                {'_id': i[0]},
                {'$set': {
                    'access_hash': i[1], 
                    'type': i[2], 
                    'username': i[3], 
                    'phone_number': i[4],
                    'last_update_on': s
                }},
                upsert=True
            ) for i in peers
        ]
        if not bulk:
            return
        await self._peer.bulk_write(
            bulk
        )

    async def update_usernames(self, usernames: List[Tuple[int, str]]):
        s = int(time.time())
        bulk_delete = [
            DeleteMany(
                {'peer_id': i[0]}
            ) for i in usernames
        ]
        bulk = [
            UpdateOne(
                {'_id': i[1]},
                {'$set': {
                    'peer_id': i[0],
                    'last_update_on': s
                }},
                upsert=True
            ) for i in usernames
        ]
        if not bulk:
            return
        await self._usernames.bulk_write(
            bulk_delete
        )
        await self._usernames.bulk_write(
            bulk
        )

    async def get_peer_by_id(self, peer_id: int):
        r = await self._peer.find_one({'_id': peer_id}, {'_id': 1, 'access_hash': 1, 'type': 1})
        if not r:
            raise KeyError(f"ID not found: {peer_id}")
        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_username(self, username: str):
        r = await self._peer.find_one({'username': username},
                                      {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})

        if r is None:
            r2 = await self._usernames.find_one({'_id': username},
                                          {'peer_id': 1, 'last_update_on': 1})
            if r2 is None:
                raise KeyError(f"Username not found: {username}")
            if abs(time.time() - r2['last_update_on']) > self.USERNAME_TTL:
                raise KeyError(f"Username expired: {username}")
            r = await self._peer.find_one({'_id': r2['peer_id']},
                                          {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})
            if r is None:
                raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r['last_update_on']) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_phone_number(self, phone_number: str):

        r = await self._peer.find_one({'phone_number': phone_number},
                                      {'_id': 1, 'access_hash': 1, 'type': 1})

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def _get(self):
        attr = inspect.stack()[2].function
        d = await self._session.find_one({'_id': 0}, {attr: 1})
        if not d:
            return
        return d[attr]

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function
        await self._session.update_one({'_id': 0}, {'$set': {attr: value}}, upsert=True)

    async def _accessor(self, value: Any = object):
        return await self._get() if value == object else await self._set(value)

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)
