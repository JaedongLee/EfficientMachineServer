from flask import Flask, jsonify, send_file

from application import tool_service
from application.tool_service import get_tool_by_tool_name
from definitions import ROOT_DIR
from mapping.tool_aggregation_mapping import dtos_to_dicts

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/tool/info/list')
def list_tool_infos():
    tool_aggregation_dtos = tool_service.list_usable_tool_aggregation()
    tool_aggregation_dicts = dtos_to_dicts(tool_aggregation_dtos)
    return jsonify(tool_aggregation_dicts)


@app.route('/tool/<tool_name>/file')
def download_tool_file(tool_name):  # put application's code here
    tool = get_tool_by_tool_name(tool_name)
    path = f'{ROOT_DIR}/download_service/resource/tool_program/{tool_name}/{tool.file_name}'
    return send_file(path)


if __name__ == '__main__':
    app.run()
