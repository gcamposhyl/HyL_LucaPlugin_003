class Transform:
    def __init__(self) -> None:
        pass

    def to_format(self, df):
        try:
            # Tomar la primera fila como nombres de columnas y eliminar esa fila
            df.columns = df.iloc[0]
            df = df[1:]
           
            return df

        except Exception as ex:
            print(str(ex))

    def set_ipc(self, df, ipc):
        import numpy as np
        import pandas as pd
        try:
            # para cada registro*
            ipc_col = np.arange(10, 37).astype(str)
            ipc_col = ['COL' + col.zfill(2) for col in ipc_col] # arreglo que contiene valorers de desde COL05 a COL32

            df[ipc_col] = df[ipc_col].replace('\.', '', regex=True)           

            df[ipc_col] = df[ipc_col].apply(pd.to_numeric)

            # formateo fecha
            col_date = "COL06"
            df[col_date] = pd.to_datetime(df[col_date], format='%d-%m-%Y')

            # Definir las fechas límite
            first_date = pd.to_datetime('01/01/2022', format='%d/%m/%Y')
            last_date = pd.to_datetime('31/12/2023', format='%d/%m/%Y')
  
            process_lambda = lambda row: row[ipc_col] * ipc[self.get_string_month(row[col_date])] if first_date <= row[col_date] <= last_date else row[ipc_col]

            df[ipc_col] = df.apply(process_lambda, axis=1)

            df[col_date] = df[col_date].dt.strftime('%Y-%m-%d')
            
            return df

        except Exception as ex:
            print(str(ex))

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
            print(str(ex))

    # columna de números en formato númerico
    def transform_to_num(self, df):
        try:
            return df
        except Exception as ex:
            print(str(ex))

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
            print(str(ex))
    
     