import plyvel


class Iterator:
    def __init__(
        self, db, include_key: bool = True, include_value: bool = True, reversed=False
    ):
        self.db = db
        self.include_key = include_key
        self.include_value = include_value
        self.reversed = reversed

        self._it = db.iterator(
            include_key=include_key, include_value=include_value, reverse=reversed
        )

    def __reversed__(self):
        return Iterator(
            self.db, self.include_key, self.include_value, not self.reversed
        )

    def seek(self, key: bytes):
        self._it.seek(key)

    def seek_to_last(self):
        # self._it.seek_to_stop()
        # Create a reversed iterator and then use seek_to_start to position it at the last key
        self._it = self.db.iterator(
            include_key=self.include_key, include_value=self.include_value, reverse=True
        )
        self._it.seek_to_start()

    def __iter__(self):
        return self

    def __next__(self):
        return self._it.__next__()


class LevelDB:
    db: plyvel.DB

    def __init__(self, db):
        self.db = db

    def get(self, key: bytes):
        return self.db.get(key)

    def put(self, key: bytes, value: bytes):
        return self.db.put(key, value)

    def delete(self, key: bytes):
        return self.db.delete(key)

    def iterkeys(self):
        return Iterator(self.db, include_value=False)

    def iteritems(self):
        return Iterator(self.db)

    def seek_to_last(self):
        it = Iterator(self.db)
        it.seek_to_last()
        return it


def open(dir, read_only: bool = False):
    return LevelDB(plyvel.DB(str(dir)))


def WriteBatch(db):
    return db.db.write_batch()
