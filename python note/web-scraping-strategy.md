

	import urllib2
	import cookielib

	# create cookiejar to store cookie
	cj = cookielib.CookieJar()

	# IP:PORT
	proxy_address = '66.98.208.8:3128' # change the IP:PORT, this one is for example

	# create the proxy handler
	proxy_handler = urllib2.ProxyHandler({'http': proxy_address})

	# create opener
	opener = urllib2.build_opener(proxy_handler, urllib2.HTTPCookieProcessor(cj))

	# install the opener
	urllib2.install_opener(opener)

	# url to browse / visit
	url = "http://www....com/" # change the url

	req=urllib2.Request(url)

	data=urllib2.urlopen(req).read()

	print data

	# now write the data to a text file

	# create file handler
	fh = open('page.txt', 'w')

	data = "".join(data)

	# write to file
	fh.write(data)

	# close the file handler
	fh.close()

lambda

	nums = range(2, 100)
	for i in range(2, 10):
	    nums = filter(lambda x: x == i or x % i, nums)
	print nums