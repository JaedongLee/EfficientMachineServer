import json
import os.path
import traceback
from datetime import datetime
from unittest import TestCase

import requests
import scrapy
from sqlalchemy import MetaData, create_engine

from download_service.efficient_machine import main
from download_service.efficient_machine.util.download.DownloadInfo import DownloadInfo
from dto.ToolAggregationDTO import ToolAggregationDTO
from entity.ToolEntity import ToolEntity


class Test(TestCase):
    def test_download_tool_from(self):
        tool_entity = ToolEntity()
        tool_entity.Id = 1
        tool_entity.Name = 'Ditto'
        tool_aggregation_dto = ToolAggregationDTO(tool_entity, None, None)
        download_info = DownloadInfo(
            'https://github.com/sabrogden/Ditto/releases/download/3.24.214.0/DittoPortable_3_24_214_0.zip',
            'DittoPortable_64bit_3_24_214_0.zip', '3.24.214.0')
        main.download_tool(download_info, tool_aggregation_dto)

    def test_download_latest_release(self):
        main.batch_download_latest_release_asset()

    def test_sqlalchemy(self):
        engine = create_engine('sqlite:///resource/database/EfficientMachine.db?check_same_thread=False')
        meta = MetaData(bind=engine)
        MetaData.reflect(meta)
        tool_table = meta.tables['Tool']
        update_stmt = tool_table.update().where(tool_table.c.Id == '1').values(
            FileName='DittoPortable_64bit_3_24_214_0.zip')
        engine.execute(update_stmt)

    def test_json(self):
        json_object = {'a': 'a_value', 'b': 'b_value'}
        json_string = json.dumps(json_object)

    def test_temp(self):
        path = '8006/228001/Material_Theme_UI-7.11.0.zip'
        file_name = os.path.basename(path)
        print(file_name)

    def test_scrapy(self):
        response = scrapy.Request(url='https://processhacker.sourceforge.io/downloads.php', callback=self.parse)

    def test_requests_get(self):
        download_url = 'https://www.listary.com/download/Listary.exe'
        try:
            response = requests.get(download_url, verify=False)
        except:
            print(traceback.format_exc())

    def test_a(self):
        x = datetime.now()
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
