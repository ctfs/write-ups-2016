from flask import *
import utils
app = Flask(__name__)
@app.route('/', methods = ['GET','POST'])
def default():
    if request.method == 'POST':
        if 'get-luggage' in request.form:
            returned = utils.get_from_table(request.form["get-luggage"])
        elif 'store-luggage' in request.form and 'team-name' in request.form:
            if not len(request.form["store-luggage"]) > 20 and not any(x in request.form["store-luggage"] for x in ["tjctf", "ftcjt", "{", "}"]):
                returned = utils.add_to_table(request.form["store-luggage"], request.form["team-name"])
            else:
                returned = "Invalid Input."
        else:
            returned = "Invalid POST Data."
        return render_template('index.html', data=returned)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
