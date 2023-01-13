import itertools
import json
import os.path
import shutil
import traceback
from datetime import datetime
from pathlib import Path
from unittest import TestCase

import requests
import scrapy
from snowflake import SnowflakeGenerator
from sqlalchemy import MetaData, create_engine

from definitions import ROOT_DIR, CLIENT_ROOT_DIR, TOOLS_DOWNLOAD_DIRECTORY
from download_service.efficient_machine import main
from download_service.efficient_machine.main import download_latest_not_custom_tool, download_tool_postprocess
from download_service.efficient_machine.test.data_creator import create_ditto_tool_aggregation, \
    create_ditto_download_info


class Test(TestCase):
    def test_download_latest_not_custom_tool(self):
        ditto_tool_aggregation = create_ditto_tool_aggregation()
        download_latest_not_custom_tool(ditto_tool_aggregation)

    def test_batch_download_latest_release_asset(self):
        # 删除 tool_program 下的文件
        path = f'{CLIENT_ROOT_DIR}/EfficientMachine/Resources/Tools/Program/'
        shutil.rmtree(path)
        os.mkdir(path)

        main.batch_download_latest_release_asset()

    def test_batch_download__not_existed_latest_release_asset(self):
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

    def test_unzip(self):
        shutil.unpack_archive(
            "D:/OneDrive/Project/Self/EfficientMachine/Service/download_service/resource/tool_program/Office Tool Plus/Office_Tool_with_runtime_v9.0.3.7.zip")

    def test_download_tool_postprocess(self):
        ditto_tool_aggregation = create_ditto_tool_aggregation()
        ditto_download_info = create_ditto_download_info()
        download_tool_postprocess(ditto_tool_aggregation, ditto_download_info)

    def test_dir(self):
        print(CLIENT_ROOT_DIR)

    def test_temp(self):
        now = datetime.now()
        print(now)
