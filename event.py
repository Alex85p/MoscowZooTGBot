import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

# Установите путь к вашему файлу JSON с учетными данными
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Авторизуйтесь и откройте таблицу
service = build('sheets', 'v4', credentials=credentials)

# Укажите ID таблицы
spreadsheet_id = '1cXcNL1WD8HWM_Q64881-1GHyvPb3KLbJzacGgLDMR18'

# Установите диапазон ячеек, где находятся вопросы и ответы
range_name = 'вопросы хищники!A3:C'


# Функция для получения вопросов и ответов из таблицы
def get_questions():
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values
