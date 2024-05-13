# Watch and Warning (WWA) ArcGIS Toolbox v.1.0

This repository contains code and documentation for an ArcGIS Python Toolbox, __WWA Tools v.1.0__, with a single tool:  __Associate Watches/Warnings with Ports__. It was developed in ArcGIS v.10.5.1 and written in Python v.2.7.   ArcGIS desktop software is required to use the toolbox.  Users without Git can download a ZIP file of the folder containing the toolbox, tool, and associated scripts and xml files.  

The toolbox was developed to support [Dr. Lisa Pfeiffer](https://www.fisheries.noaa.gov/contact/lisa-pfeiffer-phd)’s research into commercial fishing behavior as related to hazardous weather.  Specifically, the tool was used to associate historic National Weather Service (NWS) Watches and Warnings (WWA) spatial data with coastal port locations based on proximity.   This project was a follow-up to the study described in [Pfeiffer and Gratz, 2016](https://doi.org/10.1073/pnas.1509456113), but with the goal of using historical coastal forecast data (watches and warnings) instead of wind speed to understand and predict fishing behavior.

The project used historic National Weather Service (NWS) Watch and Warning polygons downloaded from Iowa State University’s Environmental Mesonet (IEM) [Archived NWS Watch/Warning page](https://mesonet.agron.iastate.edu/request/gis/watchwarn.phtml). 

The __Associate Watches/Warnings with Ports__ tool takes three inputs:
* one or more NWS WWA polygon feature classes 
* a feature class of port locations
* a user-specified maximum (straight line) distance for associating the WWA events with each port location

The output of the tool is:
* a comma-delimited text file (csv) of the ports with all associated WWA events based on the user-specified distance.  All attributes from the input feature classes are retained in this output file.

The output file from the tool can then be used as input for modeling and analysis of the potential impact of these weather and storm events on fishing behavior.   The benefit of the csv output format is that the data can be used in other statistics, modeling, and analysis environments.

This tool could also be used for any application where the user wants to associate two sets of spatial features based on a user-specified distance and output the resulting records to a csv file.

More specific details about the tool usage and guidance for data preparation, (especially related to use of the historic WWA data from IEM), can be found in the documentation included with the toolbox.
