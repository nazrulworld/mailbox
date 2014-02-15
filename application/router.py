from application import app
from flask import render_template, redirect, request, session, \
    flash, g, url_for
from .forms import LoginForm


@app.before_request
def before_request():
    g.email = session.get('email', None)
    g.password = session.get('password', None)
    g.imap4 = session.get('imap4', None)

@app.route('/')
@app.route('/index')
def index():
    if not g.imap4:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST' and form.validate_on_submit():
        from .mailbox import login
        imap4 = login(form.email.data, form.password.data)
        if hasattr(imap4, 'state') and imap4.state == 'AUTH':
            flash('Successfully authenticated', category='message')
            session['email'] = form.email.data
            session['password'] = form.password.data
            session['imap4'] = True
            imap4.logout()
            return redirect(url_for('inbox'))
        else:
            error = "Invalid user name or password"
    return render_template('login.html', form=form, error=error)


@app.route('/inbox', methods=['POST', 'GET'])
def inbox():
    if not g.imap4:
        return redirect(url_for('login'))
    from .mailbox import inbox
    emails = inbox()
    return render_template('inbox.html', emails=emails)


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash('Successfully disconnect from mail server')
    return redirect(url_for('login'), 302)


# Authentication decorator
def authenticate():
    if g.imap4 is not None and g.imap4 is True:
        return True
    return False