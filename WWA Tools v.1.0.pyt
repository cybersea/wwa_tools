import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "WWA Tools v.1.0"
        self.alias = "wwaTools10"
        self.description = "The WWA Toolbox contains tools for processing " \
                           "archived National Weather Service Watch and Warning data "

        # List of tool classes associated with this toolbox
        self.tools = [WwaToPorts]


class WwaToPorts(object):
    def __init__(self):
        """Tool to perform spatial join between port locations and
            specified years of NWW Watch/Warning data
        """
        self.label = "Associate Watches/Warnings with Ports"
        self.description = "This tool will perform a spatial join between Port locations" \
                           " and National Weather Service Watch and Warning (wwa) polygons" \
                           " given a specified maximum distance of the event from each port." \
                           " Output is a csv file of the ports and the associated weather events."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Input parameter 1:  List of wwa data to associate with port locations
        wwa_fcs = arcpy.Parameter(
            displayName="Watch/Warning Feature Class(es)",
            name="wwa_fcs",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )
        # Input parameter 2: Feature class of port locations
        port_fc = arcpy.Parameter(
            displayName="Port Locations Feature Class",
            name="port_fc",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )
        # Input parameter 3:  Maximum distance for association of watch/warn with port location
        dist_unit = arcpy.Parameter(
            displayName="Maximum Distance from Port to Associate Watches/Warnings",
            name="dist_unit",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )
        # Output parameter 4: Output csv file
        out_file = arcpy.Parameter(
            displayName="Output csv File",
            name="out_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Output"
        )
        out_file.filter.list = ['csv']

        params = [wwa_fcs, port_fc, dist_unit, out_file]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        import port_wwa_join

        # Input parameter 1:  List of wwa data to associate with port locations
        wwa_fcs = parameters[0].valueAsText  #

        # Input parameter 2: Feature class of port locations
        port_fc = parameters[1].valueAsText

        # Output parameter 3:  Maximum distance for association of watch/warn with port location
        dist_unit = parameters[2].valueAsText

        # Input parameter 4: Output csv files
        out_file = parameters[3].valueAsText

        port_wwa_join.main(wwa_fcs, port_fc, dist_unit, out_file)

        return
