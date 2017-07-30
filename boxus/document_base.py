import json
from datetime import datetime

from couchdb.mapping import Document, DateTimeField

class DocumentBase(Document):
    created_at      = DateTimeField()
    updated_at      = DateTimeField()

    db = None
    db_name = None

    def __init__(self, db = None):
        if db:
            self.db = db

        Document.__init__(self)

    @classmethod
    def _wrapper(cls, row):
        if 'doc' in row:
            doc = row['doc']
        elif 'value' in row:
            doc = row['value']
        else:
            doc = row

        return cls.wrap(doc)

    @classmethod
    def find(cls, db, doc_id):
        doc = cls.load(db[cls.db_name], doc_id)

        if doc:
            doc.db = db

        return doc

    @classmethod
    def all_iter(cls, db):
        return db[cls.db_name].view('_all_docs', cls._wrapper, **{ 'include_docs': True })

    @classmethod
    def all(cls, db):
        view = cls.all_iter(db)
        rows = list(view)

        for row in view:
            row.db = db

        return rows

    def save(self):
        if not self.created_at:
            self.created_at = datetime.now()
        else:
            self.updated_at = datetime.now()

        self.store(self.db[self.db_name])

    def destroy(self):
        self.db[self.db_name].delete(self)

    def to_dict(self):
        return self.__dict__['_data']

    def to_json(self):
        return json.dumps(self, default=lambda d: d.to_dict(), sort_keys=True)
