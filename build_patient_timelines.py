import sys
import csv
import os
from fieldReader import FieldReader
from collections import defaultdict
import shelve

working_dir = sys.argv[1]
patient_records = defaultdict(list)
print 'testing readability of all files'
for datafile in file(working_dir+'/settings/FILES_TO_READ.txt'):
    print datafile.strip()
    reader = FieldReader('data/'+datafile.strip(), fields=working_dir+'/settings/FIELDS.txt')
print 'done'

for datafile in file(working_dir+'/settings/FILES_TO_READ.txt'):
    if '#' in datafile:
      continue
    reader = FieldReader('data/'+datafile.strip(), fields=working_dir+'/settings/FIELDS.txt')
    for i,l in enumerate(reader):
        if not 'mrn' in l:
          print  'odd record', l,
        else:
          patient_records[l['mrn']].append(l)
        if (i+1)%10000 == 0:
            print i
            sys.stdout.flush()
        print l
    print 'done'
    sys.stdout.flush()

print 'writing shelf'
sys.stdout.flush()
s = shelve.open(working_dir+'/patients/visitShelf', 'n')
for i, (k,val) in enumerate(patient_records.iteritems()):
    if i % 100 == 0:
        print 'patient', i,'/',len(patient_records)
        sys.stdout.flush()
    s[str(k[0])] = val
s.close()
