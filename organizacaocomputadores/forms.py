from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from organizacaocomputadores.models import Usuario, Computador
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmação', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado! Cadastre-se com outro e-mail ou faça login para continuar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse email, cadastre um novo email.')


class FormCriarComputador(FlaskForm):
    codigo = StringField('Código', validators=[DataRequired(), Length(6)])
    modelo = StringField('Modelo', validators=[DataRequired()])
    ano = StringField('ano', validators=[DataRequired(), Length(4)])
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    sede = StringField('Sede', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])
    serial = StringField('serial', validators=[DataRequired()])
    botao_submit_criarcomputador = SubmitField('Criar Computador')

    #def validate_codigo(self, codigo):
        #computador = Computador.query.filter_by(codigo=codigo.data).first()
        #if computador:
          # raise ValidationError('Computador já cadastrado! Cadastre outro!')

class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')


class FormEditarComputador(FlaskForm):
        codigo = StringField('Código', validators=[DataRequired(), Length(6)])
        modelo = StringField('Modelo', validators=[DataRequired()])
        ano = StringField('ano', validators=[DataRequired(), Length(4)])
        username = StringField('Nome de Usuário', validators=[DataRequired()])
        sede = StringField('Sede', validators=[DataRequired()])
        status = StringField('status', validators=[DataRequired()])
        serial = StringField('serial', validators=[DataRequired()])
        botao_submit_editarcomputador = SubmitField('Editar Computador')