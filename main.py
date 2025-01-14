import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add_donation', methods=['GET', 'POST'])
def add_donation():
    if request.method == 'POST':
        
        temp_list = []

        for donor in Donor().select():
            temp_list.append(donor.name)

        if request.form['name'] not in temp_list:
            donor = Donor(name=request.form['name'])
            donor.save()

        donation = Donation(value=request.form['amount'],
                            donor=Donor.select().where(Donor.name == request.form['name']).get())
        donation.save() 

        return redirect(url_for('all'))

    else:
        return render_template('add_donation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
