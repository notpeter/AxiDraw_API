import sys

from pyfakefs.fake_filesystem import PatchMode
from pyfakefs.fake_filesystem_unittest import TestCase

from pyaxidraw import hershey_conf

from axicli import hta_cli

# python -m unittest discover in top-level package dir

class HtaCliTestCase(TestCase):

    def setUp(self):
        self.setUpPyfakefs(patch_open_code=PatchMode.AUTO)
        self.fs.add_real_file('./test/assets/HTA_trivial.svg', target_path='HTA_trivial.svg')

        self.argv_prefix = ['htacli', 'HTA_trivial.svg']

    def test_noncli_conf_options(self):
        """The HersheyAdv class must have been instantiated with the `params`
        parameter, which has all the same attributes as the default config,
        but with some values overridden by the custom config. In particular,
        values that are not settable via command-line must be properly forwarded."""
        sys.argv = self.argv_prefix
        self._setup_confpy("""
script_quiet = 'testvalue'""")
        effect_obj = hta_cli.hta_CLI(dev = True)

        # defined by custom config
        self.assertEqual(effect_obj.params.script_quiet, 'testvalue')
        # defined by default config
        self.assertEqual(effect_obj.params.script_enable, hershey_conf.script_enable)

    def test_cli_options(self):
        """ options created by argparse """
        sys.argv = self.argv_prefix + ['--preserve_text', '--rand_seed', '4']
        effect_obj = hta_cli.hta_CLI(dev = True)

        self.assertTrue(effect_obj.options.preserve_text)
        self.assertEqual(effect_obj.options.rand_seed, 4)

    def _setup_confpy(self, confpy_contents, confpy_name = "custom_conf.py"):
        self.fs.create_file(confpy_name, contents = confpy_contents)
        sys.argv.extend(['--config', confpy_name])
        return confpy_name
