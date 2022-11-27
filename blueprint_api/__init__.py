from flask import Blueprint

from blueprint_api.api.import_data import import_data
from blueprint_api.api.export_data import export_data_sql, export_data_pandas


blueprint_api = Blueprint('blueprint_api', __name__,
                          template_folder='templates',)


blueprint_api.add_url_rule('/import/xlsx/', 'import_data',
                           import_data, methods=['POST'])

blueprint_api.add_url_rule('/export/sql/', 'export_data_sql',
                           export_data_sql, methods=['GET'])

blueprint_api.add_url_rule('/export/pandas/', 'export_data_pandas',
                           export_data_pandas, methods=['GET'])
