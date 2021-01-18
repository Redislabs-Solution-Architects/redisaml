from redis import Redis
from redis.exceptions import ResponseError,ConnectionError
from os import environ,urandom,fork
from uuid import uuid1,uuid4
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
    COUNT (default 100000)
    

    Example:
    $ export REDIS_HOSTNAME=localhost; export REDIS_PORT=14000; 
    export INDEX_NAME=contracts; export COUNT=10000; 
    python3 contracts.py

'''

'''
returns a coherent record for a financial crimes case record

'''
def create_record(fake, id):
    record = {}


    statuses = ["new","investigating","resolved","on-hold","archived"]
    priorities = ["low","med","high"]
    date_range = [1389576338,1601861138] # Jan 13 2014 to Oct 5 2020

    record["id"] = 10320000000 + id
    record["status"] = statuses[random.randrange(0,len(statuses)-1)]
    record["investigator"] = random.randrange(501001,501501)
    record["value"] = int(abs(random.gauss(10000,300000)))

    record["files"] = str(uuid1()).replace("-","")
    for _ in itertools.repeat(None,random.randrange(1,8)):
        record["files"] = record["files"] + "," + str(uuid4()).replace("-","")
    record["date_reported"] = random.randrange(date_range[0],date_range[1])
    record["date_last_updated"] = record["date_reported"] + random.randrange(1728000,8640000) # + 20 days or 100 days
    record["report_body"] = fake.text()
    record["primary_acctno"] = fake.ean8(prefixes=("41","82","21","97"))
    record["ssn"] = str(fake.ssn()).replace("-","")
    record["phone"] = fake.phone_number()
    record["ip"] = fake.ipv4()
    # first, middle, last, address, country, ip
    record["account_details"] = json.dumps(
        {"Full Name": fake.name(), 
        "Street": fake.street_address(), 
        "Country": "US", "State": "NB", 
        "PostCode": fake.postcode()}
    )
    record["priority"] = priorities[random.randrange(0,len(priorities)-1)]
    record["related_tags"] = record["primary_acctno"]
    for _ in itertools.repeat(None,random.randrange(4,19)):
        record["related_tags"] = record["related_tags"] + "," + fake.ean8(prefixes=("41","82","21","97"))
    
    # print(record)
    return record




if __name__ == '__main__':

    batch = 5
    count = environ.get('COUNT',100000)
    redis_hostname = environ.get('REDIS_HOSTNAME','localhost')
    redis_port = environ.get('REDIS_PORT',6379)
    namespace = environ.get('NAMESPACE', "case") + ":"

    r = Redis(host=redis_hostname, port=redis_port, decode_responses=True)
    r.info()
    fake = Faker()

    counter = 0
    while counter <= int(count):        
        with r.pipeline(transaction=False) as pipe:
            pipe.multi()
            for _ in itertools.repeat(None, batch):
                record = create_record(fake,counter)
                if counter == 0: 
                    print("Sample record: {}".format(json.dumps(record, indent=4)))
                pipe.hset("{}{}".format(namespace,record["id"]),mapping=record)
                counter = counter + 1
            pipe.execute()
        if counter % 1000 == 0 :
            print(".",end="",flush=True)
    print("\nFinished writing {} records.".format(counter))

    # get some related tags from existing records
    seeds = r.scan(match="{}*".format(namespace),count=3)[1]
    taglist = list()
    for result in seeds:
        tags = r.hget(result,"related_tags").split(",")
        for tag in tags[0:len(tags)-4]:
            taglist.append(tag)    
    random.shuffle(taglist) # shuffle so it is less deterministic

    # create the list of tags to be added to cases
    to_be_added_tags = ""
    for i in range(1,batch):
        to_be_added_tags  = to_be_added_tags  + "," + taglist[i]
        # print("{},".format(taglist[i]),flush=False,sep='',end='')
    print("--- Tags to be added: {}".format(to_be_added_tags))

    for _ in itertools.repeat(None, random.randrange(batch,batch*3)): 
        # # find one target case
        # sample = random.sample(r.scan(match="{}*".format(namespace),count=15)[1],1)
        # print("******\n*** Main target case: {} ***\n******".format(sample))

        targets = list()
        for _ in itertools.repeat(None, random.randrange(1,batch)):
            targets.append(namespace + str(create_record(fake, random.randrange(1,int(count)))["id"]))
        print("Targets: {}".format(targets))


        for target in targets:
            related_tags = r.hget(target,"related_tags")
            related_tags = related_tags + to_be_added_tags
            #put record back
            r.hset(target,"related_tags",related_tags)
    print("\n")
            
        
        
