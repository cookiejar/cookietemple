from flask import request, render_template
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
from ..app import app


@app.route('/contact_request', methods=['POST'])
def contact_request():
    # validate form
    if not request.form['name'] or not request.form['email'] or not request.form['message'] or "@" not in request.form['email']:
        return render_template("contact_error.html")

    msg = Message("Personal website request by: " + request.form['name'],
                  sender=request.form['email'],
                  recipients=['{{cookiecutter.email}}'])
    sent_by = "The request was sent by: " + request.form['name'] + " with the contact e-mail: " + request.form['email'] + "\n\n"
    message = "His/her message is: \n\n" + request.form['message']
    msg.body = sent_by + message
    if len(request.form['emailSPAM']) == 0:
        Thread(target=send_async_email, args=(app, msg)).start()
        return render_template("contact_successful.html")
    return render_template("errors/410.html")


def send_async_email(app, msg):
    mail = Mail(app)
    with app.app_context():
        mail.send(msg)
