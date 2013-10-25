from setuptools import setup, find_packages

setup(
    name='mspacman',
    version='0.1.0',
    author='Daan Mathot',
    author_email='daanmathot@gmail.com',
    packages=find_packages(),
    scripts=['scripts/mspacman'],
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/dbsr/MsPacman',
    license='LICENSE.txt',
    description='pacman package auditor',
    long_description='\n' + open('README.md').read(),
    install_requires=[
        'Flask==0.9',
        'Jinja2==2.7',
        'MarkupSafe==0.18',
        'Werkzeug==0.8.3',
        'wsgiref==0.1.2'
    ],
)

