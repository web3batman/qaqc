from f0016_2_model import f0016_2,f0016_2_form,f0016_2_convert
from db_setup import init_db, db_session
from flask import Blueprint, Flask, jsonify, request, render_template, redirect, url_for, json, send_file
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import create_engine
import pandas as pd
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import io
f0016_2_app = Blueprint('f0016_2_app', __name__)
id=0
@f0016_2_app.route('/f0016_2_list', methods=['GET', 'POST'])
def f0016_2_list():
    global id
    id=request.args.get('area_id', None)
    qry = db_session.query(f0016_2).filter(f0016_2.area_id==id).all()
    return render_template('f0016_2_list.html', table=qry  )
@f0016_2_app.route('/f0016_2_new', methods=['GET', 'POST'])
def f0016_2_new():
    if request.method == 'GET':
        return render_template('f0016_2_new.html', id=id)
    if request.method == 'POST':
        form = f0016_2_form(request.form)
        db_session.add(f0016_2_convert(f0016_2(), form))
        db_session.commit()
        return redirect('/')
@f0016_2_app.route('/f0016_2_edit', methods=['GET', 'POST'])
def f0016_2_edit():
    if request.method == 'GET':
        id=request.args.get('id', None)
        qry = db_session.query(f0016_2).filter(f0016_2.id==id).first()
        return render_template('f0016_2_edit.html', val=qry)
    if request.method == 'POST':
        form = f0016_2_form(request.form)
        fo=f0016_2_convert(f0016_2(), form)
        flag_modified(fo,'ubicacion')
        db_session.merge(fo)
        db_session.flush()
        db_session.commit()
        return redirect('/')
@f0016_2_app.route('/f0016_2_delete', methods=['GET', 'POST'])
def f0016_2_delete():
    id=request.args.get('id', None)
    qry = db_session.query(f0016_2).filter(f0016_2.id==int(id))
    db_session.delete(qry.first())
    db_session.commit()
    return redirect('/')
@f0016_2_app.route('/f0016_2_print', methods=['GET', 'POST'])
def f0016_2_print():
    id=request.args.get('id', None)
    qry = db_session.query(f0016_2).filter(f0016_2.id==int(id)).first()
    doc = DocxTemplate("f0016_2.docx")
    context = {'frameworks' : qry}
    doc.render(context)
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, attachment_filename="f0016_2_"+"_1_"+".docx")