from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='webdriver_auto_update',
    version='0.0.3.1',
    description='Checks local chrome driver version and automatically download the latest available version online',
    author='Rony Khong',
    author_email='ronykhong77@gmail.com',
    url='https://github.com/competencytestlvl/webdriver_auto_update',
    py_modules=['webdriver_auto_update'],
    packages=find_packages(),
    package_dir={'': 'src'},
    python_requires='>=3.9',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=[
        'auto',
        'browser',
        'chrome',
        'driver',
        'download',
        'selenium',
        'web',
        'webdriver',
        'update'],
    install_requires=[
        'requests',
        'wget'],
    )
