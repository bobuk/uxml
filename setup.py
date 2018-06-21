from setuptools import setup, find_packages
with open('README.md') as readme_file:
    README = readme_file.read()

setup(name="uxml", version="0.1.0",
      py_modules=['uxml'],
      url="http://github.com/bobuk/uxml",
      author="Grigory Bakunov",
      author_email='thebobuk@ya.ru',
      description='uRPC is oversimplistic stream XML parser',
      long_description=README,
      long_description_content_type="text/markdown",
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],

)
