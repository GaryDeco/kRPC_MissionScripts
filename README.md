# My kRPC Mission Scripts for Kerbal Space Program

* Status: In Development

A collection of scripts and tools that I use to run simulations in Kerbal Space Program using krpc. I hope these are useful as a reference. I am slowly refining my old code and adding it to this repository. I have a lot but I don't like to share sloppy code. Feel free to use as you wish or let me know if I screwed up somewhere. 

For more info on krpc... [add link]

### Structure ###

A little disorganized at this point. 

* Drone_PID folder is to contain a custom PID controller for a simple atmospheric drone demo (incomplete)
* Jupyter folder contains some of my old scripts for calling streams and other experiments to get familiar with the Space Center api. Written using jupyter notebooks. 
* Tests folder is simply a location for tests and error handling
* Tools folder contains a few tools and helpers to simplify script development. The following are few already added...
  * DV_map class which can return the minimum required DV to any stock body from Kerbin to help  with rocket design. 
  * Conversions for universal or met time. 
  * Vessel info methods like part list calls, engine data, etc... (In development)

### Plans ###

* Add build diagram / PID for atmospheric drone. 
* Complete full lauch demo with reusable booster. 
* Incorporate a simplified mission planning script and flight checks for failure mitigation. 
* Full flight simulation with visualization and data output for desired destination that is reasonably accurate. 


