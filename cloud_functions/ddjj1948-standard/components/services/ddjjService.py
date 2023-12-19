class Transform:

    def to_format(self, df):
        try:

            # Tomar la primera fila como nombres de columnas y eliminar esa fila
            df.columns = df.iloc[0]
            df = df[1:]
           
            return df

        except Exception as ex:
            raise Exception(str(ex))


    # columna de números en formato númerico
    def transform_to_num(self, df):
        import numpy as np
        import pandas as pd
        try:

            ipc_col = np.arange(10, 37).astype(str)
            ipc_col = ['COL' + col.zfill(2) for col in ipc_col] # arreglo que contiene valorers de desde COL05 a COL32

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
         