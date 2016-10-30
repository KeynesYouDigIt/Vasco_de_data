import os
import lxml
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests as rq
import urllib2 as url
from urllib2 import urlopen

'''run me as you would any python file, and watch the typos! this console based UI has few vaidators!!'''

#the below gets a list a Dictionary of ISO codes and their corresponding countries
html = urlopen('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3').read()
BS = BeautifulSoup(html, "lxml")
tds=BS.find_all('td')
herp_it = []
it=-1
for d in tds:
    it += 1
    herp_it.append(it)

herp_it = np.asarray(herp_it)
global iso_dic
iso_dic={}
for t in herp_it:
    s_td=tds[t].string
    if s_td == None:
        pass
    else:
        l_s_td=len(s_td)
        nxt=t+1
        if l_s_td == 3:
            iso_dic.update({tds[nxt].string:s_td})
        else:
            pass

#the below reverses the ISO code dictionary in a new object to get country name using the ISO code
global iso_dic_code_is_key
iso_dic_code_is_key={v: k for k, v in iso_dic.items()}

def get_avail(countries, years):
    '''this is function is the begining of a project to make the original API (archive/Bartender_no_ui.py) modular and flexible. 
    as stated in views.py, I plan on creating a robust system that calls the public data APIs and stores the data in a Postgres database.'''

    order_countries=countries
    order_years=years
    saveas_file_type='csv'
    save_dir=os.getcwd()

    #the below gets a list of dictionaries that constitutes a full library of World Bank indicators
    #the indicators are simply represented by meta data which is converted into actual indicator names below (line 91 and on)

    ###by generating its own iterator it violates 7 PEP 279, I am hoping to fix that soon.
    ###I should be able to test and remove of the global calls soon, as this is not good practice long term.
    indi=rq.get('http://api.worldbank.org/indicators?format=json')
    jindi=indi.json()
    global wb_indi_list
    wb_indi_list=jindi[1]
    global wb_indi_it
    wb_indi_it = []
    it=-1
    for i in wb_indi_list:
        it += 1
        wb_indi_it.append(it)


    #the below gets a list of dictionaries that constitutes a full library of United Nations indicators
    #the indicators are simply represented by id numbers which are converted into actual indicator names below (line 91 and on)
    wb_indi_it=np.asarray(wb_indi_it)
    un_indi=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator')
    jun_indi=un_indi.json()
    global UNHDR_indi_dic
    UNHDR_indi_dic=jun_indi['indicator_name']
    global UNHDR_indi_list
    UNHDR_indi_list=[]
    for i in UNHDR_indi_dic:
        si=str(i)
        UNHDR_indi_list.append(si)
    global UN_indi_it
    UN_indi_it = []
    it=-1
    for i in UNHDR_indi_dic:
        it += 1
        UN_indi_it.append(it)

    UN_indi_it=np.asarray(UN_indi_it)

    #lines 91-165 parse the dictionaries above to check the availibility of every indicator for the specified Countries (or entities) and years
    #if the data exists, it is extracted
    global wb_availibility_dic
    wb_availibility_dic={}
    global wb_checkiftheyhave_list
    wb_checkiftheyhave_list=[]
    global UNHDR_availibility_dic
    UNHDR_availibility_dic={}
    global un_checkiftheyhave_list
    un_checkiftheyhave_list=[]
    global errorlist
    errorlist=[]
    global mislist
    mislist=[]
    for wb_i in wb_indi_it:
        for c in order_countries:
            for y in order_years:
                wb_checkiftheyhave_list.append([c,wb_i,y])

    for UN_i in UN_indi_it:
        for c in order_countries:
            for y in order_years:
                un_checkiftheyhave_list.append([c,UN_i,y])
    num=0
    for wb in wb_checkiftheyhave_list:
        num+=1
        id_as_str=str(wb_indi_list[wb[1]]['id'])
        print 'fething from world bank %s' % num
        raw_wb_avail_call=rq.get('http://api.worldbank.org/countries/' + wb[0] + '/indicators/' + id_as_str + '?per_page=100&date=' + wb[2] +'&format=json')
        wb_avail_json=raw_wb_avail_call.json()
        if str(wb_avail_json[1]) == 'None':
            errorlist.append('http://api.worldbank.org/countries/' + wb[0] + '/indicators/' + id_as_str + '?per_page=100&date=' + wb[2] +'&format=json')
        else:
            value=wb_avail_json[1][0]['value']
            try:
                float(value)
            except TypeError:
                mislist.append([wb[0],id_as_str,wb[2]])
            else:
                key_string=str(wb_avail_json[1][0]['indicator']['value']+' for '+wb[0]+' '+wb[2])
                wb_availibility_dic.update({key_string:wb_avail_json})
            finally:
                pass
    num=0
    for UN in un_checkiftheyhave_list:
        num+=1
        print 'fething from united nations %s' % num
        id_as_str=UNHDR_indi_list[UN[1]]
        raw_un_avail_call=rq.get('http://ec2-52-1-168-42.compute-1.amazonaws.com/version/1/indicator_id/' + id_as_str + '/year/' + UN[2] + '/country_code/' + UN[0])
        UN_avail_json=raw_un_avail_call.json()
        if type(UN_avail_json) == unicode:
            mislist.append(UNHDR_indi_dic[id_as_str])
            mislist.append('for'+UN[0]+UN[2])
        else:
            to_add_to_avail_dic=[UN[0],UN[2],id_as_str,UN_avail_json]
            key_string=str(UN_avail_json['indicator_name'][id_as_str].encode('ascii', 'ignore')+' for '+UN[0]+' '+UN[2])
            UNHDR_availibility_dic.update({key_string:to_add_to_avail_dic})

    wb_finished_avail=[]
    ob=0
    for i in wb_availibility_dic.keys():
        wb_finished_avail.append({})
        wb_finished_avail[ob]['Country']=str(wb_availibility_dic[i][1][0]['country']['value'])
        wb_finished_avail[ob]['Year']=wb_availibility_dic[i][1][0]['date']
        wb_finished_avail[ob][str(wb_availibility_dic[i][1][0]['indicator']['value'])]=wb_availibility_dic[i][1][0]['value']
        ob+=1

    un_finished_avail=[]
    ob=0
    for i in UNHDR_availibility_dic.keys():
        un_finished_avail.append({})
        un_finished_avail[ob]['Country']=str(UNHDR_availibility_dic[i][3]['country_name'][UNHDR_availibility_dic[i][0]])
        un_finished_avail[ob]['Year']=UNHDR_availibility_dic[i][1]
        un_finished_avail[ob][str(UNHDR_availibility_dic[i][3]['indicator_name'][UNHDR_availibility_dic[i][2]].encode('ascii', 'ignore'))]=UNHDR_availibility_dic[i][3]['indicator_value'][0][3]
        ob+=1

    both=un_finished_avail+wb_finished_avail

    return both


