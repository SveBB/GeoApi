import requests

print('Method-1 Test-1')
url = 'http://127.0.0.1:8000//api/method1/451769'
post = requests.get(url)
print(post)
print(post.text)

print('Method-1 Test-2')
url = 'http://127.0.0.1:8000//api/method1/1'
post = requests.get(url)
print(post)
print(post.text)

print('Method-1 Test-3')
url = 'http://127.0.0.1:8000//api/method1/asd'
post = requests.get(url)
print(post)
print(post.text)

print('Method-2 Test-1')
url = 'http://127.0.0.1:8000//api/method2?page=8&num=3'
post = requests.get(url)
print(post)
print(post.text)

print('Method-3 Test-1')
url = 'http://127.0.0.1:8000//api/method3/Якимово&Волосово'
post = requests.get(url)
print(post)
print(post.text)

print('Method-3 Test-2')
url = 'http://127.0.0.1:8000//api/method3/Явидово&Явидово'
post = requests.get(url)
print(post)
print(post.text)

print('Method-3 Test-3')
url = 'http://127.0.0.1:8000//api/method3/Zyabrikovo&Yeskino'
post = requests.get(url)
print(post)
print(post.text)

print('Method-Additional Test-1')
url = 'http://127.0.0.1:8000//api/additional_method/Явид'
post = requests.get(url)
print(post)
print(post.text)

print('Method-Additional Test-2')
url = 'http://127.0.0.1:8000//api/additional_method/Mos'
post = requests.get(url)
print(post)
print(post.text)
