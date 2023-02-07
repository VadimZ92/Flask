import requests


# response = requests.post('http://127.0.0.1:5000/advertising',
#                          json={'header': 'adv2', 'description': 'abc', 'user': 'user1'})


# response = requests.patch('http://127.0.0.1:5000/advertising/1',
#                           json={'header': 'adv23', 'description': 'abcabc'})
#
# print(response.status_code)
# print(response.json())

response = requests.delete('http://127.0.0.1:5000/advertising/1')

print(response.status_code)
print(response.json())


response = requests.get('http://127.0.0.1:5000/advertising/1')

print(response.status_code)
print(response.json())
