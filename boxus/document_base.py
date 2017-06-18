from datetime import datetime

from couchdb.mapping import Document, TextField, DateTimeField

class DocumentBase(Document):
    description     = TextField()
    created_at      = DateTimeField()
    updated_at      = DateTimeField()

    def save(self, db):
        if not self.created_at:
            self.created_at = datetime.now()
        else:
            self.updated_at = datetime.now()

        self.store(db)
