import flask
import asyncio
import repltalk
import authcord

from web import db
from web import app

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

from .models import User
from .models import Project
from .forms import NewProject

try: db.create_all()
except: pass

replit = repltalk.Client()

@app.route("/")
def index():
	return flask.render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
	return flask.render_template("dashboard.html")


@app.route("/project/<pid>")
@login_required
def project_page(pid):
	project = None

	for p in current_user.projects:
		if str(p.id) == (pid):
			project = p
		else:
			pass

	if project:
		return flask.render_template("project.html", new=False, project=project)
	else:
		return flask.abort(500)


@app.route("/new-project", methods=["GET", "POST"])
@login_required
def new_project():
	form = NewProject()
	if form.validate_on_submit():
		project = Project()

		project.name = str(form.name.data)
		project.content = str(form.content.data)
		project.language = str(form.language.data)
		project.user_id = str(current_user.id)

		db.session.add(project)
		db.session.commit()

		return flask.redirect(f"/project/{project.id}")
	return flask.render_template("project.html", new=True, form=form)


@app.route("/login")
def login_base():
	dlink = authcord.get_request_uri()

	replid = flask.request.headers['X-Replit-User-Id']
	replname = flask.request.headers['X-Replit-User-Name']

	if replname and replid:
		data = {'id': replid, 'name': replname}
		state = authcord.create_state(data, 5)
		url = flask.url_for("login_replit", state=state)

		return flask.redirect(url)
	else:
		return flask.render_template("login.html", dlink=dlink)


@app.route("/logout")
def logout():
    logout_user()
    return flask.redirect(flask.url_for("index"))


@app.route("/login-replit-callback")
def login_replit():
	raw_state = flask.request.args.get("state")
	state = authcord.parse_state(raw_state)

	if not state: return flask.abort(403)

	r = asyncio.run(replit.get_user(state['name']))
	user = User.query.filter_by(id=state['id']).first()
	if not user:
		user = User()
		db.session.add(user)
	else:
		pass

	user.id = str(r.id)
	user.id_type = "Repl.it"
	user.name = r.name
	user.pfp = r.avatar

	db.session.commit()
	login_user(user)

	return flask.redirect(flask.url_for("index"))


@app.route("/login-discord-callback")
def login_discord():
	code = flask.request.args.get("code")
	token = authcord.parse_token(authcord.exchange_code(code))

	d = authcord.access_endpoint("/users/@me", "GET", "Bearer", token['access_token'])
	user = User.query.filter_by(id=d['id']).first()

	if not user:
		user = User()
		db.session.add(user)
	else:
		pass

	user.id = d['id']
	user.id_type = "Discord"
	user.name = d['username']
	user.pfp = authcord.IMG_BASE.format(d['id'], d['avatar'], 128)

	db.session.commit()
	login_user(user)

	return flask.redirect(flask.url_for("index"))

