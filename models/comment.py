from init import db, ma
from marshamllow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeginKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeigKey('reviews.id'), nullable=False)

    user = db.relationship('User', back_populates='comments')
    review = db.relationship('Review', back_populates='comments')

class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['username'])
    review = fields.Nested('ReviewSchema', exclude=['comments'])

    class Meta:
        fields = ('id', 'comment', 'date', 'user', 'review')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)