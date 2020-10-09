from setuptools import setup, find_packages
setup(
    name='sandbosh',
    version='0.0.1',
    description='Self-made shell Sandbox',
    long_description='README.md',
    author='Taku Kitamura',
    author_email='takukitamura.io@gmail.com',
    py_modules=['sandbosh'],
    packages=find_packages(exclude=('tests', 'docs')),
    license='GPL-3.0 License',
    url='https://sandbosh.com',
)
