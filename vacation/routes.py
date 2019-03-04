from flask import render_template, url_for, flash, redirect
from vacation import app
from vacation.models import User, Vacation, OAuth
from vacation.forms import VacationForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_dance.contrib.google import make_google_blueprint, google
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError, OAuth2Error
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin, SQLAlchemyBackend
from flask_dance.consumer import oauth_authorized

login_manager = LoginManager(app)

google_blueprint = make_google_blueprint(client_id='925027957735-njun0ge1m7hvr0p4u0dkrgp8ks5ti9p4.apps.googleusercontent.com',
	 client_secret='y52Xui7NJVvFIr5pxHTANviY')

app.register_blueprint(google_blueprint, scope=["profile", "email"], url_prefix='/gCallback')


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

google_blueprint.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
	account_info = blueprint.session.get("/oauth2/v1/userinfo")
	if account_info.ok:
		account_info_json = account_info.json()
		email = account_info_json['email']
		query = User.query.filer_by(email=email)

		try:
			user = query.one()
		except NoResultFound:
			user = User()
			user.name = account_info_json['name']
			user.email = account_info_json['email']
			db.session.add(user)
			db.session.commit()
		login_user(user, remember=True)


@app.route("/")
@login_required
def index():
	return render_template('index.html')

@app.route("/login")
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    try:
        account_info = google.get("/oauth2/v1/userinfo")
        assert account_info.ok, account_info.text
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for("google.login"))
    return render_template('index.html')

@app.route("/logout")
@login_required
def logout():
	logout_user
	return redirect(url_for('index'))

@app.route("/admin")
def admin_panel():
	return render_template('admin.html', title='Admin Panel')

@app.route("/setup", methods=['GET', 'POST'])
def vacation_setup():
	if not google.authorized:
		return redirect(url_for('google.login'))
	form = VacationForm()
	if form.validate_on_submit():
		vacation_request = Vacation(start_period=form.start.data, end_period=form.end.data, author=current_user)
		db.session.add(vacation_request)
		db.session.commit()
		flash(f'Leaving request submitted!', 'success')
		return redirect(url_for('index'))
	return render_template('setup.html', title='Vacation Setup', form=form)