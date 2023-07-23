from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    performance_id = db.Column(db.Integer, db.ForeignKey('performances.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    performance = db.relationship('Performance', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
    comments = db.relationship('Comment', back_populates='reviews')

class ReviewSchema(ma.Schema):
    performance = fields.Nested('PerformanceSchema', only=['title'])
    user = fields.Nested('UserSchema', only=['username'])

    class Meta:
        fields = ('id', 'date', 'performance', 'review', 'rating', 'user')
        ordered = True

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)