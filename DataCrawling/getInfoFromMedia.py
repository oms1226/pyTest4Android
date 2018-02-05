from PIL import Image
from PIL.ExifTags import TAGS
import pyexiv2
import imghdr
import sys

class IMAGE:
    def __init__(self, filename):
        self.filename = filename

    def getLocation(self):
        isJPG = False
        Lon = None
        Lat = None
        Ctime = None
        CreatedFileName = None
        imageDescription = None
        extension = self.filename.split('.')[-1]
        if (extension == 'jpg') | (extension == 'JPG') | (extension == 'jpeg') | (extension == 'JPEG'):
            try:
                if imghdr.what(self.filename) == 'jpeg':
                    isJPG = True
                img = Image.open(self.filename)
                info = img._getexif()

                exif = {}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    #print decoded
                    exif[decoded] = value
                # from the exif data, extract gps
                exifGPS = exif['GPSInfo']
                #Ctime = info[0x9003]
                Ctime =  exif['DateTime']
                latData = exifGPS[2]
                lonData = exifGPS[4]
                # calculae the lat / long
                latDeg = latData[0][0] / float(latData[0][1])
                latMin = latData[1][0] / float(latData[1][1])
                latSec = latData[2][0] / float(latData[2][1])
                lonDeg = lonData[0][0] / float(lonData[0][1])
                lonMin = lonData[1][0] / float(lonData[1][1])
                lonSec = lonData[2][0] / float(lonData[2][1])
                # correct the lat/lon based on N/E/W/S
                Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
                if exifGPS[1] == 'S': Lat = Lat * -1
                Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
                if exifGPS[3] == 'W': Lon = Lon * -1
                # print file
                msg = "There is GPS info in this picture located at " + str(Lat) + "," + str(Lon)
                print msg
                CreatedFileName = Ctime[0:4]+"-"+ Ctime[5:7]+"-"+Ctime[8:10]+"-"+Ctime[11:13]+"-"+Ctime[14:16]+"-"+Ctime[17:19] + "_" + str(Lat) + "-" + str(Lon)
                kmlheader = '<?xml version="1.0" encoding="UTF-8"?>' + '<kml xmlns="http://www.opengis.net/kml/2.2">'
                kml = ('<Placemark><name>%s</name><Point><coordinates>%6f,%6f</coordinates></Point></Placemark></kml>') % (CreatedFileName, Lon, Lat)
                with open(self.filename + '.kml', "w") as f:
                    f.write(kmlheader + kml)
                print 'kml file created'
                imageDescription = exif['ImageDescription']
                print 'imageDescription:%s' % imageDescription

            except:
                print "Unexpected error:", sys.exc_info()[0]
                print "Unexpected error:", sys.exc_info()[1]
                print "Unexpected error:", sys.exc_info()[2]
                print 'There is no GPS info in this picture'
                pass

        return isJPG, Ctime, Lat, Lon, imageDescription, CreatedFileName

    def to_deg(self, value, loc):
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg = int(abs_value)
        t1 = (abs_value - deg) * 60
        min = int(t1)
        sec = round((t1 - min) * 60, 5)
        return (deg, min, sec, loc_value)
    
    def set_gps_location(self, lat = None, lng = None, imageDescription = None, Ctime = None):
        """Adds GPS position as EXIF metadata

        Keyword arguments:
        file_name -- image file
        lat -- latitude (as float)
        lng -- longitude (as float)

        """
        if lat != None or lng != None or imageDescription != None or Ctime != None:
            metadata = pyexiv2.ImageMetadata(self.filename)
            metadata.read()

        if lat != None and lng != None :
            lat_deg = self.to_deg(lat, ["S", "N"])
            lng_deg = self.to_deg(lng, ["W", "E"])

            print lat_deg
            print lng_deg

            # convert decimal coordinates into degrees, munutes and seconds
            exiv_lat = (pyexiv2.Rational(lat_deg[0] * 60 + lat_deg[1], 60), pyexiv2.Rational(lat_deg[2] * 100, 6000),
                        pyexiv2.Rational(0, 1))
            exiv_lng = (pyexiv2.Rational(lng_deg[0] * 60 + lng_deg[1], 60), pyexiv2.Rational(lng_deg[2] * 100, 6000),
                        pyexiv2.Rational(0, 1))

            ##    exif_keys = metadata.exif_keys

            metadata["Exif.GPSInfo.GPSLatitude"] = exiv_lat
            metadata["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
            metadata["Exif.GPSInfo.GPSLongitude"] = exiv_lng
            metadata["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
            metadata["Exif.Image.GPSTag"] = 654
            metadata["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
            metadata["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'

        if imageDescription != None :
            metadata['Exif.Image.ImageDescription'] = imageDescription
            #metadata.setdefault('Exif.Image.ImageDescription', 'made by oms1226')

        if Ctime != None :
            metadata['Exif.Image.DateTime'] = Ctime

        metadata.write()

if __name__ == '__main__':
    tagetImg = IMAGE("testImg.jpg")
    tagetImg.set_gps_location(18.0001, 18.0002, 'good job!')
    isJPG, Ctime, Lat, Lon, imageDescription, CreatedFileName = tagetImg.getLocation()