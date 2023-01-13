import itertools
import json
import os
import shutil
import traceback
from datetime import datetime
from threading import Thread

import requests
from snowflake import SnowflakeGenerator
from sqlalchemy import insert

from application.tool_service import list_usable_tool_aggregation
from database_init import meta, engine
from definitions import TOOLS_DOWNLOAD_DIRECTORY
from download_service.efficient_machine.util.download import download_info_builder
from enumation.FileExtensionNameEnum import FileExtensionNameEnum
from enumation.ReleaseTypeEnum import ReleaseTypeEnum
from enumation.ToolSourceTypeEnum import ToolSourceTypeEnum

DOWNLOAD_SESSION_ID = next(SnowflakeGenerator(42))


def batch_download_latest_release_asset():
    tool_aggregations = list_usable_tool_aggregation()

    # 删除旧工具集合
    shutil.rmtree(TOOLS_DOWNLOAD_DIRECTORY)
    os.mkdir(TOOLS_DOWNLOAD_DIRECTORY)

    # 下载最新工具集合
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
                raise Exception('找不到该工具源类型')
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
    file_name = download_info.file_name
    file_extension_name = download_info.file_extension_name
    version = download_info.version
    tool = tool_aggregation.tool
    tool_name = tool.name
    tool_id = tool.id
    directory_path = download_info.directory_path
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    file_path = download_info.file_path
    if os.path.exists(file_path):
        print(f"文件已存在. {file_name}.{file_extension_name}"
              .format(file_name=file_name, file_extension_name=file_extension_name))
        return
    try:
        response = requests.get(download_url, verify=False)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            update_stmt = tool_table.update().where(tool_table.c.Id == tool_id) \
                .values(FileName=file_name, Version=version,
                        LastUpdatedDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        FileExtensionName=file_extension_name)
            engine.execute(update_stmt)
            print(f'下载完成. {file_name}.{file_extension_name}'
                  .format(file_name=file_name, file_extension_name=file_extension_name))
            download_tool_postprocess(tool_aggregation, download_info)
        else:
            issue_message_json = {'download_url': download_url, 'status_code': response.status_code,
                                  'response_message': response.text}
            record_issue(issue_message_json, tool_id, tool_name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')
    except:
        print(traceback.format_exc())
        issue_message_json = {'exception_url': download_url, 'exception_stack': traceback.format_exc()}
        record_issue(issue_message_json, tool.id, tool.name, 'DOWNLOAD_LATEST_TOOLS', 'GET_TOOL_ASSET')


def download_tool_postprocess(tool_aggregation, download_info):
    tool = tool_aggregation.tool
    if is_tool_portable_and_zip(tool):
        unpack_zip(tool_aggregation, download_info)
        return
    if is_tool_installer(tool):
        tool_table = meta.tables['Tool']


def is_tool_portable_and_zip(tool):
    return ReleaseTypeEnum.PORTABLE.value == tool.release_type and \
        FileExtensionNameEnum.ZIP.value == tool.file_extension_name


def is_tool_installer(tool):
    return ReleaseTypeEnum.INSTALLER.value == tool.release_type


def unpack_zip(tool_aggregation, download_info):
    tool_name = tool_aggregation.tool.name
    file_name = download_info.file_name
    file_extension_name = download_info.file_extension_name
    directory_path = download_info.directory_path
    unpacked_directory_path = f'{directory_path}/{file_name}'
    file_path = download_info.file_path
    if os.path.exists(unpacked_directory_path):
        shutil.rmtree(unpacked_directory_path)
    shutil.unpack_archive(file_path, unpacked_directory_path)
    os.remove(file_path)
    print(f'{file_name}.{file_extension_name} 已解压'
          .format(file_name=file_name, file_extension_name=file_extension_name))


def record_issue(issue_message_json, tool_id, tool_name, issue_type, stage):
    program_issue_record = meta.tables['ServerIssueRecord']
    issue_message = json.dumps(issue_message_json)
    now = datetime.now()
    insert_issue_record_stmt = insert(program_issue_record).values(
        ToolId=tool_id,
        ToolName=tool_name,
        Type=issue_type,
        Stage=stage,
        IssueMessage=issue_message,
        DownloadSessionId=DOWNLOAD_SESSION_ID,
        CreatedTime=now
    )
    engine.execute(insert_issue_record_stmt)


if __name__ == '__main__':
    batch_download_latest_release_asset()
