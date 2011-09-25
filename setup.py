
from setuptools import setup

version = '0.0.1'

setup(
    name='ecbv',
    version=version,
    description="A Django generic view alternative.",
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='django',
    author='Xavier Ordoquy',
    author_email='xordoquy@linovia.com',
    url='http://www.linovia.com',
    packages=['ecbv'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'docutils',
    ],
)
