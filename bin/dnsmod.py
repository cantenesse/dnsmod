#!/usr/bin/env python

import dns.query
import dns.tsigkeyring
import dns.update
import sys
import yaml
from optparse import OptionParser

def parse_options():
    parser = OptionParser()
    parser.add_option("-c", "--config",
                      action="store", type="string",
                      help="source file or directory to sync")
    parser.add_option("-i", "--ipaddress",
                      action="store", type="string",
                      help="source file or directory to sync")
    parser.add_option("-r", action="store_true", dest="remove",
                      help="remove following name and ip entry")
    parser.add_option("-a", action="store_true", dest="add",
                      help="add following name and ip entry")
    parser.add_option("-n", "--name",
                      action="store", type="string",
                      help="source file or directory to sync")

    (options, args) = parser.parse_args()

    return (options, args)

def load_config(config):
    f = open(config, 'r')
    return yaml.load(f)

if __name__ == '__main__':
    options, args = parse_options()

    print options.remove, options.add
    if not (options.remove or options.add):
        print "figure out how to print usage"
        sys.exit(1)
 
    config = load_config(options.config)

    tsig =  config['domain']['tsig']
    domain_name = config['domain']['name']
    name_server = config['domain']['server']
    ttl = config['domain']['ttl']

    keyring = dns.tsigkeyring.from_text({
        "%s." % (domain_name) : tsig
    })
    
    update = dns.update.Update(domain_name, keyring=keyring)

    if options.remove:
        update.delete(options.name, 'A', options.ipaddress)
    elif options.add:
        update.add(options.name, ttl, 'A', options.ipaddress)
    try:
        response = dns.query.tcp(update, name_server)
    except Exception, e:
        print e
