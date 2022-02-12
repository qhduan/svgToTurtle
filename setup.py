from setuptools import setup
import codecs
import os


VERSION = '1.0.0'
AUTHOR_NAME = 'QHDuan'
AUTHOR_EMAIL = 'mail@qhduan.com'
GITHUB = 'https://github.com/qhduan/svgToTurtle'


setup(name='svg2turtle',
      packages=['svg2turtle'],
      version=VERSION,
      description=('A tool to convert svg image to turtle script.'),
      long_description_content_type='text/markdown',
      author=AUTHOR_NAME,
      author_email=AUTHOR_EMAIL,
      url=GITHUB,
      license='MIT',
      install_requires=['svgpathtools', 'fire'],
      keywords=['svg', 'svg path', 'svg.path', 'turtle'],
      platforms='any',
      entry_points={
            'console_scripts': [
                  'svg2turtle = svg2turtle.cli:cmd',
            ],
      },
      )