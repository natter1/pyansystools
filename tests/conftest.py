"""
@author: Nathanael Jöhrmann
"""
import pytest
# import pyansys
from ansys.mapdl.core import launch_mapdl


@pytest.fixture(scope='session')
def ansys(tmp_path_factory):
    path = tmp_path_factory.getbasetemp()
    mapdl = launch_mapdl(override=True, interactive_plotting=True,
                         run_location=path, loglevel='ERROR')
    yield mapdl
    # ansys.open_gui()
    mapdl.exit()


@pytest.fixture(scope='class')
def mapdl(ansys):
    yield ansys
    ansys.clear()