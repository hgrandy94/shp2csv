import ogr,csv,sys

shpfile = sys.argv[1]
csvfile = sys.argv[2]

#Open files
csvfile = open(csvfile,'wb')
ds = ogr.Open(shpfile)
lyr = ds.GetLayer()

#Get field names
dfn = lyr.GetLayerDefn()
nfields = dfn.GetFieldCount()
fields = []
for i in range(nfields):
    fields.append(dfn.GetFieldDefn(i).GetName())
fields.append('kmlgeometry')
csvwriter = csv.DictWriter(csvfile, fields)
try:csvwriter.writeheader() #python 2.7+
except:csvfile.write(','.join(fields)+'\n')

# Write attributes and kml out to csv
for feat in lyr:
    attributes=feat.items()
    geom = feat.GetGeometryRef()
    attributes['kmlgeometry']=geom.ExportToKML()
    csvwriter.writerow(attributes)

#clean up
del csvwriter,lyr,ds
csvfile.close()
