from setuptools import setup

setup(
    name="name_scraper",
    version="1.1.2",
    author="Elliott Pardee",
    author_email="me@vypr.xyz",
    url="https://github.com/BibleBot/name_scraper",
    license="GPLv3",
    packages=["name_scraper", "name_scraper.ext"],
    data_files=[("mappings", ["name_scraper/mappings/master.json", "name_scraper/mappings/apibible.json"])],
    description="A scraping interface to fetch Bible book names from Bible Gateway and API.Bible.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=["lxml", "requests", "bs4", "colorama", "click"],
    python_requires=">=3.6.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Religion",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Religion",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ]
)