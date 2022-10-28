'''
References
    General: https://workflowy.com/#/e3430fc52a8d
'''


import mysql.connector as cnctr
from utils.helpers import *
from utils.sqlreader import *
from __future__ import print_function
import pandas as pd 
import sys
import arcpy


# %% globals
config = {
  'user': 'root',
  'password': '300667',
  'host': '127.0.0.1',
  'raise_on_warnings' : True
  }

db_name = "rivereyes" 
sql_path = '../sql/'

# ArcMap Globals
fgdb_dir = "something" # update / conceivably hold the geodatabase in memory as opposed to storing it in a directory? 
fgdb_nm = "riverseye_gdb.gdb"

# %% Define connection, prepare cursor, create database
cnx = cnctr.connect(**config)
crsr = cnx.cursor()
createDB(db_name, crsr)
cnx.database = db_name

# %% ArcMap
#  create file geodatabase
arcpy.CreateFileGDB_management(fgdb_dir, "riverseye_gdb.gdb", "9.2")

# import database data into dictionary to load into feature datasets
features = { 'class1' : 
                    {'name1', 
                    { 'arr' : '<data>' }, 
                    { 'conversion' : '<convtype>'},
                    { 'metadata'  : '<metadata>'}}, 
             'class2' : , 
             'class3' : , }

# create features and feature datasets
for fd in features.keys():
    # create feature datasets
    arcpy.CreateFeatureDataset_management(sys.path.join(fgdb_dir, fgdb_nm), fd)
    for fc in fd:
        nm = fc.key()
        dt = fc[nm]['arr']
        conv = fc[nm]['conversion']

        if conv == 'NpToFeature':
            lyr = arcpy.da.NumPyArrayToFeatureClass(array, outFC, ['XY'], SR)
        if conv == 'NpToTable':
            lyr = arcpy.da.NumPyArrayToTable(struct_array, 'c:/data/f.gdb/array_output')
        # turn layer into 
        
        # create feature classes
        arcpy.FeatureClasstoGeodatabase_conversion(lyr, sys.path.join(fgdb_dir, fgdb_nm, nm))
        del lyr





