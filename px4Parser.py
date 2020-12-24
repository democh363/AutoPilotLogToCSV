#Usage:  python px4Parser.py --types IMU3 --i your_log_name.log --o my_2.csv

from __future__ import print_function
import csv
import sys
import time
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser(description=__doc__)
parser.add_argument("--types", default='GPS,IMU2,RCOU,BAT', help="types of messages (comma separated with wildcard)")
parser.add_argument("--i", default='vtol.log', help="types of messages (comma separated with wildcard)")
parser.add_argument("--o", default='mylog'+str((datetime.now()).strftime("|%d_%m_%y|%H:%M:%S"))+'.csv', help="types of messages (comma separated with wildcard)")



csv.register_dialect('myDialect',delimiter=',',quoting=csv.QUOTE_NONE)

args = parser.parse_args()
types=args.types
types=types.split(",")
pcd_data = args.i
out_Data = args.o
print(types)
print(pcd_data)
print(out_Data)

def cmp(a, b):
    return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]

with open(pcd_data,"r") as f:
    reader = csv.reader(f,delimiter = ",")
    data = list(reader)
    row_count = len(data)

f.close
header = []
header_sects=[]
total_length = 0
data_fields=[]
header.append("Timestamp")
for messages in types:
    para_length = 0
    print("Message is:",messages)
    print("Types === ",types)
    data_fields.append([])
    
    for rows in data:
        if cmp(rows[3],messages):
            for x in rows[6:]:
                header.append(x)
                para_length=para_length+1
                total_length = total_length +1 
            header_sects.append(para_length)
            break
print(header)

with open(out_Data, 'w') as csvFile:
    write = csv.writer(csvFile,dialect='myDialect')
    write.writerow(header)
    initialisation=0
    for messages in types:
        for rows in data:
            if rows[0] == messages:
                i = types.index(messages)
                data_fields[i].append(rows[1:])
    max_length = 0
    for logs in data_fields:
        length = len(logs)
        if length > max_length:
            max_length = length
            iterator = logs
    temp=[]
    temp = data_fields
    combined_data = []
    combined_dl = []
    i=0
    for index in iterator:
        final_line=combined_dl
        timestamp = float(index[0])
        combined_dl=[]
        combined_dl.append(timestamp)      
        for logs in temp:
            if iterator != logs and len(logs) != 1:                                                   # avoid comparison with self
                distance_1 = timestamp - float(logs[0][0])                                            #comapare first timestamp
                    
                distance_2 = timestamp - float(logs[1][0])                                            # compare second timestamp
            
                if abs(distance_2) <= abs(distance_1):
                   del(logs[0])                                                                       # delete first dataline if next timestamp is closer                           
                   i=i+1
                   current_timegps = float(logs[0][0])
                   next_time = float(logs[0][0])
                   
                ip_data = logs[0]
                for x in ip_data[1:]:
                    combined_dl.append(x)
            else:
                for x in index[1:]:
                    combined_dl.append(x)
        write.writerow(combined_dl)
        
        
csvFile.close
