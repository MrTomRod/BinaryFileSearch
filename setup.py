from distutils.core import setup

setup(
    name='binary_file_search',
    packages=['binary_file_search'],
    version='0.1',
    license='MIT',
    description='Binary search algorithm for big sorted files that cannot be read into RAM.',
    author='Thomas Roder',
    author_email='roder.thomas@gmail.com',
    url='https://github.com/MrTomRod/',
    download_url='https://github.com/MrTomRod/BinaryFileSearch/archive/v0_1.tar.gz',
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
