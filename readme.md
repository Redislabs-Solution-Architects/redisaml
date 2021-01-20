# AML Case Management Dataset in Redisearch

This repository creates a coherent AML case management data set in Redisearch and "paints" a situation by labelling a few records with similar entries. 

1. Create your python environment (w/ python3.7+):
   * With pyenv: 
```
$ pyenv versions  # which versions exist?
  3.7.5
  3.7.5/envs/venv375
* 3.7.6 (set by /Users/brad/.pyenv/version)
$ pyenv global 3.7.6  # set this version
# python -m venv .venv-redisaml
```
   * or virtualenv:
``` 
$ virtualenv -p python3.7 .venv-redisaml
$ cd redisaml
$ . .venv-redisaml/bin/activate  #activate it
```
2. Install the requirements:
``` 
pip install -r requirements.txt
```
3. Create the schemas in the target database
4. Generate the case data
5. Generate the file data
6. Query the data

## Create the Schemas

There is a schema for the cases with embedded alert detail.
```
FT.CREATE cases ON HASH PREFIX 1 case: 
SCHEMA 
caseid TAG SORTABLE
status TAG SORTABLE
investigator TAG SORTABLE
value NUMERIC SORTABLE
files TAG SORTABLE
date_reported NUMERIC SORTABLE
date_last_updated NUMERIC SORTABLE
report_body TEXT
primary_acctno TAG SORTABLE
phone TEXT NOSTEM
ip TEXT NOSTEM
account_details TEXT NOINDEX
priority TAG SORTABLE
related_tags TAG SORTABLE
ssn TAG SORTABLE


FT.CREATE cases ON HASH PREFIX 1 case: SCHEMA caseid TAG SORTABLE status TAG SORTABLE investigator TAG SORTABLE value NUMERIC SORTABLE files TAG SORTABLE date_reported NUMERIC SORTABLE date_last_updated NUMERIC SORTABLE report_body TEXT primary_acctno TAG SORTABLE phone TEXT NOSTEM ip TEXT NOSTEM account_details TEXT NOINDEX priority TAG SORTABLE related_tags TAG SORTABLE ssn TAG SORTABLE
```

Here is the files schema:
```
FT.CREATE files ON HASH PREFIX 1 file: SCHEMA
caseid TAG SORTABLE
s3_url TEXT NOINDEX
body TEXT
type TAG SORTABLE
date_added NUMERIC SORTABLE

FT.CREATE files ON HASH PREFIX 1 file: SCHEMA caseid TAG SORTABLE s3_url TEXT NOINDEX body TEXT filetype TAG SORTABLE date_added NUMERIC SORTABLE

```

## Generate the case data


### Example

Options: 
* `COUNT`: number of records to generate
* `REDIS_HOSTNAME`: hostname of redis server
* `REDIS_PORT`: redis port number
* `PAINT_ONLY`: use this if you want to paint some records with similarities
* `PREFIX_NAME`: to set a prefix instead of "`case:`" (do not specify `:`)

1. Generate case records:
```
$ export REDIS_HOSTNAME=localhost; export COUNT=100; python generate_cases.py
Sample record: {
    "id": 10320000000,
    "status": "resolved",
    "investigator": 501342,
    "value": 195689,
    "files": "2d83a34a577711eb89288c8590c28961,341353e0f0a74d688624d783638985f9,12a08f524fd8437a931040491f2a6179,b31f2fd79dc042e19cd616b047fa6f92",
    "date_reported": 1413400514,
    "date_last_updated": 1420499650,
    "report_body": "Idea film interest window where. Finish debate other red foreign boy fly what.\nPass fact one picture structure fly. Special still ten staff life program discuss.",
    "primary_acctno": "82021658",
    "ssn": "763019603",
    "phone": "445.470.7194x283",
    "ip": "184.207.165.185",
    "case_body": "{\"Full Name\": \"Raymond Trujillo\", \"Street\": \"2942 Sarah Route Apt. 975\", \"Country\": \"US\", \"State\": \"NB\", \"PostCode\": \"67047\"}",
    "priority": "low",
    "related_tags": "82021658,41525715,82098698,82527044,41750483,82849870,97004257,21609718,21198687,97558262,21392368,97550044,41410295,97347125,21578915,82367961,21098512,82173470,97919438"
}

Finished writing 105 records.
--- Tags to be added: ,21450112,41938201,97605959,21240256
Targets: ['case:10320000022', 'case:10320000013', 'case:10320000043']
Targets: ['case:10320000033']
Targets: ['case:10320000034', 'case:10320000082', 'case:10320000069']
Targets: ['case:10320000001', 'case:10320000073', 'case:10320000062', 'case:10320000088']
Targets: ['case:10320000053', 'case:10320000075', 'case:10320000032']
Targets: ['case:10320000056', 'case:10320000007', 'case:10320000075', 'case:10320000052']
Targets: ['case:10320000095', 'case:10320000062']
Targets: ['case:10320000070', 'case:10320000078']
Targets: ['case:10320000014', 'case:10320000098', 'case:10320000094']
```

2. Generate files associated with case records:
   
Options: 
* `COUNT`: number of records to generate
* `REDIS_HOSTNAME`: hostname of redis server
* `REDIS_PORT`: redis port number
* `PAINT_ONLY`: use this if you want to paint some records with similarities
* `PREFIX_NAME`: to set a prefix instead of "`file:`" (do not specify `:`)

