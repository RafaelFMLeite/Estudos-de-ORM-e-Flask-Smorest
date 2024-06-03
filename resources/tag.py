from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            #using filter to check if there is a tag with the same name in the same store
            #also it needs to use the first() to return a boolean not only a query object
            abort(409, message="A tag with that name already exists in that store")

        tag = TagModel(**tag_data, store = store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback() 
            abort(500, message="An error occurred while inserting the tag")

        return tag

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag