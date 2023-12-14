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

            # print(df['COL12'].head())

            return df
        except Exception as ex:
            print(str(ex))
         