from setuptools import setup, find_packages

setup(name='app',
      version='1.0',
      description='Exploring the capabilities of FastAPI',
      author='Sam Vermeulen',
      author_email='sam.verm@yahoo.com',
      packages=find_packages(),
      entry_points={
          "console_scripts": [
              "app-server = app:main"
          ]
      },
      test_suite='tests'
      )
