from flask_api import status
from flask import Flask, request, jsonify

import json
import pandas as pd
from datetime import datetime
from collections import OrderedDict

# local
from ifsc_data_class import IfscModel
from statsclass import StatisticsModel
from constants import *
from validation_errors import *


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# globals
ifsc_records = {}
leaderboard_records = {}
sorted_leaderboard_records = []
bank_statitistics_records = []
# globals ends

# helpers
def ifsc_search(ifsc_code):
    '''Returns: ifsc object from search of ifsc_code in ifsc_records'''
    try: 
        res = ifsc_records[ifsc_code] if ifsc_code in ifsc_records else None
        return res 
    except Exception as err:
        # print("Oops!", err, "occured")
        return ISE()
# helpers end


# create your views here

@app.route('/', methods = ['GET'])
def home():
    '''starting api'''
    try:
        return jsonify({
            'status_code': status.HTTP_200_OK,
            'success': True, 
            'message': 'Welcome user', 
        })
    except Exception as err:
        # print("Oops!", err, "occured")
        return ISE()

@app.route('/ifsc-search', methods = ['GET'])
def ifsc_query():
    '''
    The function for searching bank details with ifsc code.
    
    Parameters:
        ifsc_code (String): The code to be searched.
    
    Returns:
        results: a list contains the ifsc bank data.
    '''
    try:
        # query param
        ifsc_code = request.args.get('ifsc_code')

        if not ifsc_records: return server_error()
        if not ifsc_code is not None and len(ifsc_code) != 11: return badreq_error('ifsc_code required|not validated!')

        searched_data = ifsc_search(ifsc_code)
        if not searched_data: return notfound_error() 

        # statistics update
        now = datetime.now() # current date and time
        date_time = now.strftime("%d/%m/%Y, %H:%M:%S.%f")
        bank_statitistics_records.append(StatisticsModel(ifsc_code, date_time).__dict__)

        return jsonify({
            'status_code': status.HTTP_200_OK,
            'success': True, 
            'message': 'Result found!', 
            'data': searched_data
        })
    except Exception as err:
        # print("Oops!", err, "occured")
        return ISE()


@app.route('/leaderboard', methods = ['GET'])
def bank_leaderboard_query():
    '''
        The function for bank leaderboard data in ASC|DESC order with fetchcount.
        
        Parameters:
            sortorder (String): the sorting order ASC|DESC.
            fetchcount (String): the counts to be fetched.
        
        Returns:
            results: a list contains the banks leaderboard data.
        '''
    try:
        leaderboard_len = len(sorted_leaderboard_records)
        if leaderboard_len <= 0: return server_error()

        # query params
        sortorder = request.args.get('sortorder')
        fetchcount = request.args.get('fetchcount')
        
        # validations
        if not sortorder: sortorder = 'DESC' 
        if not fetchcount: fetchcount = 10
        if leaderboard_len < int(fetchcount) or int(fetchcount) == 0: return fetchcount_error(leaderboard_len)
        if sortorder not in sort_list: return sortorder_error()
    
        leaderboard_data = None
        if sortorder == 'DESC':
            leaderboard_data = OrderedDict(sorted_leaderboard_records[:-int(fetchcount)-1:-1])
        else:
            leaderboard_data = OrderedDict(sorted_leaderboard_records[:int(fetchcount)])
        if not leaderboard_data: return notfound_error()
        # for keys in leaderboard_data:
        #     leaderboard_data[keys] = int(leaderboard_data[keys])
        return jsonify({
            'status_code': status.HTTP_200_OK, 
            'success': True,
            'message': 'Found!', 
            'data': leaderboard_data
        })
    except Exception as err:
        # print("Oops!", err, "occured")
        return ISE()


@app.route('/statistics', methods = ['GET'])
def statistics_query():
    '''
    The function to retrieve searched ifsc code with timestamp data.
    
    Parameters:
        sortorder (String): the sorting order ASC|DESC.
        fetchcount (String): the counts to be fetched.
    
    Returns:
        results: a list contains the ifsc leaderboard data.
    '''
    try:
        records_length = len(bank_statitistics_records)          
        if records_length <= 0: return notfound_error()

        # query params
        sortorder = request.args.get('sortorder')
        fetchcount = request.args.get('fetchcount')
        
        if not sortorder: sortorder = 'ASC'
        if not fetchcount: fetchcount = 'ALL'

        if fetchcount == "ALL": fetchcount = records_length
            
        if records_length < int(fetchcount) or int(fetchcount) == 0: return fetchcount_error(records_length)
        if sortorder not in sort_list: return sortorder_error()
            
        statistics_data = []
        if sortorder == 'DESC':
            if records_length == int(fetchcount):
                statistics_data = bank_statitistics_records[::-1]
            else:
                statistics_data = bank_statitistics_records[:-int(fetchcount)-1:-1]
        else:
            statistics_data = bank_statitistics_records[0: int(fetchcount)]

        if not statistics_data: return notfound_error()
        return jsonify({
            'status_code': status.HTTP_200_OK, 
            'success': True,
            'message': 'Found!', 
            'data': statistics_data
        })
    except Exception as err:
        # print("Oops!", err, "occured")
        return ISE()





# Data loading on server startup
try:
    print('\nDATA LOADING STARTED...')

    # IFSC data 
    workbook1 = pd.read_excel(workbook_path, sheet_name='Sheet1')
    workbook1 = workbook1.fillna('NA')
    # workbook1.head()
    for i in range(0, len(workbook1)):
        ifsc_object = IfscModel(workbook1['BANK'][i], workbook1['IFSC'][i], str(workbook1['MICR CODE'][i]), workbook1['BRANCH'][i], workbook1['ADDRESS'][i], workbook1['STD CODE'][i], str(workbook1['CONTACT'][i]), workbook1['CITY'][i], workbook1['DISTRICT'][i], workbook1['STATE'][i])
        ifsc_records[workbook1['IFSC'][i]] = ifsc_object.__dict__
    # IFSC data ends

    # bank leaderboard data
    workbook2 = pd.read_excel(workbook_path, sheet_name='Pivot Table_Sheet1_1')
    workbook2 = workbook2.fillna('NA')
    # workbook2.head()
    for j in range(1, len(workbook2)):
        leaderboard_records[str(workbook2['BANK'][j])] = int(workbook2['Count - BANK'][j])
    # asc order sort 
    sorted_leaderboard_records = sorted(leaderboard_records.items(), key=lambda x: x[1])
    # bank leaderboard data ends

    print('100%')
    print('DATA LOADING COMPLETED !\n')
except Exception as err:
    # print('ERROR', err)
    print('ERROR LOADING DATA !\n')
# Data loading ended

# main
if __name__ == '__main__':
    app.run(port = 5000, debug = False)
    