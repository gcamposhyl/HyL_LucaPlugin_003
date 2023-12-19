class Transform:
    def __init__(self) -> None:
        self._ipc_col = []

    def get_ipc_col(self):
        try:
            
            return self._ipc_col 

        except Exception as ex:
            raise Exception(str(ex))
        
    def set_ipc_col(self, value):
        try:

            self._ipc_col = value

        except Exception as ex:
            raise Exception(str(ex))

    def to_format(self, df):
        try:
            # Tomar la primera fila como nombres de columnas y eliminar esa fila
            df.columns = df.iloc[0]
            df = df[1:]
           
            return df

        except Exception as ex:
            raise Exception(str(ex))

    def set_ipc(self, df, ipc, year):
        import pandas as pd
        try:
            # año comercial
            comercial_year = int(year) - 1

            # formateo fecha
            col_date = "COL06"
            df[col_date] = pd.to_datetime(df[col_date], format='%d-%m-%Y')

            # Definir las fechas límite
            first_date = pd.to_datetime(f'01/01/{comercial_year}', format='%d/%m/%Y')
            last_date = pd.to_datetime(f'31/12/{comercial_year}', format='%d/%m/%Y')

            process_lambda = lambda row: (
                                        row[self.get_ipc_col()] / ipc[self.get_string_month(row[col_date])] if first_date <= row[col_date] <= last_date
                                        else (row[self.get_ipc_col()] / ipc["inicial"] if row[col_date] == last_date else row[col_date])
                                    )


            df[self.get_ipc_col()] = df.apply(process_lambda, axis=1)
            
            return df

        except Exception as ex:
            raise Exception(str(ex))

    def get_string_month(self, date):
        """
            Función obtiene nombre de mes en español de fecha ingresada
        """
        try:
            spanish_months = {
            'January': 'enero',
            'February': 'febrero',
            'March': 'marzo',
            'April': 'abril',
            'May': 'mayo',
            'June': 'junio',
            'July': 'julio',
            'August': 'agosto',
            'September': 'septiembre',
            'October': 'octubre',
            'November': 'noviembre',
            'December': 'diciembre'
            }

            english_name = date.strftime('%B')
            spanish_month = spanish_months.get(english_name, english_name.lower())

            return spanish_month
        
        except Exception as ex:
            raise Exception(str(ex))

    # columna de números en formato númerico
    def transform_to_num(self, df):
        import numpy as np
        import pandas as pd
        try:

            ipc_col = np.arange(10, 37).astype(str)
            ipc_col = ['COL' + col.zfill(2) for col in ipc_col] # arreglo que contiene valorers de desde COL05 a COL32

            self.set_ipc_col(ipc_col) # guardo arreglo en variable de constructor, para reutilizarse más adelante

            df[ipc_col] = df[ipc_col].replace('\.', '', regex=True)           

            df[ipc_col] = df[ipc_col].apply(pd.to_numeric)

            return df
        
        except Exception as ex:
            raise Exception(str(ex))

    # lista consignificado de siglas
    def transform_list(self, df):
        try:
            # col 12
            # si es 1 => 1=Usufructario
            # si es 2 => 2=Nudo Propietario

            mapping = {"1": '1= Usufructuario', "2": '2 = Nudo Propietario'}

            df['COL08'] = df['COL08'].replace(mapping)

            return df
        except Exception as ex:
            raise Exception(str(ex))

    def queue_ipc(self, df, ipc):
        try:
            # creo columas vacias
            df["empty01"] = ""
            df["month"] = ""
            df["ipc"] = ""
            col_date = "COL06"

            # relleno columnas vacias
            df["month"] = df.apply(lambda row: self.get_string_month(row[col_date]), axis=1) # inserto mes considerado para dicho registro deflactado

            df["ipc"] = df.apply(lambda row: ipc[self.get_string_month(row[col_date])], axis=1) # inserto factor de ipc considerado para dicho registro deflactado
 
            df[col_date] = df[col_date].dt.strftime('%d-%m-%Y') # transformo fecha en string formateada

            return df
            
        except Exception as ex:
            raise Exception(str(ex))
    
     