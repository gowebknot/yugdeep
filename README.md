# BANK API

### There are two apps built:

* *Django* based
* *Flask* based

### Django API

The application where the rest-client will be calling API requests to flask microservice. 
The main functions of this layer is to :

1. Works as main interface layer.
2. Parameters validation.
3. Caching of the 'ifsc search' requests.
4. Intracting with the flask app.
5. Tracking the URL Hits & IFSC Hits.

### Flask API

The application where the datacfrom excel is processed and stored. 
The main functions of this layer is to :

1. It Works aa a microservice of the system.
2. Processes the stored data in memory.
1. Stores ifsc bank, bank leaderboard & bank statistics data.
1. Responds to the request send by django API as JSON.




#### We need to invoke the APIs from the REST Client (postman or CURL).

#### Use the provided POSTMAN collection for the django API.

## python version

    python 3.8.10

## Create virtual Environment

    python3 -m venv env
    
## Activate virtual Environment

    source env/bin/activate 
    
## Install dependencies from requirements.txt

    pip3 install -r requirements.txt 

## Change directory to cache_api directory, 
    
    cd cache_api(in terminal)

## To avoid migrations error
    
    python3 manage.py migrate    
    
## To run the unit tests in django cache_api
    
    python3 manage.py test app 

##  Run server in django cache_api

    python3 manage.py runserver
    

## Open new terminal


## Change directory to cache_api directory,

    cd backend_api(in terminal)

## To run unit test in backend_api directory , 
    
    python3 test.py

##  Run server in flask backend_api

    python3 main.py    
    
### Congrats, you are good to go. Both the servers are running and are ready to accept you API calls at:

    http://127.0.0.1:8000/api/ + 'add app urls'+'?query parameters as well'.
    
    


    
    
## Request Bank details for a given IFSC Code

### Request

`GET /ifsc-search`

    GET 'http://127.0.0.1:8000/api/ifsc-search?ifsc_code=ABHY0065004'
    
### query Params

    query parameter : ifsc_code (mandatory)

### Response

    {
        "status": 200,
        "success": true,
        "message": "Found! ifsc search data.",
        "results": {
            "BANK": "ABHYUDAYA COOPERATIVE BANK LIMITED",
            "IFSC": "ABHY0065004",
            "MICR_CODE": "400065004",
            "BRANCH": "BHANDUP",
            "ADDRESS": "CHETNA APARTMENTS, J.M.ROAD, BHANDUP, MUMBAI-400078",
            "STD_CODE": 22,
            "CONTACT": "25963157",
            "CITY": "GREATER MUMBAI",
            "DISTRICT": "MUMBAI",
            "STATE": "MAHARASHTRA"
        }
    }



## Request leaderboard

### Request

`GET leaderboard/`

    GET 'http://127.0.0.1:8000/leaderboard/'
    GET 'http://127.0.0.1:8000/leaderboard/?sortorder=ASC'
    GET 'http://127.0.0.1:8000/leaderboard/?fetchcount=6'
    GET 'http://127.0.0.1:8000/leaderboard/?sortorder=ASC&fetchcount=6'
    
### Params

    query parameter : {
        sortorder : ASC, // (optional) (valid values = ASC, DESC || Default = DESC)
        fetchcount : 6 // (optional) (valid value = 1 to 225 || Default = 10)     
    }    

### Response

    {
        "status": 200,
        "success": true,
        "message": "Found! bank leaderboard data.",
        "results": {
            "STATE BANK OF INDIA": 28500,
            "PUNJAB NATIONAL BANK": 12237,
            "CANARA BANK": 10817,
            "UNION BANK OF INDIA": 10178,
            "BANK OF BARODA": 9558,
            "HDFC BANK": 7012,
            "INDIAN BANK": 6089,
            "ICICI BANK LIMITED": 5693,
            "BANK OF INDIA": 5295,
            "AXIS BANK": 5242
        }
    }




## Request statistics

### Request

`GET statistics/`

    GET 'http://127.0.0.1:8000/api/statistics'
    GET 'http://127.0.0.1:8000/api/statistics?sortorder=DESC&fetchcount=1'
    GET 'http://127.0.0.1:8000/api/statistics?sortorder=ASC&fetchcount=5'
    
    
### Params

    query parameter : {
        sortorder : DESC, // (optional) (valid values = ASC, DESC || Default = ASC)
        fetchcount : 6 // (optional) (valid value = (1 to 10000) and all || Default = all)     
    }    

### Response

    {
        "status": 200,
        "success": true,
        "message": "Found! bank statistics data.",
        "results": [
            {
                "IFSC": "ABHY0065004",
                "TIMESTAMP": "20/10/2022, 17:15:06.797519"
            }
        ]
    }



## Request ifsc-hits

### Request

`GET /ifsc-hits`

    GET 'http://127.0.0.1:8000/ifsc-hits'
    
### Response

    {
        "status": 200,
        "success": true,
        "message": "Ifsc hit counts results.",
        "results": {
            "ABHY0065004": 1
        }
    }
    
    
    
## Request url-hits

### Request

`GET /url-hits`

    GET 'http://127.0.0.1:8000/api/url-hits'

### Response

    {
        "status": 200,
        "success": true,
        "message": "url hit counts results.",
        "results": {
            "IFSC_Search": 1,
            "Leaderboard": 1,
            "Statistics": 1
        }
    } 
        
# THANKS & REGARDS    
