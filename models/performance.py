from init import db, ma
from marshmallow import fields

class Performance(db.Model):
    __tablename__ = 'performances'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.date)
    artform = db.Column(db.String) # should i make this another table?

    company = db.relationship('Company', back_populate='performances')

class PerformanceSchema(ma.Schema):
    company = fields.Nested('CompanySchema', only=['name'])
    
    class Meta:
        fields = ('id', 'company', 'title', 'date', 'artform')
        ordered = True

performance_schema = PerformanceSchema()
performances_schema = PerformanceSchema(many=True)