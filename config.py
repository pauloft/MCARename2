import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'Lk9Dqmymz$KC%=u'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dbdata.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    INSPECTIONS_DATAFILE = 'inspections.json'
    MH_INSPECTIONS_FILE = 'manhole_inspections.json'
    RENAMED_FILES_DICTIONARY = 'renamed_files_dictionary.json'
    


config = {
    'dev_cfg' : Config,
    
    'default' : Config
}