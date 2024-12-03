from flask import Flask, render_template,request
from vsearch import search4letters

app = Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello world from Flask!'

dbconfig = {'host': 'localhost',
            'dbname': 'vsearchlogdb',
            'user': 'postgres',
            'password': '9811562757',
            'port': '5432'
                }

import psycopg2 as psql
def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results."""

    conn = psql.connect(**dbconfig)
    _SQL = """insert into log 
    (phrase, letters, ip, browser_string, results)
    values
    (%s, %s, %s, %s, %s)"""
    cursor = conn.cursor()
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          # This attribute is returning null entry while request.user_agent string does have browser name
                          res,))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search4' ,methods=['POST'])
def do_search() -> str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results) #Added logs to keep track of request made or served
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)
from markupsafe import escape
'''
Current code gives raw data instead of structured data suitable for interpertations
@app.route('/viewlog') #Created functionality to view log data in webapp only
def view_the_log() -> str:
    with open('vsearch.log') as log:
        contents = log.read()
    return escape(contents)  #escaping contents as request data is not rendered by browser
;
'''

'''
@app.route('/viewlog')
def view_the_log() -> str:
    with open('vsearch.log') as log:
        contents = log.readlines() #Reading all data into a list. If contents were a list of lists instead of a list of strings, it would open up the 
                                   #possibility of processing contents in order using a for loop
    return escape(''.join(contents))
'''

'''
The fact that the data is already in contents (thanks to our use of the 
readlines method) shouldn’t blind us to the fact that we’ve already looped 
through the data once at this point. Invoking readlines may only be a single 
call for us, but the interpreter (while executing readlines) is looping through 
the data in the file.
'''
'''
At first glance, the output produced by this new version of view_the_log
looks very similar to what you had before. But it isn’t: this new output is a list 
of lists, not a list of strings.
'''
'''@app.route('/viewlog')
def view_the_log() -> 'str':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    return str(contents)'''


"""@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                            the_title='View Log',
                            the_row_titles=titles,
                            the_data=contents,)
                            """

"""Implementing view log in relation DBMS called postgreSQL"""
@app.route('/viewlog')
def view_the_log()-> 'html':
    """Display the contents of the log file as a HTML table."""
    conn = psql.connect(**dbconfig)
    _SQL = """select phrase, letters, ip, browser_string, results from log"""
    cursor = conn.cursor()
    cursor.execute(_SQL)
    contents = cursor.fetchall ()
    conn.commit()
    cursor.close()
    conn.close()
    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents,
                           )

@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')
app.run(debug = True)

