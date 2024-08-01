from setuptools import setup, find_packages

setup(
    name='ULTRACAM_UTILS',
    packages=find_packages(),
    package_data={
        'ULTRACAM_UTILS': ['paths.json'],
    }
)
