from setuptools import setup

setup(
    name='pyansystools',
    version='0.0.5',
    packages=['tests', 'pyansystools'],
    url='https://github.com/natter1/pyansystools',
    license='MIT',
    author='Nathanael Jöhrmann',
    author_email='',
    description='Provides classes to simplify the work with ANSYS using the python module ansys-mapdl-core.',
    long_description='Provides classes to simplify the work with ANSYS using the python module ansys-mapdl-core.',
    install_requires=[
    ],
    python_requires='>=3.9',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    # package_data={
    #     #'examples': ['...'],
    # }
)
