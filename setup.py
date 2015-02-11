__author__ = 'guyanhua'

from distutils.core import setup
import py2exe
import os,sys
import shutil
from glob import glob

sys.argv.append('py2exe')

py2exe_options = {
    "includes":['sip','cx_Oracle','decimal',"encodings", "encodings.*"],
    "optimize":0,
    "dist_dir": "bin", 
    'bundle_files':1,
    'compressed':True,
    'dll_excludes':["oci.dll"],
    }


setup(
    console = ['Delete_Import_Export_EnodeB.py',],
    options = {'py2exe':py2exe_options}
    )
