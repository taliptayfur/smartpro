#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

def what_is_my_ip():

	c = requests.session()

	r = c.get("http://localhost:8080/")
	return r.content

if __name__ == "__main__":
	print what_is_my_ip()