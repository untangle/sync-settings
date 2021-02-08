import os
import stat
import sys
import subprocess
import datetime
import traceback
import re
from sync.network_util import NetworkUtil
from sync import registrar,Manager

# This class is responsible for writing /etc/hosts and /etc/hostname
# based on the settings object passed from sync-settings


class HostsManager(Manager):
    hostname_filename = "/etc/hostname"

    def initialize(self):
        registrar.register_settings_file("settings", self)
        registrar.register_file(self.hostname_filename, "update-hostname", self)

    def sync_settings(self, settings_file, prefix, delete_list):
        self.write_hostname_file(settings_file.settings, prefix)
        return

    def create_settings(self, settings_file, prefix, delete_list, filename):
        print("%s: Initializing settings" % self.__class__.__name__)
        system = {}
        system['hostName'] = "waf"
        system['domainName'] = "example.com"
        settings_file.settings['system'] = system

    def write_hostname_file(self, settings, prefix):
        if 'hostName' not in settings:
            print("ERROR: Missing hostname setting")
            return

        fqdn_hostname = settings['hostName']
        if 'domainName' in settings:
            fqdn_hostname = fqdn_hostname + "." + settings['domainName']
        filename = prefix + self.hostname_filename
        file_dir = os.path.dirname(filename)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file = open(filename, "w+")
        file.write("%s\n" % fqdn_hostname)

        file.flush()
        file.close()

        print("HostsManager: Wrote %s" % filename)
        return

registrar.register_manager(HostsManager())
