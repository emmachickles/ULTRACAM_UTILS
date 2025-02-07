from setuptools import setup, find_packages

setup(
    name='ULTRACAM_UTILS',
    packages=find_packages(),
    install_requires=[
        'hipercam @ git+https://github.com/HiPERCAM/hipercam.git',
        'numpy'
    ],
    package_data={
        'ULTRACAM_UTILS': ['paths.json'],
    }
)
