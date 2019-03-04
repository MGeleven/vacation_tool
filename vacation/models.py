from vacation import db


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True, nullable=False)
	name = db.Column(db.String(100), nullable=True)
	avatar = db.Column(db.String(200))
	active = db.Column(db.Boolean, default=False)
	tokens = db.Column(db.Text)
	role = db.Column(db.Text, default="Guest")
	vacations = db.relationship('Vacation', backref='author', lazy=True)

class Vacation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	start_period = db.Column(db.String(100), nullable=False)
	end_period = db.Column(db.String(100), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class OAuth(OAuthConsumerMixin, db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey(User.id))
	user = db.relationship(User)