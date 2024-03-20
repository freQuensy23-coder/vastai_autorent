from setuptools import setup

setup(
    name='vastai',
    version='0.2.0',  # choose your own version
    packages=['vastai'],
    entry_points={
        'console_scripts': [
            'vastai = vastai.vast:main',  # you need a main function in your vast.py file
        ],
    },
    description='Vast.ai Python CLI',
    #readme='README.md',
    url='https://github.com/vast-ai/vast-python',
    author='Vast.ai',
    author_email='support@vast.ai',
    license='MIT',  # choose your own license
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords=['CLI', 'Vast.ai', 'vast.ai', 'vast', 'vastai'],
    install_requires=['requests'],  # add any other dependencies your project needs
)