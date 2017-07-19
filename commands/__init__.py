
def build_instance_url(instance_conf):
    return instance_conf['protocol'] + '://' + instance_conf['host'] + ':' + str(instance_conf['port'])