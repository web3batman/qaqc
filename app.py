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

app= Flask(__name__)
app.register_blueprint(f0016_2_app)

@app.route("/")
def home():
    disc = gd.items_folder(service,'Formatos_Calidad')
    disc = [x['title'] for x in disc]
    return render_template('disciplina_list.html', table=disc )

if __name__ == '__main__':
    app.run()



