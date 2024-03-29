import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taroc",
    version="0.0.1",
    author="Stan Svec",
    author_email="stan.x.svec@gmail.com",
    description="CLI Client of Taro REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StanSvec/taroc",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers, Ops, Admins",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.7',
    packages=setuptools.find_packages(exclude=("test",)),
    install_requires=[
        "PyYAML>=5.1.2",
        "asyncssh>=2.6.0",
        "rich>=10.7.0",
        "sshconf>=0.2.2",
        "pyxdg>=0.27",
    ],
    package_data={
        'taroc': ['config/*.yaml'],
    },
)
