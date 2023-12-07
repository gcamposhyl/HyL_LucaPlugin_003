class Transform:
    def __init__(self) -> None:
        pass

    def to_format(self, df):
        try:
            df = df.drop(df.index[1]) # elimino segunda fila, contiene registro no necesario

            df = df.reset_index(drop=True) # reseteo indices de columna

            # Tomar la primera fila como nombres de columnas y eliminar esa fila
            df.columns = df.iloc[0]
            df = df[1:]
           
            # print(f"{df.head()}")

            return df

        except Exception as ex:
            print(str(ex))

    # consolidar ruts
    def join_rut(self, df):
        try:
            df['COL03'] = df['COL03'] + df['COL04'] + df['COL05']

            df['COL09'] = df['COL09'] + df['COL10'] + df['COL11']

            df = df.drop(columns=['COL04', 'COL05', 'COL10', 'COL11'])

            #print(df['COL03'].head())

            # print(f"{df.head()}")

            return df
            
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

            df['COL12'] = df['COL12'].replace(mapping)

            # print(df['COL12'].head())

            return df
        except Exception as ex:
            print(str(ex))
    
    # sumatoria en columnas
    def delete_supp_cols(self, df):
        try:
            # col 12
            # si es 1 => 1=Usufructario
            # si es 2 => 2=Nudo Propietario

            df = df.drop(columns=['REGID', 'TAG', 'ITER_ID', 'TYPE'])

            # print(df['COL12'].head())

            return df
        except Exception as ex:
            print(str(ex))

     