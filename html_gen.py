from cold_fuzzer import PageHolder

page = PageHolder().dump()
with open('last_page.html', 'w') as f:
	f.write(page)
print page