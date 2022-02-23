#This file converts the javascript file to a python file
import js2py
print("converting from javascript to python")
js2py.translate_file('mapgen.js', 'mapgen.py')