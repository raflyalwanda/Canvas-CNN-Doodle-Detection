
import cv2, glob
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import sqlalchemy as db
from sqlalchemy.sql import select

def testing():
    print("="*10 + "TEST MAX POLL start ")
    engine = db.create_engine('sqlite:///drawpad.db')
    connection = engine.connect()
    metadata = db.MetaData()
    drawpad = db.Table('images',metadata,autoload=True,autoload_with = engine)
    s = select([drawpad]).order_by(db.desc(drawpad.columns.img_url.label('img_url') )).limit(1)
    result = connection.execute(s)
    row = result.fetchone()
    # print(row['img_url'])

    x = row['img_url']
    ImgAddress = x[15:]


    print('testing')
    print(ImgAddress)

    testing ="C:/Canvas/static/dataset/" + str(ImgAddress)
    print(testing)


    images=glob.glob(testing)

    for image in images:
        img = cv2.imread(image,0)

        re=cv2.resize(img, (int(img.shape[1]/25), int(img.shape[0]/18.75)), interpolation = cv2.INTER_AREA)

        cv2.imshow("cek",re)

        cv2.waitKey(500)
        cv2.destroyAllWindows()

        image = "testing.jpg"
        
        cv2.imwrite("resize/"+image, re)




    CATEGORIES = ["Baju", "Celana", "Kupukupu", "Kursi", "Sepeda"]

    def data(filepath):
        IMG_SIZE = 32
        img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        #plt.imshow(img_array, cmap = "gray")
        #plt.show()
        return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    

    model = tf.keras.models.load_model("maxpooling_train_data.model")
    prediction = model.predict([data("C:/Canvas/resize/testing.jpg")])
    J = CATEGORIES[np.argmax(prediction)]
    print(J)


    model = tf.keras.models.load_model("avgpooling_train_data.model")
    prediction = model.predict([data("C:/Canvas/resize/testing.jpg")])
    K = CATEGORIES[np.argmax(prediction)]
    print(K)



    coba = db.Table('Hasil',metadata,autoload=True,autoload_with = engine)
    ins = coba.insert()
    ins = coba.insert().values(img_url=x, hasilAvg=J)
    str(ins)
    ins.compile().params 
    tampil=connection.execute(ins) 
    print('disini')

    coba = db.Table('HasilMax',metadata,autoload=True,autoload_with = engine)
    ins = coba.insert()
    ins = coba.insert().values(img_url=x, hasilMax= K)
    str(ins)
    ins.compile().params 
    tampil=connection.execute(ins)


    return J,K

