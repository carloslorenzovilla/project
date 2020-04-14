# core/views.py
from flask import render_template,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    #local beer news ticker
    #news  = data_from_some_API
    return render_template('index.html') #news=news

@core.route('/info')
def info():
    return render_template('info.html')
