"""app/feedback/models/feedback.py
"""

from datetime import datetime

from feedback.models import db


class Feedback(db.Model):
    """Feedback
    """
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, service, title, detail):
        self.service = service
        self.title = title
        self.detail = detail

    def to_dict(self):
        """to_dict
        """
        return {
            'id': self.id,
            'service': self.service,
            'title': self.title,
            'detail': self.detail,
            'created_date': self.created_date
        }
