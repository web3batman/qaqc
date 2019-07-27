from flask import Flask, jsonify, request, render_template, redirect, url_for, json
from flask import send_file
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.attributes import flag_modified
import pandas as pd

import os
from glob import glob

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm, Inches, Pt
import io
import barcode
from barcode.writer import ImageWriter
import cv2

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaIoBaseDownload
from apiclient.http import MediaFileUpload
from db_setup import init_db, db_session
import numpy as np
#import argparse
import imutils
from datetime import date

import os
from pdf2image import convert_from_path, convert_from_bytes
from pyzbar.pyzbar import decode
#curl -d "{\"Medidas\":[[1,2,3,4]]}" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/predecir
from db_setup import init_db, db_session, service
import googledrive as gd
from f0016_2_app import *
from plano_model import plano,plano_form,plano_convert
from f0016_2_model import f0016_2,f0016_2_form,f0016_2_convert
from ubicacion_model import ubicacion,ubicacion_form,ubicacion_convert


app= Flask(__name__)
app.register_blueprint(f0016_2_app)

@app.route("/")
def home():
    disc = gd.items_folder(service,'Formatos_Calidad')
    disc = [x['title'] for x in disc]
    return render_template('disciplina_list.html', table=disc )
@app.route("/list_formato")
def list_formato():
    name = request.args.get('disciplina', None)
    disc = gd.items_folder(service,name )
#    disc = [x['title'].split('_')[-1] for x in disc]
    disc = [x['title'] for x in disc]
    return render_template('formato_list.html', table=disc )
@app.route("/list_protocolo", methods=['GET', 'POST'])
def list_protocolo():
    if request.method == 'GET':
        global fname
        name = request.args.get('format', None)
        fname = 'f' + name.split('.')[0].split('-')[-1] + '_2'
        exec("qry1 = db_session.query(" + fname + ").all()")
        return render_template('protocolo_list.html',table=locals()['qry1'], formato = fname)
@app.route("/edit_protocolo", methods=['GET', 'POST'])
def edit_protocolo():
    if request.method == 'GET':
        global fname
        name = request.args.get('format', None)
        fname = 'f' + name.split('.')[0].split('-')[-1] + '_2'
        return render_template(fname + '.html')
    if request.method == 'POST':
        exec("form =" + fname + "_form(request.form)")
        exec("formats = " + fname + "_convert(" + fname + "(),form)")
        exec("db_session.add(formats)")
        db_session.commit()
        return redirect('/')      
@app.route("/getData", methods=['GET'])
def getData():
    name = request.args.get('q', None)
    print(name)
    qry = db_session.query(ubicacion).all()
    ubica = [x.codigo+' '+x.ubicacion for x in qry]
    json_str = json.dumps(ubica)
    return jsonify(json_str)
@app.route("/planogetData", methods=['GET'])
def planogetData():
    name = request.args.get('q', None)
    print(name)
    qry = db_session.query(plano).all()
    planos = [x.codigo+' Rev.'+ x.rev for x in qry]
    json_str = json.dumps(planos)
    return jsonify(json_str)
@app.route('/protocolo_print', methods=['GET', 'POST'])
def protocolo_print():
    id=request.args.get('id', None)
    formato=request.args.get('formato', None)

    qry = db_session.query(f0016_2).filter(f0016_2.id==int(id)).first()
    doc = DocxTemplate("f0016_2.docx")
    
    fid = id.zfill(3) + "0"
    fform = formato.split('_')[0][1:]
    print(fid)
    print(fform)
    EAN = barcode.get_barcode_class('ean8')
    ean = EAN(fform + fid, writer=ImageWriter())
    fullname = ean.save('ean8_1')
    image = cv2.imread(fullname)
    cv2.imwrite(fullname, image[20:100,:,2])
    context = {'f' : qry,
               'bcean8' : InlineImage(doc,'ean8_1.png',width=Mm(40))}
    doc.render(context)
    
#    file_stream = io.BytesIO()
#    doc.save(file_stream)
    
    doc.save("temp.docx")
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    DRIVE = discovery.build('drive', 'v2', http=creds.authorize(Http()))
    buscar = DRIVE.files().list(q="title='DataBase'",fields='nextPageToken, items(id, title)',pageToken=None).execute()
    folder_id = buscar['items'][0]['id']
    body = {
    'title': fform + fid + ".docx",
    'mimeType': 'application/msword',
    "parents": [{"id": folder_id, "kind": "drive#childList"}] }                 
    media_body = MediaFileUpload('temp.docx', mimetype='application/msword', resumable=True)
    res = DRIVE.files().insert(
                body=body,
                media_body= media_body).execute()
#    file_stream.seek(0)
#    return send_file(file_stream, as_attachment=True, attachment_filename="f0016_2_"+"_1_"+".docx")
    return redirect('/')
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        f = request.files['file']
        pdfname = 'temp.pdf'
        jpgname = 'temp.jpg'
        f.save(pdfname)
        images_from_path = convert_from_path(pdfname, dpi=300, last_page=1, first_page =1)
        for page in images_from_path:
            page.save(jpgname)
        image = cv2.imread(jpgname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
        gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = cv2.blur(gradient, (9, 9))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 3))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, None, iterations = 25)
        closed = cv2.dilate(closed, None, iterations = 25)
        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        rect = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)
        x1,x2,x3,x4,y1,y2,y3,y4 =box[0][0],box[1][0],box[2][0],box[3][0],box[0][1],box[1][1],box[2][1],box[3][1]
        top_left_x = min([x1,x2,x3,x4])
        top_left_y = min([y1,y2,y3,y4])
        bot_right_x = max([x1,x2,x3,x4])
        bot_right_y = max([y1,y2,y3,y4])
        img = image[top_left_y+6:bot_right_y+6, top_left_x-10:bot_right_x+10]
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('tempbar.jpg', image_gray)
        code = decode(cv2.imread('ean8_1.png'))[0][0]
        
        c1 = code.decode('ascii')
        nom_form = c1[0:4]
        reg = int(c1[4:7])
        print(nom_form)
        print(reg)
        tablas = 'f' + nom_form + '_2'
        exec("qry = db_session.query(" + tablas + ").filter(" + tablas + ".id==" + str(reg) + ").first()")
        qry1 = locals()['qry']
        qry1.fscan = str(date.today())
        flag_modified(qry1,'fscan')
        db_session.merge(qry1)
        db_session.flush()
        db_session.commit()
        
        os.rename(pdfname, c1 + ".pdf")
        
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
            creds = tools.run_flow(flow, store)
        DRIVE = discovery.build('drive', 'v2', http=creds.authorize(Http()))
        buscar = DRIVE.files().list(q="title='DataBase'",fields='nextPageToken, items(id, title)',pageToken=None).execute()
        folder_id = buscar['items'][0]['id']
        body = {
        'title': c1 + ".pdf",
        'mimeType': 'application/pdf',
        "parents": [{"id": folder_id, "kind": "drive#childList"}] }                 
        media_body = MediaFileUpload(c1 + ".pdf", mimetype='application/pdf', resumable=True)
        res = DRIVE.files().insert(
                    body=body,
                    media_body= media_body).execute()
#        os.remove(c1 + ".pdf")
    return redirect('/')
if __name__ == '__main__':
    app.run()



