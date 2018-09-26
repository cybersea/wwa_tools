__author__ = 'Allison Bailey, Sound GIS'

"""
port_wwa_join.py
8/15/2018
Script to join IEM watch/warn features to Port point locations
This assumes that watch/warning data have already been subset to the phenomenon of interest
"""

# Imports
import arcpy
import csv

arcpy.env.overwriteOutput = True

units2field = {
    'Centimeters':'dist_cm',
    'Decimal degrees':'dist_dd',
    'Decimeters':'dist_dm',
    'Feet':'dist_ft',
    'Inches':'dist_in',
    'Kilometers':'dist_km',
    'Meters':'dist_m',
    'Miles':'dist_mi',
    'Millimeters':'dist_mm',
    'Nautical Miles':'dist_nm',
    'Points':'dist_pts',
    'Unknown':'dist_unk',
    'Yards':'dist_yd',
}

def calc_doublefield(dataset, field, value):
    """ Add a Double type field and calculate value

    :param dataset: The dataset to add and calc field
    :param field: The field name of the new field
    :param value: the value to calculate (must be numeric)
    :return:
    """
    if not fieldExists(dataset, field):
        arcpy.AddField_management(dataset, field, "Double")
    arcpy.CalculateField_management(dataset, field, value)

def del_field(dataset, field):
    """  Delete a field if it exists

    :param dataset: dataset to delete field
    :param field: name of the field to detel
    :return:
    """
    if fieldExists(dataset, field):
        arcpy.DeleteField_management(dataset, field)

def fieldExists(dataset, field_name):
    """ Check if a field exists in specified data set

    :param dataset: dataset to check
    :param field_name:  name of the field to check
    :return:  boolean True if it exists
    """
    if field_name in [field.name for field in arcpy.ListFields(dataset)]:
        return True

def del_fc(fc):
    """  Delete a feature class if it exists

    :param fc: feature class to delete
    :return:
    """
    if arcpy.Exists(fc):
        arcpy.Delete_management(fc)

def msg(text):
    """ General message accumulator"""
    arcpy.AddMessage(text)

def tableToCSV(table, csv_filepath):
    """ Export table to a csv file

    :param table: input table
    :param csv_filepath:  output csv file
    :return:
    """
    msg("Exporting to csv file: {0}".format(csv_filepath))
    fields = arcpy.ListFields(table)
    fld_names = [fld.name for fld in fields if fld.name not in ["Shape", "JOIN_FID"]]
    with open(csv_filepath, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(fld_names)
        with arcpy.da.SearchCursor(table, fld_names) as cursor:
            for row in cursor:
                writer.writerow(row)
        print(csv_filepath + " CREATED")
    csv_file.close()

def main(wwa_fcs, port_fc, dist_unit, out_file):
    """ Perform spatial join of Watch/Warning polygons to port locations
    Append multiple joined feature classes and output to final csv file

    :param wwa_fcs: string of Watch/Warning feature class paths (; is separator)
    :param port_fc: path to Port feature class
    :param dist_unit: string with distance and unit (space is separator)
    :param out_file: output csv file
    :return:
    """

    dist, unit = dist_unit.split(' ')
    dist_field = units2field[unit]
    fields2delete = ["Join_Count","TARGET_FID"]

    for i, wwa_fc in enumerate(wwa_fcs.split(';')):
        # Feature class names (without path)
        wwa_fc_nm = arcpy.Describe(wwa_fc).name
        port_fc_nm = arcpy.Describe(port_fc).name
        # Output temporary joined feature class in-memory path
        out_fc = "in_memory/{0}_{1}".format(port_fc_nm, wwa_fc_nm)
        msg("Joining {0} to {1}".format(wwa_fc_nm, port_fc_nm))
        # Spatial Join ports with watch/warning data
        arcpy.SpatialJoin_analysis(port_fc, wwa_fc, out_fc, "JOIN_ONE_TO_MANY", "KEEP_COMMON", "#",
                                   "WITHIN_A_DISTANCE", dist_unit)
        # Delete extraneous fields
        for field in fields2delete:
            del_field(out_fc, field)
        # Add depth field and calc value
        calc_doublefield(out_fc, dist_field, dist)

        # IF there is more than one output feature class, append them together
        if i == 0:
            final_fc = out_fc # use first feature class as final one to append others to
        elif i > 0:
            # msg("Appending {0} to {1}".format(out_fc, final_fc))
            arcpy.Append_management(out_fc, final_fc, "NO_TEST", "", "")
            del_fc(out_fc)

    # output final feature class to csv file
    tableToCSV(final_fc, out_file)

    # clean up
    del_fc(final_fc)


if __name__ == "__main__":

    # For testing or command line use -- replace values with path to your local data
    wwa_fcs = 'Y:/projects/nmfs_econ2017/data/NWS_WatchWarn/nws_wwa_2001_2017.gdb/wwa_subset_2011_lcc;' \
              'Y:/projects/nmfs_econ2017/data/NWS_WatchWarn/nws_wwa_2001_2017.gdb/wwa_subset_2012_lcc'
    port_fc = 'Y:/projects/nmfs_econ2017/data/NWS_WatchWarn/nws_wwa_2001_2017.gdb/NE_scallop_ports_lcc'
    dist_unit = '10 Kilometers'
    out_file = 'Y:/projects/nmfs_econ2017/data/NWS_WatchWarn/output/test_out.csv'

    main(wwa_fcs, port_fc, dist_unit, out_file)

