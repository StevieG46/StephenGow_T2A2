from init import db, ma
from marshmallow import fields

class Company(db.Model):
    __tablename__ = 'companies'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String)
    artistic_director = db.Column(db.String)

    # performances = db.relationship('Performance', back_populates='company.name', cascade='all, delete')

class CompanySchema(ma.Schema):
    # performances = fields.Nested('PerformanceSchema', only=['title'])

    class Meta:
        fields = ('id', 'name', 'location', 'artistic_director', 'performances')

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)