#!/usr/local/bin/python3

import argparse
import os
import re
import subprocess

parser = argparse.ArgumentParser(description='Load *.sql.gz tables into the MySQL database')
parser.add_argument('dir_name', help='Directory that holds the *.sql.gz files')
parser.add_argument('--unzipped', help='Flag indicating whether directory holds files that are already unzipped', action='store_true', default=False)
parser.add_argument('--host', help='MySQL host', default='127.0.0.1')
parser.add_argument('--user', '-u', help='User in MySQL', default='root')
parser.add_argument('--port', '-p', help='MySQL port', default='3306')
parser.add_argument('--name', '-n', help='MySQL database name', default='wikipedia')

args = parser.parse_args()

def full_path(f):
    return os.path.join(args.dir_name, f)
    
# first unzip zipped sql files
if not args.unzipped:
    print('Unzipping files')
    for f in os.listdir(args.dir_name):
        m = re.search('.*\.sql\.gz$', f)
        if m:
            subprocess.call(['gunzip', full_path(m.group(0))])

# neeed mysql_args
mysql_args = ['-h', args.host, '-u', args.user, '-P', args.port, args.name]
            
# now go through all the sql files
txt_files = []
for f_name in os.listdir(args.dir_name):
    m = re.search('enwiki-.*-(\S*)\.sql$', f_name)
    if m:
        # get the file name
        sql_file = full_path(m.group(0))
        name = m.group(1)
        txt_file = full_path(name + '.txt')
        txt_files.append(txt_file)
        
        print('Creating', txt_file, 'from', sql_file)
        subprocess.call(['xmlfileutils/sql2txt', '-s', sql_file, '-t', txt_file])

        # get the table initialization commands from the .sql file
        with open(full_path(f_name), 'r') as f:
            commands = []
            started_commands = False
            finished_commands = False
            while(not finished_commands):
                line = f.readline()
                if not started_commands:
                    if re.match('-- Table structure for table `' + name + '`', line):
                        started_commands = True
                        f.readline() # skip next line
                else:
                    if re.match('--', line):
                        finished_commands = True
                    else:
                        commands.append(line)

        # write the commands to a temp file
        tmp_file_name = full_path('tmp.sql')
        with open(tmp_file_name, 'w') as f:
            for c in commands:
                f.write(c)

        # initialize the table in the sql database
        cmd = ' '.join(['mysql'] + mysql_args + ['<', tmp_file_name])
        subprocess.call([cmd], shell=True)

        # delete the tmp file
        subprocess.call(['rm', tmp_file_name])

# write the data to the table
print('Writing the data to', args.name)
subprocess.call(['mysqlimport', '--local'] + mysql_args + txt_files)
