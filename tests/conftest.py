import pytest


class MockWorksheet:
    def __init__(self, title='TestWorkSheet1', records=None):
        self.title = title
        self.records = records

    def get_all_records(self):
        return self.records


@pytest.fixture(scope="function")
def empty_worksheet():
    return MockWorksheet()


@pytest.fixture(scope="function")
def worksheet_with_avg():
    return MockWorksheet()