#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

urls = ('/', 'index')

app = web.application(urls, globals())

class index:
	def get(self):
		return web.ctx.ip

def main():
	app.run()

if __name__ == "__main__":
	main()