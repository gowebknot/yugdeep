from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

import json
import urllib.request

# locals
from .validation import isValidIFSCode, isValidSortOrder, isValidCount
from .constant_urls import ifsc_search_url, leaderboard_url, statistics_url


# globals.
cached_ifsc = {}
ifsc_hit_count = {}
URL_hit_count = {'IFSC_Search': 0, 'Leaderboard': 0, 'Statistics': 0}
# globals end.

# helpers.
# function to check ifsc_code in cache.
def check_in_cache(ifsc_code):
    response = cached_ifsc[ifsc_code] if cached_ifsc.get(ifsc_code) is not None else False
    return response

# function to cache the response.
def caching_response(ifsc, result):
    if result.get('success'):
        cached_ifsc[ifsc] = result.get('data')
        return True
    else:
        return False

# function to create|update per ifsc_code hit count.
def manage_ifsc_hit_count(ifsc):
    if ifsc_hit_count.get(ifsc): 
        ifsc_hit_count[ifsc] = int(ifsc_hit_count[ifsc]) + 1  
    else:
        ifsc_hit_count[ifsc] = 1

# function to update ifsc search api url hit count.
def update_ifsc_search_api_count():
    URL_hit_count['IFSC_Search'] = URL_hit_count['IFSC_Search'] + 1
    return True

# function to update leaderboard api url hit count.
def update_leaderboard_api_count():
    URL_hit_count['Leaderboard'] = URL_hit_count['Leaderboard'] + 1
    return True

# function to update statistics api url hit count.
def update_statistics_api_count():
    URL_hit_count['Statistics'] = URL_hit_count['Statistics'] + 1
    return True
# helpers ends.


# Create your views here.

class IFSC_Search(APIView):
    def get(self, request):
        '''
        The function for searching bank details with ifsc code.
        
        Parameters:
            ifsc_code (String): The code to be searched.
        
        Returns:
            results: a list contains the ifsc bank data.
        '''
        try:
            # ifsc url hit counts updated. 
            update_ifsc_search_api_count()

            # query params & validations.
            ifsc_code = request.GET.get('ifsc_code')
            if not isValidIFSCode(ifsc_code): return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, "message": 'invalid|required ifsc_code!'})

            cached_ifsc_result = check_in_cache(ifsc_code)
            if cached_ifsc_result:
                # ifsc_code hit counts created|updated.
                manage_ifsc_hit_count(ifsc_code)
                return Response({'status': status.HTTP_200_OK, 'success': True, "message": 'Found! ifsc search data.', "results": cached_ifsc_result}, )
            else:
                # get the response from the backend server URL
                src = urllib.request.urlopen(ifsc_search_url(ifsc_code)).read()
                src = src.decode('utf8').replace("'", '"')
                data = json.loads(src)
                if not data.get('success'): return Response({"status": status.HTTP_404_NOT_FOUND, 'success': False, "message": data.get('message')})
                # caching the response
                caching_result = caching_response(ifsc_code, data)
                if caching_result:
                    # ifsc_code hit counts created|updated.
                    manage_ifsc_hit_count(ifsc_code)
                    return Response({"status": status.HTTP_200_OK, 'success': True, "message": 'Found! ifsc search data.', "results": data.get('data')})
                else:
                    return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})
        except Exception as err:
            # print("Error > ", err)
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})


class Leaderboard(APIView):
    def get(self, request):
        '''
        The function for bank leaderboard data in ASC|DESC order with fetchcount.
        
        Parameters:
            sortorder (String): the sorting order ASC|DESC.
            fetchcount (String): the counts to be fetched.
        
        Returns:
            results: a list contains the banks leaderboard data.
        '''
        try: 
            # leaderboard url hit counts updated. 
            update_leaderboard_api_count()

            # query params & validations.
            sortorder = request.GET.get('sortorder')
            fetchcount = request.GET.get('fetchcount')
            if not sortorder: sortorder = 'DESC'
            if not fetchcount: fetchcount = 10
            if not isValidSortOrder(sortorder): return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, "message": 'Invalid sort order, ASC|DESC required!'}) 
            if not isValidCount(fetchcount): return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, "message": 'Invalid fetch count!'})
            
            # get the response from the backend server URL.
            src = urllib.request.urlopen(leaderboard_url(sortorder, fetchcount)).read()
            src = src.decode('utf8').replace("'", '"')
            data = json.loads(src)
            if not data.get('success'): return Response({"status": status.HTTP_404_NOT_FOUND, 'success': False, "message": data.get('message')})
            return Response({"status": status.HTTP_200_OK, 'success': True, "message": 'Found! bank leaderboard data.', "results": data.get('data')})
        except Exception as err:
            # print("Error > ", err)
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})


class Statistics(APIView):
    def get(self, request):
        '''
        The function to retrieve searched ifsc code with timestamp data.
        
        Parameters:
            sortorder (String): the sorting order ASC|DESC.
            fetchcount (String): the counts to be fetched.
        
        Returns:
            results: a list contains the ifsc leaderboard data.
        '''
        try: 
            # statistics url hit counts updated. 
            update_statistics_api_count()

            # query params & validations.
            sortorder = request.GET.get('sortorder')
            fetchcount = request.GET.get('fetchcount')

            if not sortorder: sortorder = 'ASC'
            if not fetchcount: fetchcount = 'ALL'
            if not isValidSortOrder(sortorder): return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, "message": 'Invalid sort order, ASC|DESC required!'})
            if not isValidCount(fetchcount): return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, "message": 'Invalid fetch count!'})  
            
            # get the response from the URL
            src = urllib.request.urlopen(statistics_url(sortorder, fetchcount)).read()
            src = src.decode('utf8').replace("'", '"')
            data = json.loads(src)
            if not data.get('success'): return Response({"status": status.HTTP_404_NOT_FOUND, 'success': False, "message": data.get('message')})
            return Response({"status": status.HTTP_200_OK, 'success': True, "message": 'Found! bank statistics data.', "results": data.get('data')})
        except Exception as err:
            # print("Error > ", err)
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})

        
class IFSCHits(APIView):
    def get(self, request):
        '''
        The function to retrieve per ifsc_code hit counts.

        Returns:
            results: a dict contains the ifsc_code hit data.
        '''
        try:
            return Response({"status": status.HTTP_200_OK, 'success': True, "message": 'Ifsc hit counts results.', "results": ifsc_hit_count})
        except Exception as err:
            # print("Error > ", err)
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})


class URLSHits(APIView):
    def get(self, request):
        '''
        The function to retrieve per urls hit counts.

        Returns:
            results: a dict contains the urls hits data.
        '''
        try:
            return Response({"status": status.HTTP_200_OK, 'success': True, "message": 'url hit counts results.', "results": URL_hit_count})
        except Exception as err:
            # print("Error > ", err)
            return Response({"status": status.HTTP_500_INTERNAL_SERVER_ERROR, 'success': False, "message": 'Something went wrong!'})