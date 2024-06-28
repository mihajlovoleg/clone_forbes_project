from flask import Blueprint, render_template, redirect, url_for, session, request
from app.forms import CreateArticleForm, EditArticleForm, DeleteForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app import app, mongo
from app.utils import allowed_image_file, is_admin, is_moder
from bson.objectid import ObjectId

art_bp = Blueprint('art', __name__)



@art_bp.route('/choose-action', methods=['GET'])
def manage_articles():
    return render_template('articles_templates/choose_action.html')

@art_bp.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if not is_moder(session.get('role')):
        return redirect(url_for('home.home_page'))
    
    form = CreateArticleForm()
    
    if form.validate_on_submit():
        main_image = form.main_image.data
        art_title = form.art_title.data
        content = form.content.data
        author = f"{session['name']} {session['surname']}"
        created_at = datetime.now()
        
        main_image_url = None
        if main_image and allowed_image_file(main_image.filename):
            filename = secure_filename(f"{art_title}_{created_at.strftime('%Y%m%d%H%M%S')}.jpg")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            main_image.save(filepath)
            main_image_url = 'uploads/' + filename

        article_data = {
            'main_image': main_image_url,
            'title': art_title,
            'content': content,
            'author': author,
            'created_at': created_at
        }
        result = mongo.db.articles.insert_one(article_data)
        
        return redirect(url_for('home.home_page'))
        
        
        
    return render_template('articles_templates/create_article.html', form=form)

@art_bp.route('/article/<string:article_id>')
def article(article_id):
    form = DeleteForm()
    article = mongo.db.articles.find_one({'_id': ObjectId(f'{article_id}')})
    role = session.get('role')
    
    if article:
        print('Article has been found')
    else:
        print('404')
    return render_template('articles_templates/article.html', article=article, role=role, form=form)

@art_bp.route('/edit-article/<string:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if not is_moder(session.get('role')):
        return redirect(url_for('home.home_page'))
    form = EditArticleForm()

    article = mongo.db.articles.find_one({'_id': ObjectId(article_id)})

    if article:
        if request.method == 'GET':
            form.art_title.data = article.get('title', '')
            form.content.data = article.get('content', '')


            main_image_path = article.get('main_image', '')
            if main_image_path:
                filename = os.path.basename(main_image_path)
                form.main_image.data = filename

        if form.validate_on_submit():
            main_image = form.main_image.data
            art_title = form.art_title.data
            content = form.content.data
            created_at = datetime.now()

            
            main_image_url = None
            if main_image and allowed_image_file(main_image.filename):
                filename = secure_filename(main_image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                main_image.save(filepath)
                main_image_url = 'uploads/' + filename


            updated_article = {
                'main_image': main_image_url,
                'title': art_title,
                'content': content,
                'created_at': created_at,
                'author': f"{session.get('name')} {session.get('surname')}"
            }


            result = mongo.db.articles.update_one({'_id': ObjectId(article_id)}, {'$set': updated_article})
            
            return redirect(url_for('art.article', article_id=article['_id']))

    return render_template('articles_templates/edit_article.html', form=form, article=article, article_id=article_id)

@art_bp.route('/delete-article/<string:article_id>', methods=['POST'])
def delete_article(article_id):
    
    article = mongo.db.articles.find_one({'_id': ObjectId(article_id)})
    if article is None:
        return redirect(url_for('home.home_page'))

    main_image = article.get('main_image')
    if main_image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(main_image))
        if os.path.exists(image_path):
            os.remove(image_path)

    mongo.db.articles.delete_one({'_id': ObjectId(article_id)})

    return redirect(url_for('home.home_page'))
