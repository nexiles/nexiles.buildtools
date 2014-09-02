from setuptools import setup

setup(
    name="nexiles.buildtools",
    version="0.1",
    packages=["nxdocserver"],
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points="""
    [console_scripts]
    nxdocserver=nxdocserver.docserver:cli
    """,
)
