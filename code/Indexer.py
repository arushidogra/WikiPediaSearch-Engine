#!/usr/bin/env python
# -*- coding: utf-8 -*-


def indexing(final,filename):
    a = open(filename,"w+")
    for i in final.items():
	a.write(i[0] + i[1]+"\n")


