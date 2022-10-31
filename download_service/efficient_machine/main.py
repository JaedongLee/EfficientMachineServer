import json
import os
import traceback
from datetime import datetime
from threading import Thread

import requests
from sqlalchemy import insert

from application.tool_service import list_usable_tool_aggregation
from database_init import meta, engine
from definitions import ROOT_DIR
from download_service.efficient_machine.util.download import download_info_builder
from enumation.ToolSourceTypeEnum import ToolSourceTypeEnum


def batch_download_latest_release_asset():
    tool_aggregations = list_usable_tool_aggregation()

    github_tool_aggregations = list(
        filter(lambda tool_aggregation: tool_aggregation.tool_source.type == ToolSourceTypeEnum.GITHUB.value,
               tool_aggregations))
    for github_tool_aggregation in github_tool_aggregations:
        download_latest_tool(github_tool_aggregation)

    intellij_platform_tool_aggregations = list(
        filter(lambda tool_aggregation: tool_aggregation.tool_source.type == ToolSourceTypeEnum.INTELLIJ_PLATFORM.value,
               tool_aggregations))
    for intellij_platform_tool_aggregation in intellij_platform_tool_aggregations:
        download_latest_tool(intellij_platform_tool_aggregation)


def download_latest_tool(tool_aggregation):
    tool = tool_aggregation.tool
    tool_source = tool_aggregation.tool_source
    if ToolSourceTypeEnum.CUSTOM != tool_source.type:
        download_latest_not_custom_tool(tool_aggregation)
    # elif 'Process Hacker' == tool.name:


def download_latest_not_custom_tool(tool_aggregation):
    tool = tool_aggregation.tool
    tool_source = tool_aggregation.tool_source
    url_for_release = tool_source.url_for_release
    release_asset_regex = tool_source.release_asset_regex
    try:
        response = requests.get(url_for_release)
        if response.status_code == 200:
            # 启动现场下载工具
            download_info = None
            if ToolSourceTypeEnum.GITHUB.value == tool_source.type:
                download_info = download_info_builder.build_github(tool_aggregation, response)
            elif ToolSourceTypeEnum.INTELLIJ_PLATFORM.value == tool_source.type:
                download_info = download_info_builder.build_intellij_platform(tool_aggregation, response)
            else:
                raise Exception('找不到该业务源类型')
            thread = Thread(target=download_tool,
                            args=(download_info, tool_aggregation))
            print("启动线程: " + thread.name)
            thread.start()
        else:
            issue_message_json = {'exception_url': url_for_release, 'status_code': response.status_code,
                                  'response_message': response.text}
            record_issue(issue_message_json, tool.id, tool.name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')
    except:
        issue_message_json = {'exception_url': url_for_release, 'exception_stack': traceback.format_exc()}
        record_issue(issue_message_json, tool.id, tool.name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')


def download_tool(download_info, tool_aggregation):
    # 初始化数据库
    tool_table = meta.tables['Tool']

    # 下载工具
    download_url = download_info.url
    tool_file_name = download_info.file_name
    version = download_info.version
    tool = tool_aggregation.tool
    tool_name = tool.name
    tool_id = tool.id
    directory = f'{ROOT_DIR}/download_service/resource/tool_program/{tool_name}'.format(ROOT_DIR=ROOT_DIR,
                                                                                        tool_name=tool_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
    tool_file_path = f'{ROOT_DIR}/download_service/resource/tool_program/{tool_name}/{tool_file_name}' \
        .format(ROOT_DIR=ROOT_DIR, tool_name=tool_name, tool_file_name=tool_name)
    if os.path.exists(tool_file_path):
        print(f"文件已存在. {tool_file_name}".format(tool_file_name=tool_file_name))
        return
    try:
        response = requests.get(download_url, verify=False)
        if response.status_code == 200:
            with open(tool_file_path, 'wb') as f:
                f.write(response.content)
            update_stmt = tool_table.update().where(tool_table.c.Id == tool_id) \
                .values(FileName=tool_file_name, Version=version,
                        LastUpdatedDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            engine.execute(update_stmt)
            print(f"下载完成. {tool_file_name}".format(tool_file_name=tool_file_name))
        else:
            issue_message_json = {'download_url': download_url, 'status_code': response.status_code,
                                  'response_message': response.text}
            record_issue(issue_message_json, tool_id, tool_name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')
    except:
        print(traceback.format_exc())
        issue_message_json = {'exception_url': download_url, 'exception_stack': traceback.format_exc()}
        record_issue(issue_message_json, tool.id, tool.name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')


def record_issue(issue_message_json, tool_id, tool_name, issue_type, stage):
    program_issue_record = meta.tables['ServerIssueRecord']
    issue_message = json.dumps(issue_message_json)
    insert_issue_record_stmt = insert(program_issue_record) \
        .values(ToolId=tool_id, ToolName=tool_name, Type=issue_type, Stage=stage, IssueMessage=issue_message)
    engine.execute(insert_issue_record_stmt)


if __name__ == '__main__':
    batch_download_latest_release_asset()
