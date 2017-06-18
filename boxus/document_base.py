from datetime import datetime

from couchdb.mapping import Document, DateTimeField

class DocumentBase(Document):
    created_at      = DateTimeField()
    updated_at      = DateTimeField()

    db = None

    def __init__(self, db = None):
        if db:
            self.db = db

        Document.__init__(self)

    @classmethod
    def find(cls, db, doc_id):
        doc = cls.load(db, doc_id)

        if doc:
            doc.db = db

        return doc

    @classmethod
    def all(cls, db):
        view = db.view('_all_docs')

        return map(lambda d: cls.find(db, d['id']), view)

    def save(self):
        if not self.created_at:
            self.created_at = datetime.now()
        else:
            self.updated_at = datetime.now()

        self.store(self.db)

    def destroy(self):
        self.db.delete(self)
