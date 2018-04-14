# FNBR API
A python type API module for [FNBR.co](https://fnbr.co/api).
[Documentation](https://github.com/Douile/fnbr-api/wiki)
# Installing
Installing is simple using PyPi.
```python
pip install fnbr-api
```
You can then import using
```python
import fnbr
```

# Examples
***All for python 3.5***
### Retreive today's shop
```python
import fnbr

apikey = 'YOUR_API_KEY'
request = fnbr.Shop(apikey)
response = request.send()
if response.status == 200 and response.type == fnbr.SHOP_TYPE:
  shop = response.data
  print('Shop for: {0}'.format(shop.date))
  print('Daily items:')
  for item in shop.daily:
    print('\t{0}: {1}'.format(item.name,item.price))
  print('Featured items:')
  for item in shop.featured:
    print('\t{0}: {1}'.format(item.name,item.price))
else:
  print('Error getting shop')
```
### Search for an image
```python
import fnbr

apikey = 'YOUR_API_KEY'
itemname = 'Rex' # the search is case sensitive
itemtype = 'outfit' # must be one of 'emote','glider','emoji','loading','outfit','pickaxe','skydive','umbrella' or 'misc'. not case sensitive
itemlimit = 1 # integer between 1 and 15
request = fnbr.Image(apikey,search=itemname,type=itemtype,limit=itemlimit)
response = request.send()
if response.status == 200 and response.type == fnbr.IMAGE_TYPE:
  print('Results:')
  imagedata = response.data
  for item in imagedata.results:
    print('{0}: {1}'.format(item.name,item.price))
else:
  print('Error searching images')
```
### Get statistics
```python
import fnbr

apikey = 'YOUR_API_KEY'
request = fnbr.Stat(apikey)
response = request.send()
if response.status == 200 and response.type == fnbr.STAT_TYPE:
  statdata = response.data
  print('Total cosmetics: {0}'.format(statdata.totalCosmetics))
else:
  print('Error getting stats')
```
# Links
* [pypi](https://pypi.org/project/fnbr-api/)
* [docs](https://github.com/Douile/fnbr-api/wiki)
