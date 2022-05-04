
import sys
from setuptools import Extension, setup

mgl = Extension(
    name='shaun_gui_functions.shaun_gui_functions',
    include_dirs=['src', 'shaun_gui_functions'],
    sources=[
        sys.path[0] + '/shaun_gui_functions/src/shaun_gui_functions.cpp',
    ],
)

short_description = 'Functions For Shaun Gui'

keywords = [
    '2D',
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Games/Entertainment',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Multimedia :: Graphics :: 3D Rendering',
    'Topic :: Scientific/Engineering :: Visualization',
    'Programming Language :: Python :: 3 :: Only',
]

setup(
    name='shaun_gui_functions',
    version='1',
    description=short_description,
    url='',
    author='',
    author_email='',
    license='MIT',
    classifiers=classifiers,
    keywords=keywords,
    packages=['shaun_gui_functions'],
    package_data={"shaun_gui_functions": ["shaun_gui_functions.pyi"]},
    ext_modules=[mgl],
    platforms=['any'],
)