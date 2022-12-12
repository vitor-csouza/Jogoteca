import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class GameForm(FlaskForm):
    name = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    submit = SubmitField('Salvar')


class UserForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    password = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')

def recover_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in filename:
            return filename

    return 'capa_padrao.jpg'


def delete_file(id):
    file = recover_image(id)
    if file != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))