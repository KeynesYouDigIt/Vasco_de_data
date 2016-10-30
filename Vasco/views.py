'''Pretty straight forward flask middle layer, some of the actual work
and most of the actual calls against the db are done in this file'''

from flask import render_template, url_for, request, redirect, flash, abort, Response
from sqlalchemy.sql import text
from datetime import datetime
import Vasco
from Vasco import app
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def ind():
    """This is the home page, it welcomes the user and builds a form from
    Vasco."""
    avail_form=Vasco.order_takers.Availibility_order()
    try:
        get=Vasco.order_takers.get_countries_etld()
        #above is tuples, not just list. Below makes a list.
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
        usr='!', 
        avail_form=avail_form
        )

@app.route('/showmedata/<order_y>___<order_c>', methods=['GET','POST'])
def show_avail(order_y,order_c):
    """
    This page appears after submitting a form on the home page with
    a list of indicators that exist for at least one combination 
    of years and countries requested.

    Upon submitting this form, the final data set is built 
    and sent to the client's browser for download.

    """
    final='Please select. don\'t be scared if the list is long! for now you can hit ctrl + f to search on most browsers. \n by the end of this year, there will be a smoother selection experience that will help you find your data.' 
    #first step is to take years and countries and turn the strings back to lists, then select all valid data accordingly.
    order_y=order_y.replace("'","").strip('[').strip(']').split(',')
    order_c=order_c.replace("'","").strip('[').strip(']').split(',')
    order_c=[x.strip() for x in order_c]
    order_y=[x.encode('ascii') for x in order_y]
    order_c=[x.encode('ascii') for x in order_c]

    #the years and countries are now ready to be based as a variable to our db querey to get the availible indicators.
    first_query = """SELECT * FROM literal 
                WHERE year IN :years 
                AND ent_id IN (select id from ent where name in  :names)"""
    
    full_data_points = Vasco.db.engine.execute(text(first_query), 
        {'years': tuple(order_y),'names': tuple(order_c)}).fetchall()
    data_points_as_tuples=[]
    #WTForms is built on tuples, not lists. making tuples to populate here.
    for point in full_data_points:
        if len(point) > 0:
            points=(str(point[4]),str(point[4]))
            if points not in data_points_as_tuples:
                data_points_as_tuples.append(points)
            else:
                pass
        else:
            pass
    indic_form=Vasco.order_takers.Data_set_order()
    indic_form.indicators.choices=data_points_as_tuples
    #the form is now built based on the indicators in the database.

    if indic_form.validate_on_submit():
        #the indicators now selected, we can build the necessary query to finish the data set
        query = """SELECT name, year, value, display_name
               FROM literal
               INNER JOIN ent ON ent_id = ent.id
               WHERE display_name IN :display_name
                 AND name IN :name
                 AND year IN :years
                 """
        data_return = Vasco.db.engine.execute(text(query), 
            {'display_name': tuple(indic_form.indicators.data),
            'name': tuple(order_c), 
            'years': tuple(order_y)}).fetchall()
        final_list=[]
        #this will be a list of dictionaries, with each dict as a single data point.
        #Pandas converts this seamlessly to a DataFrame
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

        if indic_form.send_descriptions.data==True:
            query = """SELECT p_name, p_description
                FROM meta
                WHERE p_name IN :display_name
                 """
            data_return_desc = Vasco.db.engine.execute(text(query), 
                {'display_name': tuple(indic_form.indicators.data)}).fetchall()
        else:
            data_return_desc = ''
        desc_list=[]
        for toople in data_return_desc:
            desc_point={}
            desc_point[toople[0]]=toople[1]
            desc_list.append(desc_point)
        final=final_list
        final_df=pd.DataFrame(final)
        descriptions_df=pd.DataFrame(desc_list)
        #next few lines clean and present the DataFrame properly
        years_column=final_df.pop('Year')
        countries_column=final_df.pop('Country')
        final_df.insert(0, 'Year', years_column)
        final_df.insert(0, 'Country', countries_column)
        final_df.set_index(['Country','Year'])
        final_df=final_df.append(descriptions_df)
        filename='Vasco_data_set'
        #keep renaming file until name is unique and send when unique
        while filename in os.listdir(os.getcwd()):
            increment=0
            filename=filename+(str(increment))
            increment+=1
        filename=filename+'.csv'
        final_df.to_csv(filename,header=True,engine='python')
        with open(filename, 'r') as fp:
            read_csv=fp.read()

        #email the data if requested
        if indic_form.Email.data:
            msg = MIMEMultipart()
            msg['Subject'] = 'Your dataset from Vasco de Data'
            
            sndr='VascoSendsData@gmail.com'
            recvr=str(indic_form.Email.data)
            
            msg['From'] = sndr
            msg['To'] = recvr
            filename=str(filename)
            attachment = MIMEBase('csv','csv')
            attachment.set_payload(read_csv)
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", 
                "attachment", 
                filename=filename)
            msg.attach(attachment)
            #fp.close()
            username = sndr
            password = 'DoYou52186Remember'
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.login(username,password)
            server.sendmail(from_addr=sndr, to_addrs=recvr, msg=msg.as_string())
            server.quit()
        #send file as direct response
        return Response(read_csv, 
                mimetype='text/csv',
                headers={"Content-disposition":
                 "attachment; filename="+filename})

    return render_template('avail.html', 
        htwo='Clean and Uniform',
        indic_form=indic_form,
        final=final
        )


@app.route('/blog')
def blog_it():
    """
    The blog content is scheduled for September,
    will appear on this page
    """
    title='About'
    post='This will be the only post I write for some time, I have had to get involved with alot of other projects to keep growing as a developer.\
     Vasco de data was inspired by many long nights as a researcher attempting to clean and work with public data to make it uniform and ready for modeling.\
     \n\nThis site does exactly that in a way that is quick and easy to use. Right now, it only works off of what is availible from the world ank and what \
     is availile from the UN Human Development report.\
    Once I get the chance to work more on tis project, I plan on adding more sources and functionality.\
     \n\n\n Of course, it helps to know what people want! please email me with feedback, ideas, or other cool projects at vince.buscarello@gmail.com'
    return render_template('blog.html',
        post=post,
        post_title=title
        )


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500