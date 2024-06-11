import os 

from flask import Flask, Response, render_template, request

import logging

from generate_qr import create_qr
logging.basicConfig(filename='flask_log.log', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

student_marked_list = [] # This is the list to track the students who are marked present
ip_list: list[str] = [] # This is ip list to track the ip address of the students

@app.route('/')
def index():
    user_ip = request.remote_addr
    
    if user_ip != "127.0.0.1":
        return render_template('error.html', error_message="Access Denied", advice_message="You are not allowed to access this page", url="/markPresent")

    hotspot_qr = create_qr() 
    mark_present_qr = create_qr()

    return render_template('index.html')

@app.route('/markPresent', methods=['POST', 'GET'])
def markPresent():
    user_ip = request.remote_addr
    logging.info(f"User IP: {user_ip}")
    if request.method == 'GET':
        return render_template('attendanceForm.html')
    if request.method == 'POST':
        # reading the student data
        logging.info(request.form)
        student_data = request.form.get('student_id')
        # if student data is not provided
        if not student_data:
            error_message = "Student ID not provided"
            advice_message = "Please provide the student ID"
            url = "/markPresent"
            # return error page
            return render_template('error.html', error_message=error_message, advice_message=advice_message, url=url)

        # check if the student is already marked present 
        if student_data in student_marked_list:
            error_message = "Cannot mark the student present"
            advice_message = "Student already marked present"
            url = "/markPresent"
            # return error page
            return render_template('error.html', error_message=error_message, advice_message=advice_message, url=url)

        # check if the student is ip list
        if student_data in ip_list:
            error_message = "Cannot mark the student present"
            advice_message = "Invalid can't mark twice"
            url = "/markPresent"
            # return error page
            return render_template('error.html', error_message=error_message, advice_message=advice_message, url=url)

        # store the ip address of the student 
        ip_list.append(user_ip)

        # store the student data in the list 
        student_marked_list.append(student_data)

        return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
