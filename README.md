# FNBR API
A python type API module for [FNBR.co](https://fnbr.co/api).

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
## Retreive today's shop
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

# Links
* [pypi](https://pypi.org/project/fnbr-api/)
* [docs](https://github.com/Douile/fnbr-api/wiki)
