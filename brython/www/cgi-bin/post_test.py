#!c:/python34/python.exe
# -*- coding: utf-8 -*-


import cgi


print('Content-type: text/html\n\n')
print()
print('script cgi with post<p>')
fs = cgi.FieldStorage()
for key in tuple(fs.keys()):
    print(('%s:%s' % (key, fs[key].value) + '<br>'))
print('ok')
