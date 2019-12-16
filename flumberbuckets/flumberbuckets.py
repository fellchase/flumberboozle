#!/usr/bin/env python

import threading, argparse, subprocess, botocore.session, os, sys
from queue import Queue

parser = argparse.ArgumentParser('./flumberbuckets.py [options] -i [bucket]')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-w', '--wordlist', dest='wordlist', help='location of wordlist from which permutations of keyword will be generated')
group.add_argument("-s", "--single", dest="single", help="check a single bucket only", action='store_const', const=True, default=False)

parser.add_argument('-i', '--input', dest='input', help='specify keyword or bucket name, supply - as argument to take input from stdin')
parser.add_argument('-t', '--threads', dest='threads', help='specify number of threads to be used for enumeration of existent buckets default is 150', default=150)
parser.add_argument('-o', '--output', dest='output', help='location to save output', default='')
parser.add_argument('-d', '--fqdn', dest='domainlist', help='specify list of FQDNs to search for buckets having same name as FQDN', default='')
try:
    par_mdns_path = os.environ['mdns_path']
except:
    par_mdns_path = 'massdns/bin/massdns'
parser.add_argument('-m', dest='mdns_path', help='specify path to massdns binary', default=par_mdns_path)
parser.add_argument('--resolve', dest='resolver_path', help='specify path to resolvers file', default='resolvers.txt')
parser.add_argument('-n', dest='no_banner', help='do not print banner', action='store_const', const=True, default=False)
parser.add_argument('--no-colour', dest='no_colour', help='output is colourless', action='store_const', const=True, default=False)
parser.add_argument('-p', "--print-everything", dest='print_everything', help='print bucket information even if it is not vulnerable', action='store_const', const=True, default=False)

# Testing relevant arguments 
parser.add_argument("-u", "--upload", dest="upload", help="perform file upload test. default=False", action='store_const', const=True, default=False)
parser.add_argument("-r", "--remove", dest="remove", help="remove file from bucket after uploading it. default=False", action='store_const', const=True, default=False)

parser.add_argument("--acl", dest="acl", help="perform ACL test", action='store_const', const=True, default=False)
parser.add_argument("--policy", dest="policy", help="perform policy test", action='store_const', const=True, default=False)
parser.add_argument("--cors", dest="cors", help="perform CORS configuration test", action='store_const', const=True, default=False)
parser.add_argument("--replication", dest="replication", help="perform replication configuration test", action='store_const', const=True, default=False)
parser.add_argument("--website", dest="website", help="perform website configuration test", action='store_const', const=True, default=False)
parser.add_argument("--location", dest="location", help="perform location test", action='store_const', const=True, default=False)
parser.add_argument("--logging", dest="logging", help="perform logging test", action='store_const', const=True, default=False)
parser.add_argument("-e", "--everything", dest="everything", help="view all bucket configuration. default=True", action='store_const', const=True, default=True)
args = parser.parse_args()

if args.acl or args.policy or args.cors or args.replication or args.website or args.location or args.logging or args.upload or args.remove:
    args.everything = False

if not args.no_banner:
    print("  __ _                 _               _                _        _        ".center(117))
    print(" / _| |_   _ _ __ ___ | |__   ___ _ __| |__  _   _  ___| | _____| |_ ___  ".center(117))
    print("| |_| | | | | '_ ` _ \| '_ \ / _ \ '__| '_ \| | | |/ __| |/ / _ \ __/ __| ".center(117))
    print("|  _| | |_| | | | | | | |_) |  __/ |  | |_) | |_| | (__|   <  __/ |_\__ \ ".center(117))
    print("|_| |_|\__,_|_| |_| |_|_.__/ \___|_|  |_.__/ \__,_|\___|_|\_\___|\__|___/ ".center(117))
    print("                                                                          ".center(117))
    print("S3 Bucket Enumeration                                          @fellchase ".center(117))
    print("                                                                          ".center(117))

session = botocore.session.get_session()
c = session.create_client('s3')
thread_lock = threading.Lock()
global_bucket_counter = 0
cols = os.get_terminal_size()[0]


green = "\033[1;32m"; yellow = "\033[1;33m"; red = "\033[1;31m"; gray = "\033[1;30m";X = "\033[0m"
if args.no_colour:
    green = ""; yellow = ""; red = ""; gray = "";X = ""



