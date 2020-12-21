from flask import Flask, render_template, request, session as flask_session, g, send_from_directory, redirect,url_for
#from flask.ext.socketio import SocketIO, emit, send
from flask_socketio import SocketIO, emit, send
import model
import os
import datetime
import sqlalchemy as db
from sqlalchemy.sql import select
import TestingMaxPooling

UPLOAD_FOLDER = 'static/dataset'
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# should probably hide this secret key at some point?
app.config['SECRET_KEY'] = 'TROLOLOLOLOLO!'
socketio = SocketIO(app)



@app.route('/', methods=['GET', 'POST'])
def sign_up_log_in():
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/hasil', methods=['GET'])
def tes():

    #if request.method == 'GET':
      #  import TestingMaxPooling
    result_tes = TestingMaxPooling.testing()
    print(result_tes)
      
        
    engine = db.create_engine('sqlite:///drawpad.db')
    connection = engine.connect()
    metadata = db.MetaData()

    coba = db.Table('HasilMax',metadata,autoload=True,autoload_with = engine)
    s  = select([coba]).order_by(db.desc(coba.columns.img_url.label('img_url') )).limit(1)
    result = connection.execute(s)
    row = result.fetchall()
    x = row
    print(x)

    coba = db.Table('Hasil',metadata,autoload=True,autoload_with = engine)
    s  = select([coba]).order_by(db.desc(coba.columns.img_url.label('img_url') )).limit(1)
    result = connection.execute(s)
    row = result.fetchall()
    y = row
    print(y)
    
    return render_template('hasil.html', value = x, data = y)


@app.route('/Start', methods=['GET'])
def BackCanvas():
     
     return redirect(url_for('sign_up_log_in'))
        


                
@app.route('/save', methods=['POST'])
def save_image():
    img = request.files['image']
    if img:
        # mac version below
        # filename = g.username + ".jpg"
        # fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Windows version below -- unsure why there is a difference between mac/windows
        dateObj = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        fullpath = app.config['UPLOAD_FOLDER'] + "/" + dateObj + ".jpg"
        img.save(fullpath)
        image =  model.save_image_to_db(fullpath)
    #return TestingMaxPooling
        print(fullpath)
    return "Failure"
    
    

    
   
    

@socketio.on('broadcastImage')
def broadcast_image(data):
    emit('loadImage', data, broadcast=True)

@socketio.on('reset')
def reset(data):
    print("Reset")
    emit('resetCanvas', data, broadcast=True)

# Offers the load() javascript function the path it needs
@app.route('/static/img/<path:path>')
def send_user_image(path):
    return send_from_directory('static/img', path)

@socketio.on('connection')
def listen_send_all(data):
    emit('new user')

@socketio.on('mousemove')
def brdcast_moving(data):
    emit('moving', data, broadcast=True)

@socketio.on('mouseup')
def brdcast_stop(data):
    emit('stopping', data, broadcast=True)

@socketio.on('broadcastColor')
def brdcast_color(data):
    emit('strokeColor', data, broadcast=True)

@socketio.on('deleteUnloaded')
def delete_unloaded(data):
    emit('deleteRemoteUser', data, broadcast=True)

PORT=int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=PORT)
