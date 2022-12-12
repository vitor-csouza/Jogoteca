from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos
from helpers import recover_image, delete_file, GameForm

import time


@app.route('/')
def index():
    games = Jogos.query.order_by(Jogos.id)
    return render_template('list.html', title='Jogos', games=games)


@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    form = GameForm()
    return render_template('new.html', title='Novo Jogo', form=form)


@app.route('/create', methods=['POST'])
def create():
    form = GameForm(request.form)

    flash(form.validate_on_submit())
    if not form.validate_on_submit():
        return redirect(url_for('new'))

    name = form.name.data
    category = form.category.data
    console = form.console.data

    game = Jogos.query.filter_by(nome=name).first()

    if game:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    new_game = Jogos(nome=name, categoria=category, console=console)
    db.session.add(new_game)
    db.session.commit()

    file = request.files['file']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    file.save(f'{upload_path}/capa{new_game.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', next=url_for('new')))
    game = Jogos.query.filter_by(id=id).first()
    form = GameForm()
    form.name.data = game.nome
    form.category.data = game.categoria
    form.console.data = game.console
    thumbnail_game = recover_image(id)
    return render_template('update.html', title='Editando Jogo', id=id, thumbnail_game=thumbnail_game, form=form)


@app.route('/update', methods=['POST'])
def update():
    form = GameForm(request.form)

    if form.validate_on_submit():

        game = Jogos.query.filter_by(id=request.form['id']).first()
        game.nome = form.name.data
        game.categoria = form.category.data
        game.console = form.console.data

        db.session.add(game)
        db.session.commit()

        file = request.files['file']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        delete_file(game.id)
        file.save(f'{upload_path}/capa{game.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()

    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))



@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)


