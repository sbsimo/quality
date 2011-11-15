import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="quality",
    version="0.1",
    author="Simone Dalmasso, Simone Balbo",
    author_email="simone.blb@gmail.com",
    description="Data quality extension for GeoNode",
    long_description=(read('README.rst')),
    classifiers=[
        'Development Status :: 2 - Pre-alpha',
        'Framework :: GeoNode',
        'License :: OSI Approved :: BSD',
    ],
    license="BSD",
    keywords="geonode django",
    url='https://github.com/sbsimo/quality',
    scripts = [
              ],
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
)
