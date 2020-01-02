import pytest
from subprocess import call
import os
import yaml


"""
test metafunc

this test will test metafunc.

this test will also show how to run tests where
failure is expected (i.e., checking that we handle
invalid parameters).
"""


class TestCLI:
    """
    simple metafunc test class

    This uses the subprocess PIPE var
    to capture system input and output,
    since we are running metafunc from the
    command line directly using subprocess.
    """

    @classmethod
    def setup_class(self):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """

    def testSetup(self):
        """
        test workflow
        """
        command = ["metafunc", "setup", "-n", "test"]
        pwd = os.path.abspath(os.path.dirname(__file__))
        rc = call(command, cwd=pwd)
        assert rc == 0

    @pytest.mark.parametrize(
        "test_input_config,expected",
        [("test/config.yaml", 0), ("config_wrong.yaml", 1)],
    )
    def test_run(self, test_input_config, expected):
        """
        test workflow
        """
        command_prefix = ["metafunc", "run"]
        pwd = os.path.abspath(os.path.dirname(__file__))

        command = command_prefix + [test_input_config]
        rc = call(command, cwd=pwd)
        assert rc == expected

        # clean up run dat
        # config files here specify a resultdir where the snakemake run results
        # will be written to. Here we find it for each indifivual run and delete
        # the directory after successful runs.
        config_data = yaml.safe_load(open(os.path.join(pwd, test_input_config)))
        print(config_data)
        resultdir = config_data["resultdir"]
        rc = call(["rm", "-rf", resultdir], cwd=pwd)
        assert rc == 0

    @classmethod
    def teardown_class(self):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        pwd = os.path.abspath(os.path.dirname(__file__))
        rc = call(["rm", "-rf", "test"], cwd=pwd)
        assert rc == 0
