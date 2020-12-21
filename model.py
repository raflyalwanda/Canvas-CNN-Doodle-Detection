from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

ENGINE = create_engine("sqlite:///drawpad.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE,
	autocommit=False,
	autoflush=False))

Base = declarative_base()
Base.query = session.query_property()

def create_db():
    '''Creates a new database when called'''
    Base.metadata.create_all(ENGINE)



class Hasil(Base):
    __tablename__ = 'Hasil'
    id = Column(Integer, primary_key=True)
    img_url = Column(String(300), nullable=False)
    hasilAvg = Column(String(20), nullable=False)


    def __repr__(self):
        return "Image_id=%d  Img_url=%r HasilAvg=%r" % (
            self.id,  self.img_url, self.hasilAvg)



class HasilMax(Base):
    __tablename__ = 'HasilMax'
    id = Column(Integer, primary_key=True)
    img_url = Column(String(300), nullable=False)
    hasilMax = Column(String(20), nullable=False)


    def __repr__(self):
        return "Image_id=%d  Img_url=%r HasilMax=%r" % (
            self.id,  self.img_url, self.hasilMax)


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    img_url = Column(String(300), nullable=False)

    def __repr__(self):
        return "Image_id=%d  Img_url=%r" % (
            self.id,  self.img_url)


def save_hasil_to_db(img_url,hasil):
    new_hasil = Hasil( img_url=img_url, hasil=hasilAvg)
    session.add(new_hasil)
    return session.commit()

def save_hasilMax_to_db(img_url,hasilMax):
    new_hasilMax = HasilMax( img_url=img_url, hasilMax=hasilMax)
    session.add(new_hasilMax)
    return session.commit()

def save_image_to_db( img_url):
    new_image = Image( img_url=img_url)
    session.add(new_image)
    return session.commit()

#------------------------------------------------------------
# For the future when there can be multiple images per user.
#------------------------------------------------------------

# def update_image(user_id, img_url):
#     updated_image = session.query(Image).filter(Image.user_id == user_id).first()
#     updated_image.img_url = img_url
#     return session.commit()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
	main()
