from setuptools import setup
import distutils.command.install_egg_info
import hhmon


class MyEggInfo(distutils.command.install_egg_info.install_egg_info):
    """
    Disable egg_info installation, seems pointless for a non-library.
    Copied from virt-manager.
    """
    def run(self):
        pass


setup(
    name='hhmon',
    version=hhmon.__version__,
    url='https://github.com/tieugene/hhmon/',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='HH.ru crowler',
    python_requires='>=3.8',
    keywords="flask headhunter",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=('hhmon',),
    install_requires=[
        'Flask',
        'requests',
    ],
    include_package_data=True,
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
    cmdclass={
        'install_egg_info': MyEggInfo,
    },
)
