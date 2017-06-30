from setuptools import setup

setup(name='boxus',
      version='0.0.3',
      description='Open automated plants grow pod project',
      url='https://github.com/boxus-plants/boxus',
      download_url='https://pypi.python.org/pypi/boxus',
      author='Alexey Kondratov',
      author_email='kondratov.aleksey@gmail.com',
      license='GNU General Public License v3.0',
      packages=['boxus'],
      install_requires=['nanpy', 'couchdb', 'pyyaml', 'python-crontab'],
      zip_safe=False)
