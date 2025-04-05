import joblib

# Load the trained model and vectorizer
model = joblib.load(r'C:\Users\akash\Downloads\MakeUC2024-NewMain\logistic_regression_model.joblib')
vectorizer = joblib.load(r'C:\Users\akash\Downloads\MakeUC2024-NewMain\vectorizer.joblib')

def classify_email(email_text):
    # Preprocess the email (convert to lowercase)
    email_text = email_text.lower()
    
    # Transform the email text using the loaded vectorizer
    email_tfidf = vectorizer.transform([email_text])
    
    # Predict using the loaded model
    prediction = model.predict(email_tfidf)
    
    # Interpret the result
    if prediction[0] == 1:
        return "Phishing Email"
    else:
        return "Safe Email"

# Example phishing email text
phishing_email = """
Dear Customer,

We have noticed some unusual activity in your account, and for your security, we have temporarily suspended it. To regain access, please verify your account information immediately.

Click the link below to confirm your identity and secure your account:
[https://bank-secure-verify.com](https://bank-secure-verify.com)

Failure to act within 24 hours will result in permanent suspension of your account.

Thank you for your prompt attention to this matter.

Sincerely,
The Security Team
"""

# Example safe email text
safe_email = """Hello Nipun,

Thanks so much for reaching out!!  I am sorry it took me so long to respond.  The last month has been a bit crazy. 

With our staff being primarily students, part of the difficulty of hiring is making sure to space peoples graduation dates out so that we don't have a large amount of paid staff leaving at one time.  With that consideration I have had some people that I would LOVE to hire, but am not able to due to their anticipated graduation and how many people we would have leaving at the same time.

Currently our potential staffing would not allow for me to hire any additional people with graduation dates in 2027.  That is not saying this could not change, but currently it is not something I could do.  If there are any changes, and it would make sense for us to talk more, I will reach out.

Very sorry, I know this is not what you wanted to hear!  

I definitely appreciate you!

Best,
Chris"""


# Classify the email
result = classify_email(phishing_email)
print("The email is classified as:", result)

result2 = classify_email(safe_email)
print("The email is classified as:", result2)