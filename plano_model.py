from aplication import db
from wtforms import Form, StringField, SelectField, validators, IntegerField
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint, exc
class plano(db.Model):
    __tablename__ = "plano"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    Codigo_TRM = db.Column(db.String, nullable=False)
    area = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    disciplina = db.Column(db.String, nullable=False)
    codigo = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    rev = db.Column(db.String, nullable=False)
class plano_form(Form):
    id = IntegerField('id')
    Codigo_TRM = StringField('Codigo_TRM')
    area = StringField('area')
    fecha = StringField('fecha')
    disciplina = StringField('disciplina')
    codigo = StringField('codigo')
    descripcion = StringField('descripcion')
    rev = StringField('rev')
def plano_convert(plano, form):
    plano.id = form.id.data
    plano.Codigo_TRM = form.Codigo_TRM.data
    plano.area = form.area.data
    plano.fecha = form.fecha.data
    plano.disciplina = form.disciplina.data
    plano.codigo = form.codigo.data
    plano.descripcion = form.descripcion.data
    plano.rev = form.rev.data
    return plano
def plano_obj(plano, obj):
    plano.id = obj.id
    plano.Codigo_TRM = obj.Codigo_TRM
    plano.area = obj.area
    plano.fecha = obj.fecha
    plano.disciplina = obj.disciplina
    plano.codigo = obj.codigo
    plano.descripcion = obj.descripcion
    plano.rev = obj.rev
    return plano