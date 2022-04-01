# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, EditForm, DeleteForm, SearchForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Опубликовано')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.my_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Главная', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Некорректное имя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/post/<id>')
@login_required
def post(id):
    user = current_user
    my_post = Post.query.filter_by(id=id).first_or_404()
    return render_template('post.html', user=user, post=my_post)


@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user = current_user
    form = EditForm()
    my_post = Post.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        my_post.body = form.post_field.data
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('post', id=my_post.id))
    elif request.method == 'GET':
        form.post_field.data = my_post.body
    return render_template('edit.html', title='Редактирование заметки', form=form, user=user, post=my_post)


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = current_user
    form = DeleteForm()
    my_post = Post.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        db.session.delete(my_post)
        db.session.commit()
        flash('Изменения сохранены')
        return redirect(url_for('index'))
    return render_template('delete.html', title='Удаление заметки', form=form, user=user, post=my_post)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        text = form.search_field.data
        return redirect(url_for('search_results', text=text))
    return render_template('search.html', title='Поиск', form=form)


@app.route('/search_results')
@login_required
def search_results():
    text = request.args.get('text')
    posts = current_user.search_my_posts(text)
    return render_template('search_results.html', title='Результаты поиска', posts=posts)
