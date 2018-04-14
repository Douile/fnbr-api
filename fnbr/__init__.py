import requests
from urllib.parse import quote_plus

# constants
BASEURL = "https://fnbr.co/api"
VALID_IMAGE_TYPES = ['emote','glider','emoji','loading','outfit','pickaxe','skydive','umbrella','misc']
VALID_IMAGE_LIMIT_MIN = 1
VALID_IMAGE_LIMIT_MAX = 15

NONE_TYPE = "none"
ERROR_TYPE = "error"
STAT_TYPE = "stats"
IMAGE_TYPE = "image"
SHOP_TYPE = "shop"
# requests
class APIRequest():
    """Parent class of all API Requests"""
    def __init__(self,key,endpoint,arguments={}):
        self.key = key
        self.endpoint = endpoint
        self.arguments = arguments
    def url(self):
        url = BASEURL + self.endpoint + self.parseArguments()
        return url
    def parseArguments(self):
        args = ""
        for a in self.arguments:
            args += uriencode(a) + "=" + uriencode(self.arguments[a]) + "&"
        if len(args) > 0:
            args = "?" + args
        return args
    def send(self):
        headers = {'x-api-key':self.key}
        self.response = APIResponse(requests.get(url=self.url(),headers=headers))
        return self.response
class Images(APIRequest):
    """Images API Request"""
    def __init__(self,key,search=None,type=None,limit=None):
        super().__init__(key,"/images",{})
        self.setSearch(search)
        self.setType(type)
        self.setLimit(limit)
    def setSearch(self,search=""):
        set = False
        if type(search) is str:
            self.arguments['search'] = search
            set = True
        return set
    def setType(self,itype=""):
        set = False
        if type(itype) is str:
            itype = itype.lower()
            if type in VALID_IMAGE_TYPES:
                self.arguments['type'] = itype
                set = True
        return set
    def setLimit(self,limit=1):
        set = False
        if type(limit) is int:
            self.arguments['limit'] = bounds(limit,VALID_IMAGE_LIMIT_MIN,VALID_IMAGE_LIMIT_MAX)
            set = True
        return set
class Shop(APIRequest):
    """"Shop API Request"""
    def __init__(self,key):
        super().__init__(key,"/shop",{})
class Stat(APIRequest):
    """Stat API Request"""
    def __init__(self,key):
        super().__init__(key,"/stats",{})
# responses
class APIResponse():
    """API Response (formated requests.response)"""
    def __init__(self,response):
        self.headers = response.headers
        try:
            self.json = response.json()
        except ValueError:
            self.json = {}
        try:
            self.status = self.json['status']
        except KeyError:
            self.status = response.status_code
        if self.status != 200:
            self.type = ERROR_TYPE
            try:
                self.error = self.json['error']
            except KeyError:
                self.error = response.reason
        elif 'data' in self.json:
            if type(self.json['data']) is list:
                self.type = IMAGE_TYPE
                self.data = ImageResponse(self.json)
            elif type(self.json['data']) is dict:
                self.type = SHOP_TYPE
                self.data = ShopResponse(self.json)
            else:
                self.type = NONE_TYPE
        elif 'totalCosmetics' in self.json and 'matrix' in self.json:
            self.type = STAT_TYPE
            self.data = StatResponse(self.json)
        else:
            self.type = NONE_TYPE
class ShopResponse():
    def __init__(self,json={}):
        self.featured = []
        for i in range(0,len(json['data']['featured'])):
            self.featured.append(Item(json['data']['featured'][i]))
        self.daily = []
        for i in range(0,len(json['data']['daily'])):
            self.daily.append(Item(json['data']['daily'][i]))
        self.date = json['data']['date']
class StatResponse():
    def __init__(self,json={}):
        self.totalCosmetics = json['totalCosmetics']
        self.matrix = []
        if 'matrix' in json:
            for i in range(0,len(json['matrix'])):
                self.matrix.append(StatItem(json['matrix'][i]))
class ImageResponse():
    def __init__(self,json={}):
        self.results = []
        for i in range(0,len(json['data'])):
            self.results.append(Item(json['data'][i]))

class Item():
    """A fortnite shop item"""
    def __init__(self,json={}):
        self.id = self.load('id',json)
        self.name = self.load('name',json)
        self.price = self.load('price',json)
        self.priceIcon = self.load('priceIcon',json)
        self.priceIconLink = self.load('priceIconLink',json)
        self.rarity = self.load('rarity',json)
        self.type = self.load('type',json)
        self.readableType = self.load('readableType',json)
        if 'images' in json:
            self.icon = self.load('icon',json['images'])
            self.png = self.load('png',json['images'])
            self.gallery = self.load('gallery',json['images'])
            self.featured = self.load('featured',json['images'],False)
    def load(self,name,json,default=""):
        if name in json:
            value =  json[name]
        else:
            value = default
        return value
class StatItem():
    """A fnbr category stat item"""
    def __init__(self,json={}):
        self.type = self.load('type',json)
        self.rarity = []
        if 'rarity' in json:
            for i in range(0,len(json['rarity'])):
                self.rarity.append(StatRarity(json['rarity'][i]))
    def load(self,name,json,default=""):
        if name in json:
            value =  json[name]
        else:
            value = default
        return value
class StatRarity():
    def __init__(self,json={}):
        self.rarity = json['rarity']
        self.count = json['count']

# functions
def bounds(value,min,max):
    if value < min:
        value = min
    elif value > max:
        value = max
    return value
def uriencode(string):
    if type(string) is int:
        string = str(string)
    return quote_plus(bytes(string,"utf-8"))
