import os
import re

from download_service.efficient_machine.util.download.DownloadInfo import DownloadInfo


def build_github(tool_aggregation, releases_response):
    tool_source = tool_aggregation.tool_source
    release_asset_regex = tool_source.release_asset_regex
    assets = releases_response.json()['assets']
    version = releases_response.json()['tag_name']
    asset = next(filter(lambda x: re.search(release_asset_regex, x['name']) is not None, assets))
    return DownloadInfo(asset['browser_download_url'], asset['name'], version)


def build_intellij_platform(tool_aggregation, releases_response):
    tool = tool_aggregation.tool
    tool_source = tool_aggregation.tool_source
    latest_update = releases_response.json()[0]
    file_relative_path = latest_update['file']
    version = latest_update['version']
    url = f'https://plugins.jetbrains.com/files/{file_relative_path}'
    file_name = os.path.basename(file_relative_path)
    return DownloadInfo(url, file_name, version)
