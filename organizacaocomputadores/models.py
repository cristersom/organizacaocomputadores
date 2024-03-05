from organizacaocomputadores import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(50), nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    senha = database.Column(database.String(60), nullable=False)
    foto_perfil = database.Column(database.String(20), nullable=False, default='default.jpg')
    computadores = database.relationship('Computador', backref='autor', lazy=True)
    posts = database.relationship('Post', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)

class Computador(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    codigo = database.Column(database.String(20), nullable=False)
    modelo = database.Column(database.String(100), nullable=False)
    ano = database.Column(database.Integer, nullable=False)
    username = database.Column(database.String(50), nullable=False)
    sede = database.Column(database.String(100), nullable=False)
    status = database.Column(database.String(20), nullable=False)
    serial = database.Column(database.String(20), nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String(100), nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
