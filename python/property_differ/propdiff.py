#! /usr/bin/env python

# Compare semantically java property file keys. Usage: ./propdiff.py propertyfile1 propertyfile2
# Remove lines starting with # as comments. Ignore rows not in format "key : value" or "key = value"
# Checks also for duplicate keys in a property file.

import logging, sys, re
from collections import defaultdict

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
LOG = logging.getLogger('propertydiffer')

p_equals = re.compile('=')
p_colon = re.compile(':')
p_comment = re.compile('^#')

class DataHolder:
    def __init__(self, value=None, attr_name='value'):
        self._attr_name = attr_name
        self.set(value)
    def __call__(self, value):
        return self.set(value)
    def set(self, value):
        setattr(self, self._attr_name, value)
        return value
    def get(self):
        return getattr(self, self._attr_name)

def load(content):
    """ Load and split properties and return as key/value map """
    d = defaultdict(list)
    for line in content:
        if p_comment.search(line):
            continue

        save_data = DataHolder()

        p1 = None
        if save_data(p_equals.search(line)):
            p1 = save_data.value

        p2 = None
        if save_data(p_colon.search(line)):
            p2 = save_data.value.start()

        if p1 and p2:
            if p1 > p2:
               k,v = p_colon.split(line)
               append_and_strip(d, k, v)
            else:
               k,v = p_equals.split(line)
               append_and_strip(d, k, v)
        elif p1:
               k,v = p_equals.split(line)
               append_and_strip(d, k, v)
        elif p2:
               k,v = p_colon.split(line)
               append_and_strip(d, k, v)
        else:
            LOG.debug("No keys found for line:" + str(line))

    return d

def append_and_strip(dict1, k, v):
    dict1[k.strip()].append(v.strip())

def check_duplicates(dict_1):
    """ check if dictionary contains more than 1 values for key and print those keys """
    return [k for (k, vlist) in dict_1.items() if has_duplicates(vlist)]

def has_duplicates(vlist):
    return len(vlist) != 1

def check_duplicates_and_report_filename(filename, dict1):
   dups = check_duplicates(dict1)
   if dups:
       print "%s has following duplicate key%s: %s " % (filename , "s"[len(dups)==1:], ", ".join(dups))

def print_keys(filename, keyset):
    print "%s has following unique key%s: %s" % (filename, "s"[len(keyset)==1:], ", ".join(keyset))

def load_file(inputfile):
    with open(inputfile) as f:
        # TODO Add nicer check for missing files.
        return [line.strip() for line in f.readlines()]

if __name__ == '__main__':
    # TODO Add usage.
    assert(len(sys.argv) == 3)

    inputfile_1 = str(sys.argv[1])
    inputfile_2 = str(sys.argv[2])

    content_1 = load_file(inputfile_1)
    content_2 = load_file(inputfile_2)

    dictionary_1 = load(content_1)
    dictionary_2 = load(content_2)

    check_duplicates_and_report_filename(inputfile_1, dictionary_1)
    check_duplicates_and_report_filename(inputfile_2, dictionary_2)

    keys_1 = set(dictionary_1.keys())
    keys_2 = set(dictionary_2.keys())

    keys_1_minus_keys_2 = keys_1.difference(keys_2)
    keys_2_minus_keys_1 = keys_2.difference(keys_1)

    if keys_1_minus_keys_2:
        print_keys(inputfile_1, keys_1_minus_keys_2)

    if keys_2_minus_keys_1:
        print_keys(inputfile_2, keys_2_minus_keys_1)

    if not keys_1_minus_keys_2 and not keys_2_minus_keys_1:
        print "Property files have identical keys."
