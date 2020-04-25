# WeGo Services Supply Backend #
[![Generic badge](https://img.shields.io/badge/version-1.1.0-<COLOR>.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/build-unstable-red.svg)](https://shields.io/) 
[![Generic badge](https://img.shields.io/badge/code_style-SWETeam22-teal.svg)](https://github.com/komoto415/COSC3339/blob/master/Trying%20Markdown/StyleAndDirectoryGuide.md)

## What to Expect ##
This repository will compose of mostly unique backend components to our supply side clients. This such as our vehicl
and vehicle request APIs, fleet monitoring and fleet manager interactions
 
## Feature Set ##
For our customer, our web service will enable us to communicate to them information about the courier of their order(s)
and be able to receive live updates about the status for an order in-progress. 

For our fleet managers, it means a way that they'll be able to interact with the both their fleets and vehicles through
a single web service where they can push and receive updates to their fleets and vehicles.  

#### Below is a table of our functionality and intended future features ####
|Functionality                  |Status     
|:---                           |:---
|Receives order from demandBE   |Functional
|HTTPS response                 |Functional
|Returns vehicle data           |Functional
|Creating dispatch              |Functional?
|Interaction with vehicle table |Queued
|Update dispatch record         |Queued
|