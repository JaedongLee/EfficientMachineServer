from unittest import TestCase

from application.tool_service import list_usable_tool_aggregation, get_tool_by_tool_name


class Test(TestCase):

    def test_list_usable_tool_aggregation(self):
        result = list_usable_tool_aggregation()
        for i in result:
            print(i.tool.name)

    def test_get_tool_by_tool_name(self):
        result = get_tool_by_tool_name('Office Tool Plus')
        print(result.__dict__)
