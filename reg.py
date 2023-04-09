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
app = flask.Flask(__name__)
#-----------------------------------------------------------------------
def cookiehandle():
    prev_dept = flask.request.cookies.get('deptcookie')
    if prev_dept.find('None')>=0:
        prev_dept = ''
    prev_num = flask.request.cookies.get('numcookie')
    if prev_num.find('None')>=0:
        prev_num = ''
    prev_area = flask.request.cookies.get('areacookie')
    if prev_area.find('None')>=0:
        prev_area = ''
    prev_title = flask.request.cookies.get('titlecookie')
    if prev_title.find('None')>=0:
        prev_title = ''
    return [prev_dept, prev_num,prev_area,prev_title]

@app.route('/', methods =['GET'])
def search_results():
    source = flask.request.url
    if source.find('?')<0:
        dept = flask.request.args.get('dept')
        num = flask.request.args.get('number')
        area = flask.request.args.get('area')
        title = flask.request.args.get('title')
    else:
        request = source.split('?')[1].split('&')
        dept = str(request[0].split('=')[1])
        num = str(request[1].split('=')[1])
        area = str(request[2].split('=')[1])
        title=str(request[3].split('=')[1])
    try:
        search = ds.DatabaseSearch()
        rawsearch = search.fullsearch(idept=dept,icoursenum=num,
        iarea=area, ititle=title)
    except Exception as ex:
        print(ex,file=sys.stderr)
        html_code=flask.render_template('errorpage.html',
            type_error = '''A server error occured.
            Please contact the system adminstrator''')
        return flask.make_response(html_code)
    course_results_ = []
    for row in rawsearch:
        course_results_.append(lp.LineParser(row))
    if dept is None:
        dept = ''
    if num is None:
        num = ''
    if area is None:
        area = ''
    if title is None:
        title = ''
    html_code = flask.render_template('regresults.html',
        course_results = course_results_,
        dept = dept,
        num = num,
        area = area,
        title = title)
    response = flask.make_response(html_code)
    response.set_cookie('deptcookie',dept)
    response.set_cookie('numcookie',num)
    response.set_cookie('areacookie',area)
    response.set_cookie('titlecookie',title)
    return response

@app.route('/regdetails',methods=['GET'])
def regdetails():
    previous = cookiehandle()
    try:
        classid = flask.request.url.split('=')[1]
    except IndexError:
        html_code = flask.render_template('errorpage.html',
            type_error = 'Missing Classid')
        return flask.make_response(html_code)
    try:
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
                type_error = 'Non-Exisiting Classid')
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
        professors=profs,prereqs=general[9],prev_dept=previous[0],
        prev_num=previous[1],prev_area=previous[2],
        prev_title=previous[3])
    response = flask.make_response(html_code)
    return response
