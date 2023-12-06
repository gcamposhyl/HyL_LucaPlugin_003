from components.utils.gsheetUtil import Gsheet
from components.utils.driveUtil import Drive
import pandas as pd


class Ddjj_1948:

    def __init__(self, sc_id, sc_name) -> None:
        self._sc_id = sc_id
        self._sc_name = sc_name

    def get_sc_id(self):
        try:
            return self._sc_id
        except Exception as ex:
            print(str(ex)) 

    def get_sc_name(self):
        try:
            return self._sc_name
        except Exception as ex:
            print(str(ex)) 

    def get_ddjj1948(self):

        # ESTAS VARIABLES VIENEN EN EL MENSAJE, SOLO ESTAN PARA TEST

        USER_ID = "123456"

        CARD_ID = "456789"

        TEMPLATE_FOLDER_ID = "1crLw_nmcOXYtVElAfxJgNuqQEs-G-1wv"

        OUTPUT_FOLDER_ID = "1F496ZgJi6I_Pn0NQvOmklIgYJ649B17L"

        PLUGIN_NAME = "ddjj_outputs"
        
        try:
            # obtengo datos de scraping, aqui me llagara este mensaje, solo es para test
            scraping_data = Gsheet().getSheetByNameSheet(self.get_sc_id(), self.get_sc_name())
            # transformo en df
            df_scraping_data = pd.DataFrame(scraping_data)

            #print(df_scraping_data.head())

            # valido datos relevantes

            # id de carpeta donde se dejan los archivos nuevos
            new_folder_id = self.output_directory(OUTPUT_FOLDER_ID, PLUGIN_NAME, USER_ID, CARD_ID)



            # carpeta de proceso, estructura sera: plugin_name/user_id/card_id/file
                # si existe uso esa
                # si no existe creo una
            
            # retorno id de dicha carpeta

            # obtengo template planilla

            year = "2023" # test año de proceso solicitado

            temp_files = self.get_template(TEMPLATE_FOLDER_ID, year) # nombre e id de template según año

            # creo copia de planilla template

            # inserto datos en copia

            # obtengo url

            # retorno url

            
            #df_temp_files = pd.DataFrame(temp_files)
            #print(f"dato encontrado: {temp_files}")

        except Exception as ex:
            print(str(ex)) 

    def get_template(self, folder_id, year):
        
        try:
            name_id_files = Drive().get_files_in_folder(folder_id)

            matches = list(filter(lambda x: year in x[0], name_id_files))
            return matches[0] if matches else None
             
        except Exception as ex:
            print(str(ex)) 

    def output_directory(self, folder_id, plugin_name, user_id, card_id):
        drive = Drive()
        try:
            # consulto carpeta plugin_name/
            plugin_folder = drive.get_subfolders(folder_id)
            if len(plugin_folder) == 0: # valido carpeta plugin_name
                # crea todas las carpetas
                print("crea todo: plugin_name/user_id/card_id")
                new_plugin_folder = drive.create_folder(plugin_name, folder_id)
                new_user_folder = drive.create_folder(user_id, new_plugin_folder) 
                new_card_id = drive.create_folder(card_id,new_user_folder)
                
            else:
                matches = list(filter(lambda x: plugin_name in x[0], plugin_folder))
                plugin_folder = matches[0] if matches else None

                if plugin_folder is None: # valido carpeta plugin_name/user_id
                    # crea carpetas plugin_name/user_id/card_id                    
                    pass

                else:
                    # busco carpetas dentro de plugin_name
                    user_folders = drive.get_subfolders(plugin_folder[1]) # carpetas de usuarios
                    if len(user_folders) == 0: # valido carpeta plugin_name
                        # crea todas las carpetas
                        print("crea todo: plugin_name/user_id/card_id")
                        pass
                        # busco id de usuario
                    else:
                        matches = list(filter(lambda x: user_id in x[0], user_folders))
                        user_folder = matches[0] if matches else None
                        if user_folder is None: # valido carpeta plugin_name/user_id
                            # crea carpetas plugin_name/user_id/card_id                    
                            pass
                        else:
                            card_folders = drive.get_subfolders(user_folder[1])
                            matches = list(filter(lambda x: card_id in x[0], card_folders))




                #print(f"plugin folders: {plugin_folder}")
                    # reviso si contiene la carpeta user_id
                        # si la contiene reviso si existe plugin_name/user_id/card_id:
                            # si existe uso ese id
                            # si no existe creo la carpeta
                        # si no creo las carpetas plugin_name/user_id/card_id
                pass
        except Exception as ex:
            print(str(ex)) 