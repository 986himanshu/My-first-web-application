from flask import Flask, render_template,request,session
from vsearch import search4letters
from DBcm import SQLDatabase
from checker import check_logged_in

app = Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello world from Flask!'

@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You pare now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


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

@app.route('/viewlog')
@check_logged_in
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

app.secret_key = 'YouWillNeverGuessMySecretKey' #Seed Flask’s cookie generation technology with a “secret key,” which is used by Flask to encrypt your cookie, protecting it from any prying eyes
app.run(debug = True, host= "0.0.0.0", port = 5000)
# In the context of servers, 0.0.0.0 means "all IPv4 addresses on the local machine".
# If a host has two IP addresses, 192.168.1.1 and 10.1.2.1, and a server running on the host listens on 0.0.0.0,
# it will be reachable at both of those IPs.

