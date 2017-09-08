from setuptools import setup

setup(name='boxus',
      version='0.1.1',
      description='High-level framework for easy control of multiple devices connected to the Raspberry Pi and Arduino via GPIO',
      url='https://github.com/boxus-plants/boxus',
      download_url='https://pypi.python.org/pypi/boxus',
      author='Alexey Kondratov',
      author_email='kondratov.aleksey@gmail.com',
      license='GNU General Public License v3.0',
      packages=['boxus'],
      install_requires=['nanpy', 'couchdb', 'pyyaml', 'python-crontab'],
      zip_safe=False)
