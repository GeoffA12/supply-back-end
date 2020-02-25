Supply Backend ReadMe

Functionality and Connections: (Will have the same content in the /supply-front-end/readMe.txt, so can skip this part if you already read that)
User will open start at our login.html, after credential validation, they are redirected to our dashboard.html. 
Onload, our dashboard will make a GET request to our fleetHandler(not implemented as of this current update) to fetch 
fleet data and vehicles of said fleet(s) and load them into our table(s). 
From there the user will be able to see tables of their fleet(s) and a bulletin that will display
potentially urgent messages and quickfixes that may need their attention

1.  Login (input credentials)
2.  Credential validation (input is POSTed to login.py to check DB)
3a. Fail, (reprompt credentials)
3b. Pass, (redirected to dashboard.html)
4.  Dashboard (onload will make GET request for fleet manager's fleet info to populate tables and bulletin)

File Structure:
/experiments
    # As the name may imply, small experiments for testing certain functionality and behaviour on the local

/Notes and Design
    # This is where I've thrown both my API design and the thought processes I had going into the design process

    # As the name may imply, really just chicken scratchings and notes
    /apiNotes.txt

    # The actual design and documentation of the vehicle request API
    # It contains some documentation of allowable parameters, example calls and some
    # pseudocode for what I might expect to have to write in the actual implementation
    /vehiclesReqDesign.md

/dispatch.py
    # This was just a quick and dirty dispatch class I decided to make to help myself try and understand what Dispatch really was
    # and how it might manifest itself at an implementation level

/vehicle.py
    # This is our vehicle request handler. It will be receiving an HTTPs string from our Demand Backend asking for a vehicle
    # as well as an order.json which we will parse to make a dispach to add to our dispatch record table.
    # We will then responde with vehicle data of the vehicle that has been selected as that order's courier (however we makde that desicion TO BE IMPLEMENTED)
