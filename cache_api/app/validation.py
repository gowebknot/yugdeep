import re

# ifsc code validation.
def isValidIFSCode(ifsc_code):
    regex = "^[A-Z]{4}0[A-Z0-9]{6}$"    
    cmpl = re.compile(regex)

    if (ifsc_code == None): return False
    
    response = True if(re.search(cmpl, ifsc_code)) else False
    return response

# sort order validation.
def isValidSortOrder(order):
    response = True if order in ['ASC', 'DESC'] else False
    return response

# fetch count validation.
def isValidCount(count):
    if count == 'ALL':
        return True

    response = True if count != 0 and count.isnumeric() else False
    return response


# from django.test import TestCase
# from rest_framework import status
# from rest_framework.test import APITestCase

# # Create your tests here.

# class TestAPIMethods(APITestCase):
#     def test_ifsc_search(self):
#         response = self.client.get('/ifsc-search/?ifsc_code=ABHY0065004', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_bank_leaderboard(self):
#         response = self.client.get('/leaderboard/?sortorder=DESC&fetchcount=225', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_statistics(self):
#         response = self.client.get('/statistics/?sortorder=DESC&fetchcount=1', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_ifsc_hits(self):
#         response = self.client.get('/ifsc-hits/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_url_hits(self):
#         response = self.client.get('/url-hits/', format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)






