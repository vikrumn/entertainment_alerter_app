from db import db, association_table

class MediaModel(db.Model):
	__tablename__ = 'media'

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(80))
	media_type = db.Column(db.String(80))
	users = db.relationship("UserModel", secondary = association_table, backref = db.backref("media", lazy = 'dynamic'))

	def __init__(self, title, media_type):
		self.title = title
		self.media_type = media_type

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_title(cls, title):
		return cls.query.filter_by(title = title).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	def json(self):
		return {'title': self.title, 'type': self.media_type, 'users': list(user.username for user in self.users)}