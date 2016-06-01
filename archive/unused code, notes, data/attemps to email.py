#email??
#http://stackoverflow.com/questions/19679820/send-pandas-dataframe-data-as-html-e-mail
import smtplib
from email.mime.text import MIMEText

final_df.to_csv('data_cocktail.csv')

filename = "data_cocktail.csv"
f = file(filename)
attachment = MIMEText(f.read(),'html')
msg.attach(attachment)