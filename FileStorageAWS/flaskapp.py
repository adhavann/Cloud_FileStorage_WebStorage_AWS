#Adhavann Ramalingam
#Cloud Computing FileStorage web applicationusing EC2 and S3 in Amazon Web Services

import os
import boto3
from flask import render_template,request
from flask import Flask
import MySQLdb
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


#Function for root page
@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='GET':
        return render_template('/Auth.html')
    
#Function for validating user name and password
@app.route('/ValidateUser',methods=['POST'])
def authenticate():
    if request.method=='POST':
        username=request.form['username']
        auth_files='names.txt'
        #os.chdir('XXXXXX')
        #Opening the file to read the username and password
        f = open(auth_files,'r')
        for line in f.read().split('\n'):
            print "line"+line
            print "username"+username
            if (line==username):
                return render_template('/SelectOperation.html')
            else:
                status='false'
        status_message='Inavlid username'
        if status=='false':
            return """
            <!doctype html>
            <title>Status</title>
            <h1 style="color: #ff0000">%s</h1>
            """ % status_message

#Function to store the file into the bucket
@app.route('/List',methods=['GET'])
def List():
    s3=boto3.resource('s3')
    my_bucket=s3.Bucket('cloud-assign')
    listfileshtml=''
    for name in my_bucket.objects.all():
        listfileshtml = listfileshtml+"<tr>"
        listfileshtml=listfileshtml+"<td>"+name.key+"</td>"
        listfileshtml=listfileshtml+"</tr>"

    listfileshtml = "<table>"+listfileshtml+"</table>"
    return """
    <!doctype html>
    <title>Files List</title>
    <body style="background-color: #00ffff"><h5>List of Files:</h5>
    %s</body>
    """ % listfileshtml

#Function to Download the content of the file 
@app.route('/Download',methods=['GET','POST'])
def Download():
    if(request.method=='GET'):
        return """
            <!doctype html>
            <title>Input File Name</title>
            <body style="background-color: #00ffff">
            <form name="FormFileDownload" action="\Download" class="col-6" method="POST" enctype="multipart/form-data">
            <input href="/Download"  class="col-6 btn btn-lg btn-success" type="text" name="DownloadFile">
            </form>
            </body>
            """
    if(request.method=='POST'):
        s3=boto3.resource('s3')
        client = boto3.client('s3')
        # transfer = S3Transfer(client)
        # my_bucket=s3.Bucket('cloud-assign')
        filename=request.form['DownloadFile']
        # s3.Object('cloud-assign',filename).download_file('/hello.txt')
        client.download_file('cloud-assign', filename, filename)
        status=open(filename).read()
        # state=my_bucket.download_file(filename,'\Hello.txt')
        # print state
        status='Document Downloaded'
        return """
         <!doctype html>
            <title>Success Status</title>
            <body style="background-color: #00ffff">%s</body>
            """ % status

#Function to Delete the file mentioned 
@app.route('/Delete',methods=['GET','POST'])
def Delete():
    if(request.method=='GET'):
        return """
            <!doctype html>
            <title>Input File Name</title>
            <body style="background-color: #00ffff">
            <form name="FormFileDelete" action="\Delete" class="col-6" method="POST" enctype="multipart/form-data">
            <input href="/Delete"  class="col-6 btn btn-lg btn-success" type="text" name="DeleteFile">
            </form>
            </body>
            """
    if(request.method=='POST'):
        s3=boto3.resource('s3')
        client = boto3.client('s3')
        # transfer = S3Transfer(client)
        my_bucket=s3.Bucket('cloud-assign')
        filename=request.form['DeleteFile']
        for key in my_bucket.objects.all():
            print "file to delete :"+filename
            print key.key
            if(filename==key.key):
                key.delete()
        status='Document Deleted'
        return """
         <!doctype html>
            <title>Success Status</title>
            <body style="background-color: #00ffff">%s</body>
            """ % status
    
#Function to load the webpage for selecting the file to upload
@app.route('/FileUpload',methods=['GET'])
def FileUpload():
    return render_template('FileUpload.html')

#Function to upload the file to the bucket
@app.route('/Upload',methods=['POST'])
def Upload():
    file=request.files['fileupload']
    #return str(file.filename)
    filename=file.filename
    s3_client=boto3.client('s3')
    s3=boto3.resource('s3')
    data=file.read()
    s3.Bucket('cloud-assign').put_object(Key=filename,Body=data)
    status=">Uploaded successfully"
    return """
            <!doctype html>
            <title>Success Status</title>
            <body style="background-color: #00ffff">%s</body>
            """ % status


if __name__ == '__main__':
    app.run(host="127.0.0.1",
                port=int("6234"),
                debug=True)





