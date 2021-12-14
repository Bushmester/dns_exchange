import pytest

from tests import helpers
from dns_exchange.handlers import mining


@pytest.mark.usefixtures("clean_db")
def test_mine():
    user_info = helpers.get_user(auth_token=True)
    auth_token = user_info['auth_token']

    number = 5

    response_from_mine = mining.mine(auth_token=auth_token, number=number)

    result = response_from_mine.content[0]['title']

    assert result
