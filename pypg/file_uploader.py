'''
Created on Mar 17, 2017

@author: bperlman1
'''
import sys
import os
import pandas as pd
import string
from builtins import str
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded

from flask import Flask, render_template, request, redirect, url_for, send_from_directory,make_response
#from Werkzeug import secure_filename
uloader_folder = None
# Initialize the Flask application
app = Flask(__name__)

# These are the extension that we are accepting to be uploaded
#app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(['sql','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index_uploader.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
#         filename = secure_filename(file.filename)
        filename = file.filename
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filename=filename))

# Route to show jquery DataTables
@app.route('/dtables', methods=['GET'])
def dtables():
    # Get the name of the uploaded file
    return render_template('dtables.html')

# Route to show jquery DataTables
@app.route('/dtables2', methods=['GET'])
def dtables2():
    # Get the name of the uploaded file
    df_1 = pd.DataFrame({'c1':[1,2,3,4],'c2':['a','b','c','d']})
    df_1.c1 = df_1.c1.astype(int)
    a = list(string.ascii_lowercase)
    df_2 = pd.DataFrame({'c1':range(len(a)),'c2':a})
    df_2.c1 = df_2.c1.astype(int)
    a = list(string.ascii_uppercase)
    df_3 = pd.DataFrame({'c1':range(len(a)),'c2':a})
    df_3.c1 = df_3.c1.astype(int)
    df_3.c1 = df_3.c1.apply(lambda x:x*100)

    df_4 = pd.DataFrame({'c1':['dog','cat','mouse'],'c2':[1,2,3]})
    df_4.c2 = df_4.c2.astype(int)
    
    return render_template('dtables2.html', 
            html_to_display_1=df_1.to_html(classes='table-striped df1'),
            html_to_display_2=df_2.to_html(classes='table-striped df2'),
            html_to_display_3=df_3.to_html(classes='table-striped df3'),
            html_to_display_4=df_4.to_html(classes='table-striped df4')
    )


# Route to show jquery DataTables
@app.route('/view_csv', methods=['GET'])
def view_csv():
    # Get the name of the uploaded file
    csv_path = request.args.get('csv_path')
    html=None
    if ".txt" in csv_path:
        s = open(csv_path,'r').read()
#         html = unicode(s, "utf-8")
        html = str(s, "utf-8")
        return render_template('editor_viewer.html', 
            html_to_display_1=html)
    else:
        width = pd.get_option('display.max_colwidth')
        pd.set_option('display.max_colwidth', -1)
        df = pd.read_csv(csv_path)
        html = df.to_html(classes='table-striped df1')
        pd.set_option('display.max_colwidth', width)
        return render_template('csv_viewer.html', 
            html_to_display_1=html)


@app.route('/editor_view', methods=['GET'])
def editor_view():
    # Get the name of the uploaded file
    text_path = request.args.get('text_path')
    s = open(text_path,'r').read()
#     html = unicode(s, "utf-8")
    html = str(s, "utf-8")
    return render_template('editor_viewer.html', 
        html_to_display_1=html)
    
@app.route('/editor_capture_text', methods=['POST'])
def editor_capture_text():
    # Get the name of the uploaded file
    full_text = request.args.get('full_text')
    print (full_text)

@app.route('/dtables2_return', methods=['GET'])
def dtables2_return():
    rowdata = request.args.get('rowdata')
    print (rowdata)
    return render_template('ok.html')

def create_arg_dict(args=None):
    """
    Create an Dictionary of from an array that should have come from sys.argv
      which looks like: -i myInputFile -o myOutputFile -b myBegDate -e myEndDate
    The command line must have pairs like the above
    """
    curr_args = args
    if curr_args is None:
        curr_args = sys.argv[1:]
    curr_key = ""
    arg_dict = {}
    for i in range(0,len(curr_args)):
        if "-" == curr_args[i][0]:
            curr_key = curr_args[i]
        else:
            arg_dict[curr_key] = curr_args[i]
    return arg_dict

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    global uploader_folder
    ad = create_arg_dict()
    uploader_folder = ad['-f']
    # This is the path to the upload directory
    app.config['UPLOAD_FOLDER'] = uploader_folder #'uploads/'

    app.run(
        host="127.0.0.1",
        port=int("5550"),
#         debug=True
        debug=False
    )
