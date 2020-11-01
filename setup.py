from setuptools import setup, find_packages

setup_args = dict(
    name='mygit',
    version='1',    
    description='A Python library to clone and create a new git repository',
    url='https://github.com/test/mygit',
    author='No Body',
    author_email='test@email.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests','gitpython'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.'
    ],
)
if __name__ == '__main__':
    setup(**setup_args)