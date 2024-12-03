from flask import Flask, render_template,request
from vsearch import search4letters

app = Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello world from Flask!'

import psycopg2 as psql


class SQLDatabase:  # This class will be context manager with start and exit defined. It will implement Setup, Do, Teardown pattern
    def __init__(self, config: dict) -> None:  # For connection to PostgreSQL
        self.configuration = config

    def __enter__(self) -> 'cursor':  # Do part: Creating cursor object that will constitute DB API
        self.conn = psql.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value,
                 exc_trace) -> None:  # Teardown part: It will close connection and release resources safely
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

app.config['dbconfig'] = {'host' : 'localhost',
                'dbname' : 'vsearchlogdb',
                'user' : 'postgres',
                'password' : '9811562757',
                'port' : '5432'
    }

def log_request(req: 'flask_request', res: str) -> None:
    with SQLDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log 
        (phrase, letters, ip, browser_string, results)
        values
        (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              # This attribute is returning null entry while request.user_agent string does have browser name
                              res,))

@app.route('/search4' ,methods=['POST'])
def do_search() -> str:
    """Extract the posted data; perform the search; return results."""
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)
@app.route('/entry')

@app.route('/viewlog')
def view_the_log() -> 'html':
    with SQLDatabase(app.config['dbconfig']) as cursor:
        _SQL = """Select phrase, letters, ip, browser_string, results
        FROM log;"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View Log',
                           the_row_titles=titles,
                           the_data=contents, )

@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')
app.run(debug = True)

