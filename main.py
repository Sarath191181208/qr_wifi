import os
import socket

from flask import Flask, render_template, request
from generate_qr import create_qr, get_qr_path, save_qr

import logging

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
logging.basicConfig(filename="flask_log.log", level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# This is the list to track the students who are marked present
student_marked_list = list()
# This is ip list to track the ip address of the students
ip_list = list() 


@app.route("/")
def index():
    user_ip = request.remote_addr

    if user_ip != "127.0.0.1":
        return render_template(
            "error.html",
            error_message="Access Denied",
            advice_message="You are not allowed to access this page",
            url="/markPresent",
        )

    link = f"http://{IPAddr}:5000/"
    hotspot_qr = create_qr(link)
    hotspot_path = get_qr_path('ht.png')
    save_qr(hotspot_qr, hotspot_path)

    mark_present_qr = create_qr(link)
    mark_present_qr_path = get_qr_path('qr.png')
    save_qr(mark_present_qr, mark_present_qr_path)

    return render_template("showQR.html", qr1_path="ht.png", qr2_path="qr.png")


@app.route("/markPresent", methods=["POST", "GET"])
def markPresent():
    user_ip = request.remote_addr
    logging.info(f"User IP: {user_ip}")
    if request.method == "GET":
        return render_template("attendanceForm.html")
    if request.method == "POST":
        # reading the student data
        logging.info(request.form)
        student_data = request.form.get("student_id")
        # if student data is not provided
        if not student_data:
            error_message = "Student ID not provided"
            advice_message = "Please provide the student ID"
            url = "/markPresent"
            # return error page
            return render_template(
                "error.html",
                error_message=error_message,
                advice_message=advice_message,
                url=url,
            )

        # check if the student is already marked present
        if student_data in student_marked_list:
            error_message = "Cannot mark the student present"
            advice_message = "Student already marked present"
            url = "/markPresent"
            # return error page
            return render_template(
                "error.html",
                error_message=error_message,
                advice_message=advice_message,
                url=url,
            )

        # check if the student is ip list
        if student_data in ip_list:
            error_message = "Cannot mark the student present"
            advice_message = "Invalid can't mark twice"
            url = "/markPresent"
            # return error page
            return render_template(
                "error.html",
                error_message=error_message,
                advice_message=advice_message,
                url=url,
            )

        # store the ip address of the student
        ip_list.append(user_ip)

        # store the student data in the list
        student_marked_list.append(student_data)

        return render_template("success.html")

    error_message = "Something went wrong"
    advice_message = "Invalid route this shouldn't happen"
    url = "/markPresent"
    # return error page
    return render_template(
        "error.html",
        error_message=error_message,
        advice_message=advice_message,
        url=url,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
