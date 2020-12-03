import os
from sync import registrar,Manager

class FreeRadiusManager(Manager):
    config_dir = "/etc/freeradius/3.0/sites-available"
    config_file = config_dir + "/default"
    def initialize(self):
        registrar.register_settings_file("network", self)
        registrar.register_file(self.config_file, "restart-networking", self)

    def sync_settings(self, settings_file, prefix, delete_list):
       self.update_freeradius_server_config(prefix + self.config_file)

    def update_freeradius_server_config(self, configfile):
        os.system("sed 's/#\tradutmp/\tradutmp/g' " + configfile + ">" + configfile + ".bak")
        os.system("cp " + configfile + ".bak " + configfile)

        print("FreeRadiusManager: Wrote %s" % configfile)        

registrar.register_manager(FreeRadiusManager())