# retuns flask backend ifsc search url.
def ifsc_search_url(ifsc_code):
    return 'http://127.0.0.1:5000/ifsc-search?ifsc_code='+str(ifsc_code)

# retuns flask backend leaderboard url.
def leaderboard_url(sortorder, fetchcount):
    return 'http://127.0.0.1:5000/leaderboard?sortorder='+str(sortorder)+'&fetchcount='+str(fetchcount)

# retuns flask backend statistics url.
def statistics_url(sortorder, fetchcount):
    return 'http://127.0.0.1:5000/statistics?sortorder='+str(sortorder)+'&fetchcount='+str(fetchcount)