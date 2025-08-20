from setuptools import setup

setup(
    name='shell-keeper',
    version='0.1.0',
    py_modules=['sk'],
    install_requires=[
        'pyperclip',
    ],
    entry_points={
        'console_scripts': [
            'sk=sk:main',
        ],
    },
    author='trevortomesh',
    description='Shell Keeper: Save and retrieve shell commands from the terminal.',
    url='https://github.com/trevortomesh/shell-keeper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
