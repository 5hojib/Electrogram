from .file_storage import FileStorage
from .memory_storage import MemoryStorage

try:
    import pymongo
except Exception:
    pass
else:
    from .mongo_storage import MongoStorage
from .storage import Storage
