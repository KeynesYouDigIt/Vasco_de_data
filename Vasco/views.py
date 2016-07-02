from flask import render_template, url_for, request, redirect, flash, abort
from sqlalchemy.sql import text
from datetime import datetime
from Vasco import *
from Vasco.models import *
from Vasco.order_takers import *
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


'''this is the only current connection between the front end an the data itself. 
Within the next couple weeks, I plan on replacing it with a robust system that calls 
the public data APIs and stores the data in a Postgres database for easy retrival.'''

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def ind():
    avail_form=Availibility_order()
    try:
        get=get_countries_etld()
        countries_etld=[]
        for country_tuple in get:
            countries_etld.append(country_tuple[1])
    except:
        countries_etld='nothing yet'
    if avail_form.validate_on_submit():
        order_y=avail_form.years.data
        order_c=avail_form.countries.data
        return redirect(url_for('show_avail', order_y=order_y, order_c=order_c))

    return render_template('home.html', 
        htwo='Clean and Uniform',
        countries_etld=countries_etld,
        #above gets results as list of tuples
        usr='!!!', 
        avail_form=avail_form
        )

@app.route('/showmedata/<order_y>___<order_c>', methods=['GET','POST'])
def show_avail(order_y,order_c):
    final='final order wil display here'
    order_y=order_y.replace("'","").strip('[').strip(']').split(',')
    order_c=order_c.replace("'","").strip('[').strip(']').split(',')
    order_c=[x.strip() for x in order_c]
    #order_c=[x[1:-1] for x in order_c]
    order_y=[x.encode('ascii') for x in order_y]
    order_c=[x.encode('ascii') for x in order_c]
    #quoted=" ' "
    #order_c=[x+quoted for x in order_c]
    first_query = """SELECT * FROM literal 
                WHERE year IN :years 
                AND ent_id IN (select id from ent where name in  :names)"""
    
    full_data_points = db.engine.execute(text(first_query), {'years': tuple(order_y),'names': tuple(order_c)}).fetchall()
    data_points_as_tuples=[]
    for point in full_data_points:
        if len(point) > 0:
            points=(str(point[4]),str(point[4]))
            if points not in data_points_as_tuples:
                data_points_as_tuples.append(points)
            else:
                pass
        else:
            pass
    empty_indic_form=Data_set_order()
    empty_indic_form.indicators.choices=data_points_as_tuples
    indic_form=empty_indic_form
    get_email='then I\'ll get your email here :)'

    if empty_indic_form.validate_on_submit():
        query = """SELECT name, year, value, display_name
               FROM literal
               INNER JOIN ent ON ent_id = ent.id
               WHERE display_name IN :display_name
                 AND name IN :name
                 AND year IN :years

                 """
        data_return = db.engine.execute(text(query), {'display_name': tuple(indic_form.indicators.data),'name': tuple(order_c), 'years': tuple(order_y)}).fetchall()
        #FINALLY data_return works as expected
        final_list=[]
        for toople in data_return:
            final_point={}
            final_point['Country']=toople[0]
            final_point['Year']=toople[1]
            final_point[toople[3]]=toople[2]

            if len(final_list)>0:
                for i,f in enumerate(final_list):
                    if final_point['Country']==f['Country'] and final_point['Year']==f['Year']:
                        final_list[i].update(final_point)
                        break
                else:
                    final_list.append(final_point)
            else:
                final_list.append(final_point)

        final=final_list
        final_df=pd.DataFrame(final)
        years_column=final_df.pop('Year')
        countries_column=final_df.pop('Country')
        final_df.insert(0, 'Year', years_column)
        final_df.insert(0, 'Country', countries_column)
        final_df.set_index(['Country','Year'])
        filename='Vasco_data_set'
        while filename in os.listdir(os.getcwd()):
            increment=0
            filename=filename+(str(increment))
            increment+=1
        filename=filename+'.csv'
        final_df.to_csv(filename,header=True,engine='python')
        msg = MIMEMultipart()
        msg['Subject'] = 'Your dataset from Vasco de Data'
        
        sndr='VascoSendsData@gmail.com'
        recvr=str(empty_indic_form.Email.data)
        
        msg['From'] = sndr
        msg['To'] = recvr
        filename=str(filename)
        fp = open(filename, 'r')
        attachment = MIMEBase('csv','csv')
        attachment.set_payload(fp.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", 
            "attachment", 
            filename=filename)
        msg.attach(attachment)
        fp.close()
        username = sndr
        password = 'DoYou52186Remember'
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(from_addr=sndr, to_addrs=recvr, msg=msg.as_string())
        server.quit()
        return redirect(url_for('ind'))

    return render_template('avail.html', 
        htwo='Clean and Uniform',
        indic_form=indic_form,
        final=final
        )   



@app.route('/sendmedata')
def send_it():
    
    sendto=str(raw_input('Please enter the email you would like to send this to'))
    # Import smtplib for the actual sending function
    import smtplib

    # Here are the email package modules we'll need
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Your dataset from Vasco de Data'
    sndr='VascoSendsData@gmail.com'
    recvr=str(sendto)
    msg['From'] = sndr
    msg['To'] = recvr

    #content = 'wordsarewords'
    #msg = MIMEText(content)
    #msg.preamble = 'worrds'
    '''throws MultipartConversionError: 
    Cannot attach additional subparts to non-multipart/*'''

    # Now the file itself from get_make_file_params above
    filename=str(file)
    fp = open(filename, 'rb')
    #file=csv.reader(fp)
    attachment = MIMEBase('csv','csv')
    attachment.set_payload(fp.read())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", 
        "attachment", 
        filename=file)
    msg.attach(attachment)
    fp.close()

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500