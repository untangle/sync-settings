import sync.registrar

sync.registrar.register_operation("update-hostname",    None, ["hostname -F /etc/hostname"],          1, "restart-networking")
sync.registrar.register_operation("restart-networking", ["ifdown -a -v --exclude=lo"], ["ifup -a -v --exclude=lo", "/usr/bin/systemctl-wait"], 10, None)