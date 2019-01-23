from setuptools import setup, find_packages
from datapump import __version__


setup(name='beepbeep-strava-worker',
      version=__version__,
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      entry_points="""
      [console_scripts]
      beepbeep-strava-worker = datapump.run:main
      """)
