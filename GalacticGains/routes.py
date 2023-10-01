from GalacticGains import app
from flask import render_template, url_for, request, redirect, flash
import GalacticGains.forms
import GalacticGains.database
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd

app.config['SECRET_KEY']='RVCE'
@app.route('/')
@app.route('/home')
@app.route('/Home')
def home():  # put application's code here
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
@app.route('/Login', methods=['GET', 'POST'])
def login():
    form = GalacticGains.forms.LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if GalacticGains.database.verifyLogin(email, password):
            return redirect(url_for("home"))

        return render_template("login.html", errorMsg="Invalid email id or password", form=form)

    return render_template("login.html", form=form)

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signUp', methods=['GET', 'POST'])
@app.route('/SignUp', methods=['GET', 'POST'])
def signUp():
    form = GalacticGains.forms.SignUpForm()

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        confirmPassword = form.confirmPassword.data

        errorMessage = GalacticGains.database.verifyAccountCreation(email, password, confirmPassword)

        if errorMessage:
            return render_template("signUp.html", form=form, errorMessage=errorMessage)

        # Rest of your logic for adding data to the database

        return redirect(url_for("home"))

    return render_template("signUp.html", form=form)
import requests
IEX_CLOUD_API_TOKEN = 'pk_017dddcdcb664dd8867d6817b089959a'

@app.route('/rtd')
def temp():
    return render_template('rtdForm.html', title='Stosk-O-Matic')

import requests

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        company_name = request.form['ticker']
        api_url = f'https://cloud.iexapis.com/stable/stock/{company_name}/quote?token={IEX_CLOUD_API_TOKEN}'

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()

            # Fetch latest news for the company
            news_endpoint = f'https://cloud.iexapis.com/stable/stock/{company_name}/news/last/5?token={IEX_CLOUD_API_TOKEN}'
            news_response = requests.get(news_endpoint)
            news_data = news_response.json()
            latest_news = [{'headline': news_item['headline'], 'url': news_item['url']} for news_item in news_data]

            # Fetch company information
            company_info_endpoint = f'https://cloud.iexapis.com/stable/stock/{company_name}/company?token={IEX_CLOUD_API_TOKEN}'
            company_info_response = requests.get(company_info_endpoint)
            company_info_data = company_info_response.json()

            # Include company data
            company_data = {
                'name': company_info_data['companyName'],
                'sector': company_info_data['sector'],
                'industry': company_info_data['industry'],
                'CEO': company_info_data['CEO'],
                'description': company_info_data['description']
            }

            return render_template('stock_data.html', title=company_name, data=data, latest_news=latest_news, company_data=company_data)
        else:
            # If the response status code is not 200, raise an exception to trigger the error handling
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        # If there was an error with the API request, render an error page
        print(f"unsuccessful : {e}")
        return render_template('error.html', error_message='Error fetching stock data. Please try again later.')

    except KeyError:
        # If the required form field 'ticker' is missing or incorrect, render an error page
        print(f"Unsuccessful")
        return render_template('error.html', error_message='Invalid company ticker. Please enter a valid ticker symbol.')


@app.route('/developer')
@app.route('/Developer')
def developer():
     return (render_template('developer.html', title='Developer'))





import json

@app.route('/chart', methods=['POST'])
def chart():
    years = request.form.get('timeYears')
    if years is None:
        # Handle the case when 'timeYears' is missing in the form data
        return "Please enter a valid value for 'timeYears'."

    url = f"https://cloud.iexapis.com/stable/stock/META/chart/{years}y?token={IEX_CLOUD_API_TOKEN}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        raw_data = response.json()
        extracted_data = []

        for data_point in raw_data:
            price = data_point["close"]
            date = data_point["date"]
            extracted_data.append({"price": price, "date": date})

        with open("extracted_data.json", "w") as f:
            json.dump(extracted_data, f, indent=4)

        print("Data extraction successful. Results saved in 'extracted_data.json'.")

        return render_template('chart.html', data=extracted_data)

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions (e.g., connection errors)
        error_message = f"Error fetching data: {e}"
        return render_template('error.html', error_message=error_message)

    except KeyError as e:
        # Handle missing keys in the response data (e.g., 'close' or 'date' not found)
        error_message = f"Data format error: {e}"
        return render_template('error.html', error_message=error_message)



@app.route('/StockBuilder', methods=['GET', 'POST'])
def feature2():
    if request.method == 'POST':
        try:
            numberOfCompanies = int(request.form.get('numberOfCompanies'))
            # Limit the number of companies to a maximum of 50
            numberOfCompanies = min(numberOfCompanies, 50)
        except ValueError:
            flash('Invalid input. Please enter a valid number of companies (integer between 1 and 50).', 'error')
            return redirect('/feature2')  # Redirect back to the form page

        portfolio_value = 0  # Initialize portfolio value with a default value
        errors = []

        for i in range(numberOfCompanies):
            ticker = request.form.get('ticker' + str(i))
            shares = request.form.get('shares' + str(i))

            # Check if shares is not None and is a valid positive integer
            if shares is not None and shares.isdigit() and int(shares) > 0:
                shares = int(shares)
            else:
                errors.append(f'Invalid input for shares of company {i + 1}. Please enter a valid positive integer.')
                continue

            api_url = f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token={IEX_CLOUD_API_TOKEN}'
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                latest_price = data.get('latestPrice')
                if latest_price is not None:
                    portfolio_value += shares * latest_price
                else:
                    errors.append(f'Unable to get the latest price for company {i + 1}. Please try again later.')
            else:
                errors.append(f'Error fetching data for company {i + 1}. Please try again later.')

        if errors:
            for error in errors:
                flash(error, 'error')

    else:
        numberOfCompanies = 0  # Default value for the number of companies
        portfolio_value = 0  # Initialize portfolio value with a default value

    return render_template('StockBuilder.html', numberOfCompanies=numberOfCompanies, portfolio_value=portfolio_value)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_message='Page not found.', error_code=404), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error_message='Internal server error.', error_code=500), 500

@app.route('/model')
def model():
    return render_template('model.html', title='model')
