from setuptools import setup

long_description = ''
 
try:
    import subprocess
    import pandoc
 
    process = subprocess.Popen(
        ['which pandoc'],
        shell=True,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
 
    pandoc_path = process.communicate()[0]
    pandoc_path = pandoc_path.strip('\n')
 
    pandoc.core.PANDOC_PATH = pandoc_path
 
    doc = pandoc.Document()
    doc.markdown = open('README.md').read()
 
    long_description = doc.rst
 
except:
    pass


setup(
	name="asterisk_dialplan",
	version="0.1.2",
	author="Andrew Yager",
	author_email="andrew@rwts.com.au",
	license="BSD",
	packages=['asterisk_dialplan'],
	description="Helpers to convert numbers to dialplan strings for use in Asterisk",
	long_description=long_description,
	classifiers=[
		"Development Status :: 4 - Beta",
		"Topic :: Communications :: Telephony",
		"Topic :: Software Development :: Libraries",
		"License :: OSI Approved :: BSD License",
		]
)
