import os
from io import StringIO
from io import BytesIO
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build



class Data_manipulation:
    def __init__(self) -> None:
        pass

    def row_orderer(self, dictionary):
        try:
            row = []
            order = ['ANIO', 'MES', 'DIA', 'COL01', 'COL02', 'COL03', 'COL04', 'COL05', 'COL06', 'COL07', 'COL08', 'COL09', 'COL10', 'COL11', 'COL12', 'COL13', 'COL14', 'COL15', 'COL16', 'COL17', 'COL18', 'COL19', 'COL20', 'COL21', 'COL22', 'COL23', 'COL24', 'COL25', 'COL26', 'COL27', 'COL28', 'COL29', 'COL30', 'COL31', 'COL32', 'COL33', 'COL34', 'COL35', 'COL36', 'COL37', 'COL38', 'COL39', 'COL40']
            return row
        except Exception as error :
           print("Error in read_sientos_in_drive()", error) 
