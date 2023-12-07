from components.utils.driveUtil import Drive

class File_manager:
    def __init__(self) -> None:
        pass

    def copy_file(self, folder_id, gsheet_id, name_gsheet):
        try:

            drive = Drive()

            new_gsheet_id = drive.set_gsheet_in_folder(folder_id, gsheet_id, name_gsheet)

            return new_gsheet_id
        except Exception as ex:
            print(str(ex.with_traceback)) 