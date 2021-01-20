from redis import Redis
from redis.exceptions import ResponseError,ConnectionError
from os import environ,path,listdir
from uuid import uuid4
import random
from time import sleep
from logging import debug, info
from faker import Faker
import json
import itertools

'''
    REDIS_HOSTNAME optional (default localhost)
    REDIS_PORT optional (default 6379)
    PREFIX_NAME optional (default cases)
    COUNT optional (default 10000)
    CSV_DIR optional - should be a relative path without trailing '/'
    

    Example:
    $ export REDIS_HOSTNAME=localhost; export REDIS_PORT=14000; 
    export PREFIX_NAME=files; export COUNT=10000; 
    python3 generate_text_files.py

'''

'''
returns a coherent file attachment record for a financial crimes case record

'''
def create_text_file_record(fake, id, type):
    record = {}

    file_types = ["pdf","txt","doc","csv"]
    date_range = [1389576338,1601861138] # Jan 13 2014 to Oct 5 2020

    if type not in file_types:
        print("File type {} not accepted".format(type))
        exit()

    record["guid"] = str(uuid4()).replace("-","")
    record["caseid"] = id
    record["s3_url"] = fake.file_path(depth=3, extension=type)
    if type is not 'csv':
        record["body"] = fake.text(max_nb_chars=random.randrange(120,4000))
    else:
        record["body"] = ""
    record["filetype"] = type
    record["date_added"] = random.randrange(date_range[0],date_range[1])
    
    # print(record)
    return record




if __name__ == '__main__':

    batch = 1
    count = environ.get('COUNT',10000)
    redis_hostname = environ.get('REDIS_HOSTNAME','localhost')
    redis_port = environ.get('REDIS_PORT',6379)
    namespace = environ.get('NAMESPACE', "file") + ":"
    input_namespace = environ.get('INPUT_NAMESPACE',"case") + ":"
    csv_dir = environ.get('CSV_DIR', None)

    r = Redis(host=redis_hostname, port=redis_port, decode_responses=True)

    fake = Faker()

    # Get a few records to associate files with
    seeds = r.scan(match="case:*",count=100)[1]
    if len(seeds) <= 0:
        print("No records founds with pattern {}*".format(input_namespace))
    print("Records to use: {}", seeds)
    caselist = list()
    for result in seeds:
        caselist.append(r.hget(result,"caseid"))
    random.shuffle(caselist)

    # generate the text files

    counter = 0
    while counter <= int(count) and int(count) > 0:        
        record = create_text_file_record(fake,random.choice(caselist),type=random.choice(["pdf","txt","doc"]))
        if counter == 0: 
            print("Sample record: {}".format(json.dumps(record, indent=4)))
        r.hset("{}{}".format(namespace,record["guid"]),mapping=record)
        counter = counter + 1
    if counter % 1000 == 0 :
        print(".",end="",flush=True)

    ## add csv files if CSV_DIR set
    if csv_dir is not None:
        # does dir exist?
        if path.isdir(csv_dir):
            print("Directory '{}' found".format(csv_dir))
            # and csv files in it?
            print("Files in dir: {}".format(listdir(csv_dir)))
            for file in listdir(csv_dir):
                if path.splitext(file)[-1].lower() == '.csv':
                    # read the file, store contents in 
                    with open("{}/{}".format(csv_dir,file),"r") as f:
                        file_data = f.read().replace(","," ")
                        # print("{}: {}".format(file,file_data))
                        record = create_text_file_record(fake,random.choice(caselist),type="csv")
                        record["body"] = file_data
                        r.hset("{}{}".format(namespace,record["guid"]),mapping=record)
        else:
            print("Directory '{}' NOT found".format(csv_dir))
        exit()
