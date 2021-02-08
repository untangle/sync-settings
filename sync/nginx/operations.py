import sync.registrar

sync.registrar.register_operation("update-hostname",    None, ["hostname -F /etc/hostname"],          1, "restart-networking")
sync.registrar.register_operation("restart-networking", None, ["echo 'restart-networking'"], 10, None)