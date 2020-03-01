# WeGo Services Supply Frontend
[![Generic badge](https://img.shields.io/badge/version-1.0-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/build-stable-<COLOR>.svg)](https://shields.io/) 
[![Generic badge](https://img.shields.io/badge/code_style-SWETeam22-teal.svg)](https://github.com/komoto415/COSC3339/blob/master/Trying%20Markdown/StyleAndDirectoryGuide.md)

## Features

```
As the name may imply, small experiments for testing certain functionality and behaviour on the local
/experiments

This is where I've thrown both my API design and the thought processes I had going into the design process
/Notes and Design
    As the name may imply, really just chicken scratchings and notes
    /apiNotes.txt

    The actual design and documentation of the vehicle request API
    It contains some documentation of allowable parameters, example calls and some
    pseudocode for what I might expect to have to write in the actual implementation
    /vehiclesReqDesign.md

This was just a quick and dirty dispatch class I decided to make to help myself try and understand what Dispatch really was
and how it might manifest itself at an implementation level
This doesn't actually interact with anything yet
/dispatch.py

This is our vehicle request handler. It will be receiving an HTTPs string from our Demand Backend asking for a vehicle
as well as an order.json which we will parse to make a dispach to add to our dispatch record table.
We will then responde with vehicle data of the vehicle that has been selected as that order's courier (however we makde that desicion TO BE IMPLEMENTED)
/vehicle.py
```