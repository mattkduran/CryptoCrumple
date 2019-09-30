from distutils.core import setup

setup(name='CryptoCrumple',
      version='1.0.0',
      description="Encryption process for journald",
      author="Matt Duran",
      author_email="matduran@pdx.edu",
      url="https://github.com/mattkduran/CryptoCrumple/",
      packages=['cryptocrumple'],
      classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: Beta',
        'Environment :: Console',
        'Operating System :: Debian',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Encryption',
        'Topic :: Software Development :: systemd',
        'Topic :: journald']
)
