from setuptools import setup

long_description = ""

try:
    import subprocess
    import pypandoc

    long_description = pypandoc.convert_file("README.md", to="rst", format="md")

except ImportError:
    pass


setup(
    name="asterisk_dialplan",
    version="0.2.0",
    author="Andrew Yager",
    author_email="andrew@rwts.com.au",
    license="BSD",
    packages=["asterisk_dialplan"],
    description="Helpers to convert numbers to dialplan strings for use in Asterisk",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
    ],
)
