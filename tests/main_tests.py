from mc_server_downloader import *
from nose.tools import ok_


def test_json_format():
    test_json = get_json_file_from_url(minecraft_url)
    ok_(type(test_json), dict)
