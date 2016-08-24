from flask import Flask, render_template, request, url_for
import tweet_timer
import datetime

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/predict/', methods=['POST'])
def predict():
    start=datetime.datetime.now()
    name=request.form['username']
    result=tweet_timer.processing(name)
    print datetime.datetime.now()-start
    return render_template('form_action.html', name=name, result=result)

# Run the app :)
if __name__ == '__main__':
  app.run()
