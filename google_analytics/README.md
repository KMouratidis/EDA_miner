## Google Analytics REST API

This mini-server exists to handle the connection to Google with the `googleanalytics`
library. Since it only works with `oauth2client==1.5.2` it is incompatible with
`gspread` (used on the main app; needs `oauth2client>=3`).

#### To build & run with docker:
    sudo docker build --rm -t kmouratidis/ganalytics .
    sudo docker run --rm --network host kmouratidis/ganalytics
    
#### Example usage for Python:

    >>> import requests, json

    # Send your credentials to the server
    >>> response = requests.post("http://127.0.0.1:5000/", json={
            "client_email": data["client_email"],
            "user_id": "kostas",
            "private_key": data["private_key"]
        })

    # Make a request for one or more pageviews
    >>> response = requests.get("http://127.0.0.1:5000/kostas/pageviews,sessions")

    # To read the response, use json to decode the results
    >>> results = json.loads(response.text)
    
    >>> print(results)
    {  
        'data':{  
            'pageviews':[  
                4
            ],
            'sessions':[  
                4
            ]
        },
        'metrics':[  
            'ga:pageviews',
            'ga:sessions'
        ],
        'success':'true'
    }