def getorder():
    not_iso_order_countries=raw_input("Hey there, which countries in your custom data coctail tonight? Please seperate each with a comma, don't just throw em all me at once. They are case sensitive (its an entire country! don't be lazy.)")
    not_iso_order_countries=str(not_iso_order_countries)
    not_iso_order_countries=not_iso_order_countries.split(',')
    global order_countries
    order_countries = []
    for co in not_iso_order_countries:
        if co in iso_dic:
            order_countries.append(str(iso_dic[co]))
        else:
            print('I cant find the ISO code for %s , is that country spelled right?') % co
            YN=raw_input('Care to try that country name agin? Type Y for yes or N for no')
            if YN in ('n', 'no', 'N', 'No', 'NO'):
                print('OK, on we go')
            elif YN in ('y','ye', 'yes','Yes','Y','YEs','YES'):
                correction=raw_input('ok type that (or those) country name(s) again')
                if correction in iso_dic:
                    print('oh you meant %s !! why didnt you say so? yeah I got their ISO code we are all set to move on.') % correction
                else:
                    YNtwo=raw_input('still not gettin it. Start over (Start) or Move on without this country (Go)')
                    if YNtwo == 'Start' or 'start':
                        getorder()
                    else:
                        pass
            else:
                YN=raw_input('what? Y for yes N for no')
    global order_years

    order_years=str(raw_input('Got it! For which years do you need data? seperate each with a comma as well'))
    order_years=order_years.split(',')
    #print order_countries
    #print type(order_years[0])
    extracted=get_avail(countries=order_countries,years=order_years)
    get_make_file_params(extracted)


def get_make_file_params(data):
    glass=str(raw_input('Please enter, without the dot, the file type you need your data in. Ill let you know if we have it.\nCSV and JSON are tested, but you can try an alternate if you\'d like.'))
    if glass in ['csv','CSV','Excel','excel','C','Cs','CS']:
        make_files(['csv'],data)

    elif glass in ['json','JSON','Json','jayson','javascript']:
        make_files(['json'])

    else:
        print('well Im not really programmed for that')
        do=raw_input('I can try to save to a %s file and see what happens, wanna try?[y/n]')
        if do in ('n', 'no', 'N', 'No', 'NO'):
            print('arighty, so far its just CSV and JSON that are programmed to be returned properly. Try one of those.') 
            get_make_file_params(data)
        elif do in ('y','ye', 'yes','Yes','Y','YEs','YES', 'ok', 'Ok', 'OK', 'k'):
            make_files([glass],data)
        else:
            print('thats a yes or no question, please try again')
            get_make_file_params(data)
    return glass


def email_file(file):

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


    # Send the email via our own SMTP server.
    username = sndr
    password = 'DoYou52186Remember'
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_addr=sndr, to_addrs=recvr, msg=msg.as_string())
    server.quit()
    print 'that data set has been emailed! lets make another'
    getorder()


def make_files(ftype, data):

    try:
        name=raw_input('what would you like to call the file? please do not include file type, and its a file name so no slashes or periods!')
        name.strip(',''!''/')
    except:
        print 'something is wrong with that name, try again'
        make_files(ftype, data)

    ftype=ftype[0]
    fullname=name+'.'+ftype
    print fullname+' ready to be created'

    if ftype=='csv':
        duff=pd.DataFrame(data)
        cols = duff.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        duff = duff[cols] 
        duff.to_csv(fullname)
        print('done, csv file created')

    elif ftype=='json':
        with open(fullname, 'w') as fp:
            json.dump(data, fp)
        print('done, json file created')
    else:
        with open(fullname, 'w') as fp:
            try:
                fp.write(data)
                fp.close()
                print('Holy crap it worked!! I think. At least there wasnt an error.')
            except:
                print('that didnt work - there was an error. saving as csv')
                cols = duff.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                duff = duff[cols] 
                duff.to_csv(fullname)
                print('done, csv file created')

    email_file(fullname)


getorder()