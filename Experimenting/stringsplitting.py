str = "https://supply.team22.softwareengineeringii.com/getDispatch/?vid=123&test=queued&tess=queued&tesa=queued"
# str = "https://supply.team22.softwareengineeringii.com/getDispatch/?vid=123"

str = str.split('/')[-1].strip('?')
print(str)
# vid = str.split('=')[1]
# print(vid)

# assert(vid == '123')

arr = str.split('&')
print(arr)
arr1 = [x.split('=')[0] for x in arr]
arr2 = [x.split('=')[1] for x in arr]
# arr3 = [x.split('=') for x in arr if x.split('=')[0] == 'vid']
print(arr1)
print(arr2)
# print(arr3)
# dict1 = dict(zip(arr1, arr2))
# print(dict1)