```
$ export COUNT=3000; python generate_text_files.py
Records to use: {} ['case:10320000050', 'case:10320000087', 'case:10320000034', 'case:10320000071', 'case:10320000023', 'case:10320000036', 'case:10320000028', 'case:10320000064', 'case:10320000090']
Sample record: {
    "guid": "2fb6cf83fd394d65b5a3990f3dab5ed3",
    "caseid": "10320000064",
    "s3_url": "/word/among/score/money.txt",
    "body": "Involve last thought produce toward bar. Purpose contain action.\nAvailable perhaps hear husband. Impact election realize TV where investment. Production piece might part drop.\nDraw goal Mrs gun wear. Several culture finally we challenge near before. Election part leader wind who thing society.\nAnimal positive authority try student. Support difficult its attention tax about reality.\nPainting more television <snip>recognize.\nStyle every professor social Democrat weight. Spend matter apply impact draw per economic everything.\nMother manage whatever standard.\nRealize director day report. Far after team interesting best. Must either free responsibility weight plan.\nCause ahead approach. Send involve edge court.\nDecide ago ground world again generation energy. Performance system trade each step.",
    "filetype": "txt",
    "date_added": 1436571647
}
```


## Example Redisearch Queries

Which cases contain the word 'society' in report_body:
``` 
ft.search cases "world" RETURN 1 report_body SUMMARIZE HIGHLIGHT
```
Which cases have the status 'new':
```
ft.search cases "@status:{new}" RETURN 0 LIMIT 0 15
```
How many cases are there of specific status? 
```
ft.aggregate cases * GROUPBY 1 @status REDUCE COUNT 0
```
What is the total Value of cases under investigation by status?
```
ft.aggregate cases * GROUPBY 1 @status REDUCE sum 1 value as Category_Case_Value
```
Find the terms 'capital' or 'economy' in files associated with *any* case:
```
ft.search files "capital |economy" RETURN 1 body SUMMARIZE HIGHLIGHT LIMIT 0 4
1) (integer) 1687
2) "file:afce89c82df44934b593a6bc44b95e12"
3) 1) "body"
   2) "color. Another amount firm parent real voice. Animal <b>capital</b> step dog. To sign recent activity. Identify allow political...  Player happy green spring magazine sport. On front wonder <b>capital</b>. <b>Economy</b> within policy computer central. Here mean need perhaps our... "
4) "file:7956248de91e479b81e61b95a9582d67"
5) 1) "body"
   2) "choose true explain its management force. Page child kid. <b>Capital</b> brother keep then white also opportunity kitchen. Police... like ago despite budget body. Cell turn long when eight <b>capital</b>. As fact responsibility ago. Language career drug. Score... similar. Outside end arm person. Hundred week nothing five <b>capital</b> very current study. Mouth policy relationship. Evening... "
6) "file:1f608bf7faf6445b9df46e26ac2f6b03"
7) 1) "body"
   2) "Usually current everybody top attack bit trip. Next <b>capital</b> past administration glass six health. Successful staff... "
8) "file:0031baed6be3442f8f510663058ffb6b"
9) 1) "body"
   2) "office left. Officer with home hundred letter. Anything <b>economy</b> material the. Himself strategy leg speech system one camera... choose. Budget clearly two fall place. Quality should <b>economy</b> thought outside. You mind plan. Improve blood write sort... Change tree perhaps worry service. Computer save usually <b>economy</b>. Citizen chance box deep. Develop carry next personal ready... "
``` 

Find the terms 'building in the files associated with a specific case:
```
ft.search files "building @caseid:{10320000064}" RETURN 1 body SUMMARIZE HIGHLIGHT LIMIT 0 4
1) (integer) 166
2) "file:75f089fc65ee495d9e71711dcaae8397"
3) 1) "body"
   2) "cultural. Report apply across. Trip hold <b>building</b> chance truth office. Interest box <b>building</b> Democrat look. Speak help without piece... "
4) "file:603a243c46574cee8692d7c05bb42cd9"
5) 1) "body"
   2) "claim you. New deep professional control above successful <b>building</b>. Want wonder evening itself wind. Fish miss who year. Seek...  Seek especially model. Partner feel should loss. Agent <b>building</b> middle off reveal. Fact try nothing cultural character ok... "
6) "file:25f66202f5c642ef9ab3ee4f95c693de"
7) 1) "body"
   2) "try real. Financial character sea agreement seek produce <b>building</b>. Never view order. Different color father. Leader study she... she stuff away. Scientist four election commercial cause <b>building</b>. Big return from us right try. Range clearly me... "
8) "file:05a46732fe584c55b53a549da7ab52c5"
9) 1) "body"
   2) "decision. Analysis these avoid ago. Bar hear at. Fast more <b>building</b> keep. Manage board then left southern travel. President... full. Sea movie pattern shoulder audience open middle sea. <b>Building</b> land remember better general address end. Successful game... "
```

## Example API Queries

* `http://localhost:5000/search?val_min=1000&val_max=10000&count=2`
* `http://localhost:5000/search?render=1&val_min=1000&val_max=10000&count=2`
* `http://localhost:5000/search?val_min=1000&val_max=10000&count=12&search_str=industry`
* `http://localhost:5000/search?val_min=1000&val_max=10000&count=12&tag_str=41923764`
* 

### Optional
Generate *N* CSV files to be indexed in directory 'files/':
```
$ N=234
$ for i in $(seq 0 1 $N); do csvfaker -r $((1 + $RANDOM % 40)) first_name last_name job ean8 ssn > files/csv$i.csv; done;
$ ls files
csv1.csv  csv2.csv  csv3.csv  csv4.csv ...
```
You can index these files this way:
```
$ export COUNT=0; export CSV_DIR=files; python generate_text_files.py
```
You should probably delete the files now. `rm -r files/*.csv`
