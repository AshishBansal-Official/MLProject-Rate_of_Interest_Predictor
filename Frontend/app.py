from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)


def calculateInterest(amount_requested, loan_length, loan_purpose, debt_to_income_ratio, home_ownership, monthly_income, fico_range, open_credit_lines, revolving_credit_balance, inquiries_in_last_6_months, employment_length):

    with open(r"My_random_forest_model.pickle", 'rb') as f:
        lm_model = pickle.load(f)
    df = pd.read_csv(r"test1.csv")
    new_row = pd.DataFrame([[0]*df.shape[1]], columns=df.columns)
    df = df.append(new_row, ignore_index=True)
    df['Amount.Requested'] = int(float(amount_requested))
    df['loan_period'] = int(float(loan_length))
    df['Loan_purpose_car'] = 1 if loan_purpose == 0 else 0
    df['Loan_purpose_credit_card'] = 1 if loan_purpose == 1 else 0
    df['Loan_purpose_debt_consolidation'] = 1 if loan_purpose == 2 else 0
    df['Loan_purpose_educational'] = 1 if loan_purpose == 3 else 0
    df['Loan_purpose_home_improvement'] = 1 if loan_purpose == 4 else 0
    df['Loan_purpose_house'] = 1 if loan_purpose == 5 else 0
    df['Loan_purpose_major_purchase'] = 1 if loan_purpose == 6 else 0
    df['Loan_purpose_medical'] = 1 if loan_purpose == 7 else 0
    df['Loan_purpose_moving'] = 1 if loan_purpose == 8 else 0
    df['Loan_purpose_other'] = 1 if loan_purpose == 9 else 0
    df['Loan_purpose_small_business'] = 1 if loan_purpose == 10 else 0
    df['Loan_purpose_vacation'] = 1 if loan_purpose == 11 else 0
    df['Loan_purpose_wedding'] = 1 if loan_purpose == 12 else 0
    df['Debt.To.Income.Ratio'] = int(float(debt_to_income_ratio))
    df['HO_MORTGAGE'] = 1 if home_ownership == 'Mortgage' else 0
    df['HO_OWN'] = 1 if home_ownership == 'Own' else 0
    df['HO_RENT'] = 1 if home_ownership == 'Rent' else 0
    df['Monthly.Income'] = int(float(monthly_income))
    df['Fico_Score'] = int(float(fico_range))
    df['Open.CREDIT.Lines'] = int(float(open_credit_lines))
    df['Revolving.CREDIT.Balance'] = int(float(revolving_credit_balance))
    df['Inquiries.in.the.Last.6.Months'] = int(
        float(inquiries_in_last_6_months))
    df['Employment.Length'] = int(float(employment_length))
    predictions_test = str(round(float(lm_model.predict(df)), 2))
    print('Interest is : ' + predictions_test)
    return predictions_test


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/interest')
def getInterest():
    interest_rate = calculateInterest(request.args['amount_requested'], request.args['loan_length'], request.args['loan_purpose'], request.args['debt_to_income_ratio'], request.args['home_ownership'],
                                      request.args['monthly_income'], request.args['fico_range'], request.args['open_credit_lines'], request.args['revolving_credit_balance'], request.args['inquiries_in_last_6_months'], request.args['employment_length'])
    return render_template('interest.html', interest=interest_rate)


if __name__ == '__main__':
    app.run()
