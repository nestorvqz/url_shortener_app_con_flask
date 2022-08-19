from flask import Flask, render_template, request,redirect,url_for,flash,abort,session
import json
import os.path
from werkzeug.utils import secure_filename
## Alerting users with message flashing
app = Flask(__name__)
# because we're using message flashing,  
# we also need to say app.secret_key. This allows us to securely send messages back 
# and forth from the user to make sure that those trying to snooping on the connection 
# cannot see this information. So we need to provide some sort of random string for 
# the time being, just because we're in development you can just type some gibberish.
# But when it comes to production, you would want to find a very random key and make 
# it long so that no one could guess the secret key.
#  


app.secret_key =  'sdsdsds'


@app.route('/')
def home():
    ## Page templates in Flask with Jinja
    ## Implementing sessions and cookies
    return render_template('home.html', codes=session.keys())

## Using GET and POST requests in Flask
@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls={}
        ## Parsing a JSON file for conflicting entrie
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has been taken, please choose another name')
            return redirect(url_for('home'))  
        ## Variable rules in URLs
        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('D:/Python/Flask_Essenctial_Training/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']]={'file':full_name}
        ## Saving to a JSON file
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]= True
        ## Passing form variables to other routes in Flask
        return render_template('your_url.html', code=request.form['code'])
    else:
        ## Using redirect and url_for for error handling
        return redirect(url_for('home'))
     
@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                    ## Variable rules in URLs
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url']) 
                else:
                    ## Working with static files
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)
## Displaying custom error pages
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404