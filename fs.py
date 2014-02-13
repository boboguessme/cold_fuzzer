import web

from cold_fuzzer import PageHolder

urls = (
	'/', 'index'
)

class index:
	def GET(self):
		page = PageHolder().dump()
		with open('/tmp/fs/last_page.html', 'w') as f:
			f.write(page)
		return page

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()