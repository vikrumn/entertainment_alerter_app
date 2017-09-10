from flask_sqlalchemy import SQLAlchemy
import math

db = SQLAlchemy()
association_table = db.Table('user_media_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'))
)