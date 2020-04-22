import copy
import os
import stat
import sys
import subprocess
import datetime
import re
import traceback
import glob
from sync import registrar, Manager
from sync.uri_util import UriUtil

# This class is responsible for updating logrotate configuration files

class LogrotateManager(Manager):

    logrotate_conf_file_name = '/etc/logrotate.conf'
    logrotate_directory_name = '/etc/logrotate.d'

    keyword_rotate = re.compile(r'^(\s*rotate\s+)(\d+)')

    def initialize(self):
        """
        Register the settings file and logrotate files.
        """
        registrar.register_settings_file("system", self)
        
        for file_name in self.get_file_names():
            registrar.register_file(file_name, "logrotate-test", self)

    def sync_settings(self, settings_file, prefix, delete_list):
        """
        Synchronize our file by modifying.
        """
        logRetention = 7
        if 'logRetention' in settings_file.settings:
            logRetention = settings_file.settings['logRetention']
        logRetention = str(logRetention)

        for in_file_name in self.get_file_names():
            out_file_name = prefix + in_file_name
            out_file_dir = os.path.dirname(out_file_name)
            if not os.path.exists(out_file_dir):
                os.makedirs(out_file_dir)

            in_file = open(in_file_name, "r")
            out_file = open(out_file_name, "w+")
        
            for line in in_file:
                match = re.search(self.keyword_rotate, line)
                if match:
                    line = "{rotate}{logRetention}\n".format(rotate=match.group(1), logRetention=logRetention)
                out_file.write(line)

            in_file.close()
            out_file.flush()
            out_file.close()
            print("LogrotateManager: Wrote %s" % out_file_name)

        return

    def get_file_names(self):
        """
        Get the primary logrotate configuration and all others under its directory.
        """
        log_rotate_file_names = glob.glob(self.logrotate_directory_name + "/*")
        log_rotate_file_names.insert(0, self.logrotate_conf_file_name)
        return log_rotate_file_names

registrar.register_manager(LogrotateManager())
