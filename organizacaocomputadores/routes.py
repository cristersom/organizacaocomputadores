from flask import Flask, render_template, flash, request, redirect, url_for, abort
from organizacaocomputadores.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarComputador, FormCriarPost, FormEditarComputador
from organizacaocomputadores import app, database, bcrypt
from organizacaocomputadores.models import Usuario, Computador, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
@login_required
def home():
    order_by = request.args.get('order_by', 'codigo')  # Recebe o parâmetro de ordenação
    sort_order = request.args.get('sort_order', 'asc')  # Recebe o parâmetro de ordem de classificação
    computadores = None

    if sort_order == 'asc':  # Verifica a ordem de classificação
        if order_by == 'codigo':
            computadores = Computador.query.order_by(Computador.codigo.asc()).all()
        elif order_by == 'modelo':
            computadores = Computador.query.order_by(Computador.modelo.asc()).all()
        elif order_by == 'ano':
            computadores = Computador.query.order_by(Computador.ano.asc()).all()
        elif order_by == 'username':
            computadores = Computador.query.order_by(Computador.username.asc()).all()
        elif order_by == 'sede':
            computadores = Computador.query.order_by(Computador.sede.asc()).all()
        elif order_by == 'status':
            computadores = Computador.query.order_by(Computador.status.asc()).all()
        elif order_by == 'serial':
            computadores = Computador.query.order_by(Computador.serial.asc()).all()
    else:
        if order_by == 'codigo':
            computadores = Computador.query.order_by(Computador.codigo.desc()).all()
        elif order_by == 'modelo':
            computadores = Computador.query.order_by(Computador.modelo.desc()).all()
        elif order_by == 'ano':
            computadores = Computador.query.order_by(Computador.ano.desc()).all()
        elif order_by == 'username':
            computadores = Computador.query.order_by(Computador.username.desc()).all()
        elif order_by == 'sede':
            computadores = Computador.query.order_by(Computador.sede.desc()).all()
        elif order_by == 'status':
            computadores = Computador.query.order_by(Computador.status.desc()).all()
        elif order_by == 'serial':
            computadores = Computador.query.order_by(Computador.serial.desc()).all()

    # Determina a próxima ordem de classificação
    next_sort_order = 'asc' if sort_order == 'desc' else 'desc'

    return render_template('home.html', computadores=computadores, order_by=order_by, sort_order=sort_order,
                           next_sort_order=next_sort_order)

    search_query = request.args.get('search')
    # Use search_query para filtrar os resultados da sua consulta ao banco de dados
    # Exemplo:
    if search_query:
        computadores = Computador.query.filter(Computador.modelo.ilike(f"%{search_query}%")).all()
    else:
        computadores = Computador.query.all()

    return render_template('computador.html', computadores=computadores)



@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/posts")
@login_required
def posts():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('posts.html', posts=posts)


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()  # Added () after first
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. Email ou senha incorretos', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode(
            'utf-8')  # Decode the password hash
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Cadastro feito com sucesso no email {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso.', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/computador/criar', methods=['GET', 'POST'])
@login_required
def criar_computador():
    form = FormCriarComputador()
    if form.validate_on_submit():
        computador = Computador(codigo=form.codigo.data, modelo=form.modelo.data, ano=form.ano.data,
                                username=form.username.data, sede=form.sede.data, status=form.status.data,
                                serial=form.serial.data, autor=current_user)
        database.session.add(computador)
        database.session.commit()
        flash('Computador adicionado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarcomputador.html', form=form)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post adicionado com sucesso!', 'alert-success')
        return redirect(url_for('posts'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extencao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash(f'Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>' , methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data=post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com sucesso!', 'alert-success')
            return redirect(url_for('posts'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/computador/<computador_id>', methods=['GET', 'POST'])
@login_required
def exibir_computador(computador_id):
    computador = Computador.query.get(computador_id)
    if not computador:
        abort(404)  # Se o computador não existir, retorna 404

    if current_user != computador.autor:
        abort(403)  # Se o usuário não for o autor do computador, retorna 403

    form = FormEditarComputador(obj=computador)  # Preenche o formulário com os dados atuais do computador
    if request.method == 'POST' and form.validate():
        form.populate_obj(computador)  # Preenche o objeto computador com os dados do formulário
        database.session.commit()
        flash('Computador atualizado com sucesso!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('computador.html', computador=computador, form=form)


@app.route('/post/<post_id>/excluir' , methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('posts'))
    else:
        abort(403)


@app.route('/computador/<computador_id>/excluir' , methods=['GET', 'POST'])
@login_required
def excluir_computador(computador_id):
    computador = Computador.query.get(computador_id)
    if current_user == computador.autor:
        database.session.delete(computador)
        database.session.commit()
        flash('Computador excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)