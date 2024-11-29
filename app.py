from flask import Flask, render_template,request
from vsearch import search4letters

app = Flask(__name__)
@app.route('/')
def hello() -> str:
    return 'Hello world from Flask!'

def log_request(req: 'flask_request', res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep='|')

@app.route('/search4' ,methods=['POST'])
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


@app.route('/viewlog')
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
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on the web!')
app.run(debug = True, host= "0.0.0.0", port = 5000)
# In the context of servers, 0.0.0.0 means "all IPv4 addresses on the local machine".
# If a host has two IP addresses, 192.168.1.1 and 10.1.2.1, and a server running on the host listens on 0.0.0.0,
# it will be reachable at both of those IPs.

