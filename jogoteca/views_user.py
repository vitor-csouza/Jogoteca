from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from models import Usuarios
from helpers import UserForm
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    next = request.args.get('next')
    form = UserForm()
    return render_template('login.html', next=next, form=form)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    form = UserForm(request.form)
    user = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.senha, form.password.data)
    if user and password:
        session['logged_user'] = user.nickname
        flash(user.nickname + ' logado com sucesso')
        next_page = request.form['next']
        return redirect(next_page)
    else:
        flash('Usuário não logado!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))