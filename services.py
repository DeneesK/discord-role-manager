from api_google import get_google_service
from config import SHEET_ID, COLUMNS


class NamesService:
    def __init__(self, 
                 service = get_google_service(),
                 sheet_id: str = SHEET_ID,
                 columns: str = COLUMNS
                 ):
        self.service = service
        self.sheet_id = sheet_id
        self.columns = columns
    
    def _get_sheet(self):
        return self.service.spreadsheets()
    
    def get_names(self) -> set:
        sheet = self._get_sheet()
        data = sheet.values().get(spreadsheetId=self.sheet_id, range=self.columns).execute()
        names = {v[0] for v in data['values'] if v}
        return names
    
    def check_name(self, name: str) -> bool:
        return name in self.get_names()