def enum_bucket(bucket):
    global global_bucket_counter
    def run_func(func, msg, flag, arg):
        if args.everything or flag:
            try:
                response = func(**arg)
                return True, green + '[' + msg + ']' + X
            except:
                return False, gray + ' ' + msg + ' ' + X
        return False, red + ' ' + msg + ' ' + X

    o_list_objects_v2 = run_func(c.list_objects_v2, 'LIST', True, {"Bucket": bucket})
    o_get_bucket_acl = run_func(c.get_bucket_acl, 'ACL', args.acl, {"Bucket": bucket})
    o_get_bucket_policy = run_func(c.get_bucket_policy, 'POLICY', args.policy, {"Bucket": bucket})
    o_get_bucket_cors = run_func(c.get_bucket_cors, 'CORS', args.cors, {"Bucket": bucket})
    o_get_bucket_replication = run_func(c.get_bucket_replication, 'REPLICATION', args.replication, {"Bucket": bucket})
    o_get_bucket_website = run_func(c.get_bucket_website, 'WEBSITE', args.website, {"Bucket": bucket})
    o_get_bucket_location = run_func(c.get_bucket_location, 'LOCATION', args.location, {"Bucket": bucket})
    o_get_bucket_logging = run_func(c.get_bucket_logging, 'LOGGING', args.logging, {"Bucket": bucket})
    o_put_object = run_func(c.put_object, 'UPLOAD', args.upload, {"Bucket": bucket, "Key": 'BugBounty-flumber.txt', "Body": b"This file is created for assessing the security of your S3 Buckets as part of your VRP and not for any malicous purposes so check for a new report submitted if it's not there, it'll be filed soon :) Thanks"})
    o_delete_object = run_func(c.delete_object, 'DELETE', args.remove, {"Bucket": bucket, "Key": 'BugBounty-flumber.txt'})
    
    with thread_lock:
        if args.print_everything or o_list_objects_v2[0] or o_get_bucket_acl[0] or o_get_bucket_policy[0] or o_get_bucket_cors[0] or o_get_bucket_replication[0] or o_get_bucket_website[0] or o_get_bucket_location[0] or o_get_bucket_logging[0] or o_put_object[0] or o_delete_object[0]:
            global_bucket_counter += 1
            print(
            (str(global_bucket_counter) + '.').center(4,' '),
            o_list_objects_v2[1], '|',
            o_get_bucket_acl[1], '|',
            o_get_bucket_policy[1], '|',
            o_get_bucket_cors[1], '|',
            o_get_bucket_replication[1], '|',
            o_get_bucket_website[1], '|',
            o_get_bucket_location[1], '|',
            o_get_bucket_logging[1], '|',
            o_put_object[1], '|',
            o_delete_object[1], ' > ',
            yellow + bucket + X, file=sys.stdout if args.output == '' else open(args.output,'a'))


def threader():
    while True:
        task = q.get()
        enum_bucket(task)
        q.task_done()


def create_potential_bucket_list(location_of_potential_bucket_file, wordlist):
    # Bucket names can contain letters, numbers, periods, and hyphens
    # "abcdefghijklmnopqrstuvwxyz0123456789.-"
    print(' '*cols,end='\r') # Cleaning up the terminal line
    print(green + '[+]' + X, "Generating wordlist", end='\r')
    abshere = os.path.join(os.getcwd(), __file__)
    generated_list = [args.input + '.s3.amazonaws.com']

    for word in open(os.path.join(os.path.dirname(abshere), wordlist)):
        word = word.strip('\n')
        generated_list.append("{0}{1}.s3.amazonaws.com".format(args.input, word))
        generated_list.append("{1}{0}.s3.amazonaws.com".format(args.input, word))
        generated_list.append("{0}.{1}.s3.amazonaws.com".format(args.input, word))
        generated_list.append("{1}.{0}.s3.amazonaws.com".format(args.input, word))
        generated_list.append("{0}-{1}.s3.amazonaws.com".format(args.input, word))
        generated_list.append("{1}-{0}.s3.amazonaws.com".format(args.input, word))
    if args.domainlist:
        [generated_list.append(fqdn.strip('\n') + '.s3.amazonaws.com') for fqdn in open(args.domainlist)]
    # Add OSINT on Google and github
    # Printing generated_list to a file
    with open(location_of_potential_bucket_file,'w') as fp:
        [print(item, file=fp) for item in generated_list]
    return location_of_potential_bucket_file


def find_live_buckets():
    if os.path.isfile(args.mdns_path) == False:
        quit("massdns binary does not exist")
    elif os.path.isfile(args.resolver_path) == False:
        quit("resolvers.txt does not exist")
    elif os.path.isfile(args.wordlist) == False:
        quit("wordlist does not exist")

    potential_buckets_file = create_potential_bucket_list('/tmp/flumberbuckets_massdns.txt', args.wordlist)
    mdns_resolve = "{} -r {} --error-log /dev/stderr -q -o S - | tr '[:upper:]' '[:lower:]' | sort -u".format(args.mdns_path, args.resolver_path)
    print(' '*cols,end='\r') # Cleaning up the terminal line
    print(green + '[+]' + X, "Sorting buckets", end='\r')
    output = subprocess.run("< {} {} | grep -v 's3-1-w.amazonaws.com' | grep -v directional | cut -d ' ' -f1 | sed 's/.s3.amazonaws.com.//'".format(potential_buckets_file, mdns_resolve), shell=True, capture_output=True)
    os.remove(potential_buckets_file)
    if len(output.stdout.decode().strip('\n')) == 0:
        print(red + '[-]' + X, "No bucket was found")
        quit()
    return output.stdout.decode().strip('\n').split('\n')
    

try:
    q = Queue()

    if args.single and args.input == '-':
        [q.put(item.strip('\n')) for item in open('/dev/stdin') if item]
    elif args.single:
        with open('/dev/stderr', 'w') as fp:
            print(green + '[+]' + X, "Testing", args.input, "bucket, meanwhile you do Google & GitHub dorking for buckets", file=fp)
        enum_bucket(args.input)
        quit()
    elif args.wordlist:
        [q.put(x) for x in find_live_buckets()]

    with open('/dev/stderr', 'w') as fp:
        print(green + '[+]' + X, "Testing", len(q.queue), "buckets, meanwhile you do Google & GitHub dorking for buckets", file=fp)


    for x in range(int(args.threads)):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    q.join()
except KeyboardInterrupt:
    print(' '*cols,end='\r') # Cleaning up the terminal line
    print(yellow + '[!]' + X, "Terminating")
