from flask import Flask, render_template, request, redirect,jsonify
from flask_cors import CORS
# from flask_bootstrap import Bootstrap
# from flask_nav import Nav
# from flask_nav.elements import Navbar, View
from redisearch import AutoCompleter, Suggestion, Client, Query, aggregation, reducers, IndexDefinition, TextField, NumericField, TagField

from os import environ
import redis
import json
import string
from datetime import datetime

'''
    REDIS_HOSTNAME optional (default localhost)
    REDIS_PORT optional (default 6379)
    REDIS_PASSWORD optional (default none)
    

    Example:
    $ export REDIS_HOSTNAME=localhost; export REDIS_PORT=14000; 
    export PREFIX_NAME=case; 
    python3 app.py

'''



redis_hostname = environ.get('REDIS_HOSTNAME','localhost')
redis_port = environ.get('REDIS_PORT',6379)
redis_password = environ.get('REDIS_PASSWORD',"")


app = Flask(__name__)
CORS(app)
# bootstrap = Bootstrap()

caseclient = Client(
   'cases',
   host=redis_hostname,
   password=redis_password,
   port=redis_port
   )
fileclient = Client(
   'files',
   host=redis_hostname,
   password=redis_password,
   port=redis_port
   )

@app.route('/<case_id>')
def get_case(case_id):
   query = Query("@caseid:{" + case_id + "}").paging(0, 1)
   results = caseclient.search(query)
   total = results.total
   if total > 0:
      case = results.docs[0]
   else:
      case = "None found"
      return None
   # case = [
   #    (lambda x: [x.caseid, x.investigator, x.value, x.primary_acctno, x.ssn, x.report_body, (datetime.fromtimestamp(float(x.date_reported)).strftime('%c'))]) (x) for x in results.docs
   #    ]
   if request.args.get("render",None):
      return render_template('case.html', case = case.__dict__)
   else:
      return case.__dict__

@app.route('/search')
def index():
   investigator_id = request.args.get("inv_id",default=None)
   status = request.args.get("status",default=None)
   priority = request.args.get("priority",default=None)
   search_str = request.args.get("search_str","*")
   pri_acctno = request.args.get("pri_acctno",None)
   tag_str = request.args.get("tag_str",None)
   ssn = request.args.get("ssn",None)
   count = request.args.get("count",default=25)
   val_min = request.args.get("val_min",None)
   val_max = request.args.get("val_max",None)
   summarize = request.args.get("summarize",None)

   # print("--- investigator id: {} {}".format(investigator_id, type(investigator_id)))


   query_str = search_str + " "
   if investigator_id is not None:
      query_str = query_str.replace("*","") + "@investigator:{" + investigator_id + "} "
   if status is not None:
      query_str = query_str.replace("*","") + "@status:{" + status + "} "
   if tag_str is not None:
      query_str = query_str.replace("*","") + "@related_tags:{" + tag_str + "} "
   if pri_acctno is not None:
      query_str = query_str.replace("*","") + "@primary_acctno:{" + pri_acctno + "} "
   if ssn is not None:
      query_str = query_str.replace("*","") + "@ssn:{" + ssn + "} "      
   if priority is not None:
      query_str = query_str.replace("*","") + "@priority:{" + priority + "} "   
   if not (val_min is None and val_max is None):
      query_str = query_str.replace("*","") + "@value:[" + val_min + " " + val_max + "]"

   if summarize:
      query = Query(query_str).sort_by("date_reported",asc=False).limit_fields("report_body").paging(0, count).highlight("report_body").summarize("report_body")
   else:
      query = Query(query_str).sort_by("date_reported",asc=False).paging(0, count).highlight(fields="report_body")

   results = caseclient.search(query)
   total = results.total
   cases = [
      (lambda x: [x.caseid, x.investigator, x.value, x.primary_acctno, x.ssn, x.report_body, (datetime.fromtimestamp(float(x.date_reported)).strftime('%c'))]) (x) for x in results.docs
      ]
   
   cases_dict = [ (lambda x: x.__dict__)(x) for x in results.docs ]

   if request.args.get("render",None):
      return render_template('latest.html', cases = cases, total = total)
   else:
      return jsonify(cases_dict)

@app.route('/filesearch')
def file_search():
   search_str = request.args.get("search_str","*")
   caseid = request.args.get("caseid",None)
   filetype = request.args.get("filetype",None)
   count = request.args.get("count",default=25)

   query_str = search_str + " "
   if caseid is not None:
      query_str = query_str.replace("*","") + "@caseid:{" + caseid + "} "
   if filetype is not None:
      query_str = query_str.replace("*","") + "@filetype:{" + filetype + "} "


   query = Query(query_str).sort_by("date_added",asc=False).paging(0, count).highlight(fields="body").summarize(fields="body")

   results = fileclient.search(query)
   total = results.total
   cases = [
      (lambda x: [x.caseid, x.id, x.filetype, x.s3_url, (datetime.fromtimestamp(float(x.date_added)).strftime('%c')), x.body]) (x) for x in results.docs
      ]

   files_dict = [ (lambda x: x.__dict__)(x) for x in results.docs ]

   if request.args.get("render",None):
      return render_template('fileresults.html', cases = cases, total = total)
   else:
      return jsonify(files_dict)

if __name__ == '__main__':


   # nav = Nav()
   # topbar = Navbar('',
   #    View('Home', 'index'),
   #    # View('Case Search', 'search_cases'),
   #    # View('File Search', 'search_files'),
   #    # View('Aggregations', 'show_agg'),
   # )
   # nav.register_element('top', topbar)



   # bootstrap.init_app(app)
   # nav.init_app(app)
   app.debug = True
   app.run(port=5000, host="0.0.0.0")
