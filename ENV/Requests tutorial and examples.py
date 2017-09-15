import requests
import json

# query = input("Please input your query terms : ")
# params = {"q" : query}
# r = requests.get("https://www.google.com.sg/search?", params= params)
#
# URL = r.url
# encoding = r.encoding
# headers = r.headers
# content = r.content
# text = r.text
# if r.json is not None:
#     json = r.json
# else:
#     print("JSON Empty")
# status = r.raise_for_status()
# status_code = r.status_code
#
# print("URL : " + str(URL))
# print("Response :" + str(r))
# print("Encoding : " + str("Original Encoding : " + encoding))
# r.encoding = 'ISO-8859-1'
# encoding = r.encoding
# print("New Encoding : " + str(encoding))
# print("Headers : " + str(headers))
# # Content is the response body as bytes
# print("Content : " + str(content))
# # Text is the response body as text
# print("Text : " + str(text))
# if json is not None:
#     print("JSON : " + str(json))
# print("Status : " + str(status))
# print("Status Code : " + str(status_code))


# Accessing the raw socket response from the server
# r = requests.get("https://www.google.com.sg", stream=True)
# print(r.raw)
# print(r.raw.read())
#
# # Saving to a file
# with open("test.txt", "wb") as fd:
#     for block in r.iter_content(chunk_size=128):
#         fd.write(block)

# Custom headers {dict}
# Note: All header values must be a string, bytestring, or unicode. While permitted,
# it's advised to avoid passing unicode header values.
# header = {"user-agent" : "my-app/0.0.1"}
# r = requests.get("https://www.google.com.sg", headers=header)
# print("Headers: ")
# print(r.headers)


# POST requests
# payload = {"key1" : "value1" , "key2" : "value2"}
# r = requests.post("http://httpbin.org/post", data=payload)
# print(r.text)

# Passing tuple as data
# payload = (("key1", "value1"), ("key2", "value2"))
# r = requests.post(("http://httpbin.org/post"),data=payload)
# print(r.text)

# send data that is not form-encoded. If you pass in a string instead of a dict, that data will be posted directly.
# For example, the GitHub API v3 accepts JSON-Encoded POST/PATCH data:
# payload = {"some" : "data"}
# r = requests.post('https://api.github.com/some/endpoint',data=json.dumps(payload))

# Instead of encoding the dict yourself, you can also pass it directly using the json parameter (added in version 2.4.2)
# and it will be encoded automatically:
# payload = {"some" : "data"}
# r = requests.post("https://api.github.com/some/endpoint",json=payload)

# # Post a multi-part encoded file
# url = "http://httpbin.org/post"
# files = {"file", open("test.txt", "rb")}
# r = requests.post(url,files=files)
# print(r.text)
#
# # Set filename,content type and headers explicity
# url = 'http://httpbin.org/post'
# files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
#
# r = requests.post(url, files=files)
# r.text

# Send strings to be received as files
# WARNING
# It is strongly recommended that you open files in binary mode. This is because Requests may attempt to provide the
# Content-Length header for you, and if it does this value will be set to the number of bytes in the file. Errors may
# occur if you open the file in text mode.

# url = 'http://httpbin.org/post'
# files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
#
# r = requests.post(url, files=files)
# r.text


# Check response status code
# r = requests.get("http://httpbin.org/get")
# print(r.status_code)
# # Requests also comes with a built-in status code lookup object for easy reference:
# if r.status_code == requests.codes.ok:
#     print(requests.codes.ok)

# If we made a bad request (a 4XX client error or 5XX server error response), we can raise it with
# Response.raise_for_status()
# bad_r = requests.get("http://httpbin.org/status/404")
# print(bad_r.status_code)
# bad_r.raise_for_status()

# # If status is ok(200)
# r = requests.get("http://httpbin.org/get")
# # No status
# r.raise_for_status()
#
# # Response Headers
# print(r.headers)
# # HTTP headers are case insensitive so we can access the headers using any capitalization we want:
# print(r.headers["CONTENT-TYPE"])
# print(r.headers["content-type"])

# Accessing cookies
# url = 'http://example.com/some/cookie/setting/url'
# r = requests.get(url)
# cookies = r.cookies
# print(cookies["example_cookie_name"])

# Sending cookies to the server
# url = "http://httpbin.org/cookies"
# cookie = {"test_cookie" : "working"}
# r = requests.get(url,cookies=cookie)
# print(r.text)


# Cookies are returned in a RequestsCookieJar, which acts like a dict but also offers a more complete interface,
# suitable for use over multiple domains or paths. Cookie jars can also be passed in to requests:
# jar = requests.cookies.RequestsCookieJar()
# jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
# jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
# url = "http://httpbin.org/cookies"
# r = requests.get(url,cookies=jar)
# print(r.text)

# Redirection and History
# By default Requests will perform location redirection for all verbs except HEAD.
# We can use the history property of the Response object to track redirection.
# The Response.history list contains the Response objects that were created in order to complete the request. The list is sorted from the oldest to the most recent response.
# For example, GitHub redirects all HTTP requests to HTTPS:
# r = requests.get("http://github.com")
# print(r.url)
# print(r.history)

# Disableing redirects
# r = requests.get("http://github.com", allow_redirects= False)
# print(r.status_code)
# print(r.history)

# Redirection can be enabled with HEAD requests. HEAD = > Response has no message body
# r = requests.head("http://github.com", allow_redirects= True)
# print(r.status_code)
# print(r.history)

# You can tell Requests to stop waiting for a response after a given number of seconds with the timeout parameter.
# Nearly all production code should use this parameter in nearly all requests.
# Failure to do so can cause your program to hang indefinitely:
r = requests.get("http://github.com", timeout=1.0)

# Errors and Exceptions
# In the event of a network problem (e.g. DNS failure, refused connection, etc), Requests will raise a ConnectionError exception.
# Response.raise_for_status() will raise an HTTPError if the HTTP request returned an unsuccessful status code.
# If a request times out, a Timeout exception is raised.
# If a request exceeds the configured number of maximum redirections, a TooManyRedirects exception is raised.
# All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException.
