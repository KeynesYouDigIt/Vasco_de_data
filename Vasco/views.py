from flask import render_template, url_for, request, redirect, flash, abort
from sqlalchemy.sql import text
from datetime import datetime
from Vasco import *
from Vasco.models import *
from Vasco.order_takers import *
import pandas as pd
import shlex

'''this is the only current connection between the front end an the data itself. 
Within the next couple weeks, I plan on replacing it with a robust system that calls 
the public data APIs and stores the data in a Postgres database for easy retrival.'''

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def ind():
    avail_form=Availibility_order()
    get=get_countries_etld()
    countries_etld=[]
    for country_tuple in get:
        countries_etld.append(country_tuple[1])

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
            final_list.append(final_point)
        final=final_list
        final_df=pd.DataFrame(final)
        final_df=final_df.set_index(['Country'],['Year'])
        final_df=final_df.reindex_axis(final_df.index)
        try:
            final_df.to_csv('final'+'.csv',header=True,engine='python')
        except:
            final_df.to_csv('final2'+'.csv',header=True,engine='python')

    return render_template('avail.html', 
        htwo='Clean and Uniform',
        indic_form=indic_form,
        final=final
        )   



@app.route('/sendmedata')
def send_it():
    pass

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500