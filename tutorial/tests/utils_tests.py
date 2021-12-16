from tutorial.utils import *

def test_split_url():
    test_url = "https://www.quakeworld.nu/forum/14/team-fortress"
    url_head, url_tail = split_url(test_url)

    assert url_head == "https://www.quakeworld.nu/forum/14"
    assert url_tail == "team-fortress"