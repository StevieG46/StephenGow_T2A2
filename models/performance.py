from init import db, ma
from marshmallow import fields

class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    artform = db.Column(db.String) 

    reviews = db.relationship('Review', back_populates='performance', cascade='all, delete')

class PerformanceSchema(ma.Schema):
    reviews = fields.Nested('ReviewSchema', only=['review', 'rating'])
    
    class Meta:
        fields = ('id', 'company_id', 'title', 'date', 'artform',  'reviews')
        ordered = True

performance_schema = PerformanceSchema()
performances_schema = PerformanceSchema(many=True)