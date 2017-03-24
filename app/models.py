import os
from datetime import datetime

from . import db
from config import Config as cfg

# expected database file extension - change to '.accdb' based on your file extension
DB_FILE_EXT = '.mdb'

class MCA(object):
    data_directory = ''
    dbfilename = ''
    dbcrsr = None

    def __init__(self, datapath=''):
        print(datapath)
        self.data_directory,self.dbfilename = os.path.split(self._verify_path(datapath))
        
        

    def _verify_path(self, datapath):
        """
        Verify that the path (datapath) to the MS Access database file exists
        """

        # Copy the path argument to local variable
        target = ''
        copy_datapath = datapath
        # Check if it is a file or a directory
        if os.path.isdir(copy_datapath):
            items = os.listdir(copy_datapath)
            arr_file = [item for item in items if str(item).endswith(DB_FILE_EXT)]
            # if more than ONE Access db file exists, take t he first one!
            if len(arr_file) > 0:
                target = os.path.abspath(os.path.join(copy_datapath, arr_file[0]))
        elif(str(copy_datapath).endswith(DB_FILE_EXT)):
            target = os.path.abspath(copy_datapath)

        return target


    def _get_dbcursor(self):
        """
        Get a cursor to access the MS Access database file records. Return None
        if the path to the database file is not valid
        """
        if self.dbfilename != '':
            path = os.path.join(self.data_directory, self.dbfilename)
            # verify path to database file exists
            if os.path.exists(path):
                conn_str = (
                    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' 
                    r'DBQ=' + path + ';'
                )
                cnxn = pyodbc.connect(conn_str)
                self.dbcrsr = cnxn.cursor()
                return self.dbcrsr
        return None


    def create_inspection_list(self):
        """
        Create a dictionary of inspection image data keyed on inspection number, 
        and find EMPTY inspections
        """
        insp_dict = {}
        count_insp = 0
        insp_too_few_imgs = []
        insp_more_than_few_imgs = []
        empty_insp = []

        if os.path.exists(self.data_directory):
            # traverse all inspection folders and find the image files
            for root, dirs, files in os.walk(self.data_directory):
                if len(files):
                    # get the inspection number from the first file in the files list 
                    # e.g. if files[0] is 'inspection-26881_image_Header.0.jpg', we get inspection-26881
                    insp_num = str(files[0].split('/'[-1])).split('_'[0])
                    # We next split 'inspection-26881' to obtain the dictionary key: 26881
                    key = str(insp_num).split('-')[-1]
                    # get the name(s) of all image files for this inspection
                    imgs = [fname for fname in files]
                    # increment the inspection count
                    count_insp += 1
                    # Are there images for this inspection? If so, update the insp_dict, or update the empty_insp list
                    if len(imgs):
                        insp_dict[key] = imgs
                    else:
                        empty_insp.append(key)
                    # Is the number of images less than 3 or greater than 3, or equal to 3? 
                    if len(imgs) < 3:
                        insp_too_few_imgs.append(key)
                    elif(len(imgs) > 3):
                        insp_more_than_few_imgs.append(key)
                # Otherwise, if the sub-folder inside the inspection folder is empty
                elif(len(dirs)==0 and len(files)==0):
                    key = str(root).split('-')[-1]
                    key = str(key).split('_')[0]
                    empty_insp.append(key)

        # Now we have all our data so we write all this to disk
        import json
        # Write the inspection data in JSON format to a file
        with open(os.path.join(self.data_directory, cfg[INSPECTIONS_DATAFILE]), w) as f:
            json.dump(insp_dict, f)
        