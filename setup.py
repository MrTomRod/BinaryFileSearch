from distutils.core import setup
from os import path

# Instructions:
# https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

setup(
    name='binary_file_search',
    packages=['binary_file_search'],
    version='0.4',
    license='MIT',
    description='Binary search algorithm for big sorted files that cannot be read into RAM.',
    long_description='Please read the descriptionon on the github page.',
    author='Thomas Roder',
    author_email='roder.thomas@gmail.com',
    url='https://github.com/MrTomRod/BinaryFileSearch',
    download_url='https://github.com/MrTomRod/BinaryFileSearch/archive/v0_4.tar.gz',
    keywords=['binary', 'search', 'file', 'files'],
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
