import django
from copy import deepcopy, copy

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ] 


class GeoJsonContext():


    def __init__(self):
        '''
        Passes a model object (by default a Django one) for conversion to GeoJSON
        '''
        self.feature_dict = {
                            "type": "Feature",
                            "properties": {
                                "name": None,
                                "pk": None,
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": None # [Long, Lat]
                            }
                            }

        self.data = {
                        "type": "FeatureCollection",
                        "crs": {
                            "type": "name",
                            "properties": {
                                "name": "EPSG:4326"
                            }
                        },
                        "features": None #feature_dict
                    }


    def _to_GeoJsonDict(self):

        pk = 1
        feat_list = []
        feat_dict = deepcopy(self.feature_dict)

        for q in self.qs:
            
            if q.feature is not None:
                # print(q.feature)
                
                ''' modify to make more general eventually '''
                feat_dict['properties']['name'] = q.feature # +' \ud83c\uddee\ud83c\uddf9'
                feat_dict['properties']['pk'] = str(pk)
                feat_dict['geometry']['coordinates'] = [q.longitude_rounded, q.latitude_rounded]

                feat_list.append(deepcopy(feat_dict))

                feat_dict = deepcopy(self.feature_dict)
                pk = pk + 1

        self.feat_list = feat_list 
        return self.feat_list 

    def to_GeoJsonDict(self, qs):

        if type(qs) == django.db.models.query.QuerySet: 
            self.qs = qs
        else: 
            print('warning, no queryset passed; no qs set')
            self.qs = None

        self.data['features'] = self._to_GeoJsonDict()

        return self.data


    