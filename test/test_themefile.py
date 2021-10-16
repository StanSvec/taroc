import pytest

from taroc import themefile, theme
from test import util

THEME_FILE = 'test.theme'


@pytest.fixture(autouse=True)
def remove_config_if_created():
    yield
    util.remove_test_file(THEME_FILE)


def test_variables_set_from_the_file():
    config = """\
        [general]
        warning = orange

        [hosts_panel]
        title = pink
    """
    util.create_test_file(THEME_FILE, config)
    themefile.load_theme(THEME_FILE)

    assert 'orange' == theme.warning
    assert 'pink' == theme.hosts_panel_title
