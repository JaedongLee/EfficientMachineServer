import os
import re

from definitions import CLIENT_ROOT_DIR
from download_service.efficient_machine.util.download.DownloadInfo import DownloadInfo


def build_github(tool_aggregation, releases_response):
    tool_source = tool_aggregation.tool_source
    release_asset_regex = tool_source.release_asset_regex
    assets = releases_response.json()['assets']
    version = releases_response.json()['tag_name']
    asset = next(filter(lambda x: re.search(release_asset_regex, x['name']) is not None, assets))
    file_full_name = asset['name']
    split_tup = os.path.splitext(file_full_name)
    file_name = split_tup[0]
    file_extension_name = split_tup[1][1:]
    download_info = DownloadInfo(asset['browser_download_url'], file_name, version, '', '', file_extension_name)
    build_path(tool_aggregation, download_info)
    return download_info


def build_intellij_platform(tool_aggregation, releases_response):
    tool = tool_aggregation.tool
    tool_source = tool_aggregation.tool_source
    latest_update = releases_response.json()[0]
    file_relative_path = latest_update['file']
    version = latest_update['version']
    url = f'https://plugins.jetbrains.com/files/{file_relative_path}'
    file_full_name = os.path.basename(file_relative_path)
    split_tup = os.path.splitext(file_full_name)
    file_name = split_tup[0]
    file_extension_name = split_tup[1][1:]
    download_info = DownloadInfo(url, file_name, version, '', '', file_extension_name)
    build_path(tool_aggregation, download_info)
    return download_info


def build_path(tool_aggregation, download_info):
    tool = tool_aggregation.tool
    tool_name = tool.name
    file_name = download_info.file_name
    file_extension_name = download_info.file_extension_name
    directory_path = '{client_root_dir}/EfficientMachine/EfficientMachine/Resources/Tools/Program/{tool_name}' \
        .format(client_root_dir=CLIENT_ROOT_DIR, tool_name=tool_name)
    file_path = '{client_root_dir}/EfficientMachine/EfficientMachine/Resources/Tools/Program/{tool_name}/{file_name}.{file_extension_name}'.format(
        client_root_dir=CLIENT_ROOT_DIR, tool_name=tool_name, file_name=file_name,
        file_extension_name=file_extension_name)
    download_info.directory_path = directory_path
    download_info.file_path = file_path
