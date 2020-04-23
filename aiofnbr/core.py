import aiohttp
import asyncio
from . import constants, utils

# requests
class APIRequest():
    """Parent class of all API Requests"""
    def __init__(self,key,endpoint,arguments={}):
        self.key = key
        self.endpoint = endpoint
        self.arguments = arguments
    @asyncio.coroutine
    def url(self):
        args = yield from self.parseArguments()
        url = constants.BASEURL + self.endpoint + args
        return url
    @asyncio.coroutine
    def parseArguments(self):
        args = ""
        for a in self.arguments:
            args += uriencode(a) + "=" + uriencode(self.arguments[a]) + "&"
        if len(args) > 0:
            args = "?" + args
        return args
    @asyncio.coroutine
    def send(self):
        headers = {'x-api-key':self.key}
        session = aiohttp.ClientSession(headers=headers)
        url = yield from self.url()
        response = yield from session.get(url)
        json = yield from response.json()
        yield from session.close()
        self.response = APIResponse(response,json)
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
            if type in constants.VALID_IMAGE_TYPES:
                self.arguments['type'] = itype
                set = True
        elif itype == None:
            self.arguments.pop('type',None)
            set = True
        return set
    def setLimit(self,limit=1):
        set = False
        if type(limit) is int:
            self.arguments['limit'] = utils.bounds(limit,constants.VALID_IMAGE_LIMIT_MIN,constants.VALID_IMAGE_LIMIT_MAX)
            set = True
        elif limit == None:
            self.arguments.pop('limit',None)
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
    def __init__(self,response,json):
        self.headers = response.headers
        self.json = json
        try:
            self.status = self.json['status']
        except KeyError:
            self.status = response.status
        if self.status != 200:
            self.type = constants.ERROR_TYPE
            try:
                self.error = self.json['error']
            except KeyError:
                self.error = response.reason
        elif 'data' in self.json:
            if type(self.json['data']) is list:
                self.type = constants.IMAGE_TYPE
                self.data = ImageResponse(self.json)
            elif type(self.json['data']) is dict:
                self.type = constants.SHOP_TYPE
                self.data = ShopResponse(self.json)
            else:
                self.type = constants.NONE_TYPE
        elif 'totalCosmetics' in self.json and 'matrix' in self.json:
            self.type = constants.STATS_TYPE
            self.data = StatResponse(self.json)
        else:
            self.type = constants.NONE_TYPE

class ShopResponse():
    def __init__(self,json={}):
        self.featured = []
        for i in range(0,len(json['data']['featured'])):
            self.featured.append(Item(json['data']['featured'][i]))
        self.daily = []
        for i in range(0,len(json['data']['daily'])):
            self.daily.append(Item(json['data']['daily'][i]))
        self.date = json.get('date',None)

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
        self.id = json.get('id',None)
        self.name = json.get('name',None)
        self.price = json.get('price',None)
        self.priceIcon = json.get('priceIcon',None)
        self.priceIconLink = json.get('priceIconLink',None)
        self.rarity = json.get('rarity',None)
        self.type = json.get('type',None)
        self.readableType = json.get('readableType',None)
        images = json.get('images',None)
        if images != None:
            self.icon = images.get('icon',None)
            self.png = images.get('png',None)
            self.gallery = images.get('gallery',None)
            self.featured = images.get('featured',None)

class StatItem():
    """A fnbr category stat item"""
    def __init__(self,json={}):
        self.type = json.get('type',None)
        self.rarity = []
        rarity = json.get('rarity',None)
        if rarity != None:
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
