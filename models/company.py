from init import db, ma
from marshmallow import fields

class Company(db.Model):
    __tablename__ = 'companies'

    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String, default='nomadic')
    artistic_director = db.Column(db.String)

class CompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'location', 'artistic_director')

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)