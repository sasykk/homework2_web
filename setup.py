from setuptools import setup, find_packages

setup(name='helper',
      version='0.0.1',
      description='Very usefull code',
      url='https://github.com/AllianceOfEmpires/Alliance.git',
      author='Alliance',
      author_email='',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'markdown',
      ],
      entry_points={'console_scripts': ['run=src.main:run']},
      include_package_data=True,
      zip_safe=False)
