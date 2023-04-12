#-----------------------------------------------------------------------
# Author: Lois I Omotara
# reg.py
#-----------------------------------------------------------------------
import sys
import flask
import databasesearch as ds
import classsearch as cs
import lineparser as lp

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')
#-----------------------------------------------------------------------

@app.route('/', methods =['GET'])
def init():
    html_code = flask.render_template('regresults.html')
    response = flask.make_response(html_code)
    return response

@app.route('/searchresults',methods = ['GET'])
def search_results():
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''
    dept = dept.strip()
    num = flask.request.args.get('num')
    if num is None:
        num = ''
    num = num.strip()
    area = flask.request.args.get('area')
    if area is None:
        area = ''
    area = area.strip()
    title = flask.request.args.get('title')
    if title is None:
        title = ''
    title = title.strip()
    try:
        search = ds.DatabaseSearch()
        rawsearch = search.fullsearch(idept=dept,icoursenum=num,
        iarea=area, ititle=title)
    except Exception as ex:
        print(ex,file=sys.stderr)
        html_code=flask.render_template('errorpage_portion.html',
            type_error = '''A server error occured.
            Please contact the system adminstrator''')
        return flask.make_response(html_code)
    course_results_ = []
    for row in rawsearch:
        course_results_.append(lp.LineParser(row))
    html_code = flask.render_template('resultstable.html',
        course_results = course_results_)
    response = flask.make_response(html_code)
    return response


@app.route('/regdetails',methods=['GET'])
def regdetails():
    classid = flask.request.args.get('results')
    if classid == '':
        html_code = flask.render_template('errorpage.html',
            type_error = 'Missing Classid')
        return flask.make_response(html_code)
    try:
        strclassid = classid
        classid = int(classid)
    except ValueError:
        html_code = flask.render_template('errorpage.html',
            type_error = 'Non-Integer Classid')
        return flask.make_response(html_code)
    try:
        search = cs.ClassSearch(classid)
        general= search.get_general()
        if bool(general) is False:
            html_code = flask.render_template('errorpage.html',
            type_error = 'No Class with Classid '+strclassid+' Exists')
            return flask.make_response(html_code)
        general = general[0]
        deptandnum =[]
        for row in search.get_deptandnum():
            deptandnum.append(row[0]+' '+row[1])
        profs = []
        for row in search.get_prof():
            profs.append(row[0])
    except Exception as ex:
        print(ex,file=sys.stderr)
        html_code=flask.render_template('errorpage.html',
            type_error = '''A server error occured.
            Please contact the system adminstrator''')
        return flask.make_response(html_code)
    html_code = flask.render_template('regdetails.html',
        class_id=classid,days=general[1],start_time=general[2],
        end_time=general[3],building=general[4],room=general[5],
        course_id=general[0],dept_and_nums=deptandnum,
        area=general[6],title=general[7],description=general[8],
        professors=profs,prereqs=general[9])
    response = flask.make_response(html_code)
    return response
