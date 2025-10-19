from flask import jsonify, Blueprint, request
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Post
from .schema import PostSchema
from sqlalchemy.orm import joinedload


blog_bp = Blueprint('blog_app', __name__)


@blog_bp.route('/create-post', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    new_post = Post(title=data.get('title'), body=data.get('body'), author_id=current_user_id)

    db.session.add(new_post)
    db.session.commit()

    return jsonify({'msg': "The Post Successfully Created!"})

@blog_bp.route('/posts')
def get_all_posts():
    posts = Post.query.all()

    output = [
        {"id":p.pid, "title":p.title, "author":p.author.fullname()}

        for p in posts    

    ]
    return jsonify(output)

@blog_bp.route('/posts/<int:pid>')
def get_post_by_id(pid):
    post = (
        Post.query
        .options(joinedload(Post.author))
        .filter_by(pid=pid)
        .first_or_404()
    )

    result = {
        "pid": post.pid,
        "title": post.title,
        "body": post.body,
        "author": post.author.fullname() 
    }

    return jsonify(result)
    
@blog_bp.route('/posts/<int:pid>/edit', methods=['PUT'])
@jwt_required()
def edit_post_by_id(pid):
    post = Post.query.get_or_404(pid)
    user_id = int(get_jwt_identity())
    print(user_id)
    print(post.author_id)

    if post and user_id == post.author_id:

        data = request.get_json()
        title = data.get('title')
        body = data.get('body')

        if title:
            post.title = title
        elif body:
            post.body = body
        
        db.session.commit()
        return jsonify({
            "msg":'Post Updated successfully!',
            "post":{
                'pid': post.pid,
                'title': post.title,
                'body': post.body
            }
            
            })
    else:
        return jsonify({
            'msg': "Invalid parameter!"
            })
    
@blog_bp.route('/posts/<int:pid>/delete',methods=['DELETE'])
@jwt_required()
def delete_post_by_id(pid):
    post = Post.query.get_or_404(pid)
    user_id = get_jwt_identity()

    if post and user_id == post.author_id:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "post deleted successfully!"})
    else:
        return jsonify({'msg':"invalid paramerter or invalid creditnial"})

    
