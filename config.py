class Config(object):
    def __init__(self, uri, fac_id, apikey, mongo_uri, seconds):
        self._uri = uri
        self._facility_id = fac_id
        self._apikey = apikey
        self._mongo_uri = mongo_uri
        self._update_sec = seconds
        
    @property
    def uri(self):
        return self._uri
    
    @uri.setter
    def uri(self, value):
        self._uri = value
    
    @property
    def fac_id(self):
        return self._facility_id
    
    @fac_id.setter
    def fac_id(self, value):
        self._facility_id = value
    
    @property
    def apikey(self):
        return self._apikey
    
    @apikey.setter
    def apikey(self, value):
        self._apikey = value
        
    @property
    def mongo_uri(self):
        return self._mongo_uri
    
    @mongo_uri.setter
    def mongo_uri(self, value):
        self._mongo_uri = value

    @property 
    def seconds(self):
        return self._update_sec
    
    @seconds.setter
    def seconds(self, value):
        self._update_sec = value

    def __str__(self):
        return f"{self.uri}, {self._facility_id}, {self.apikey}, {self.mongo_uri}"
    