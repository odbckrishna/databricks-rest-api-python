import setuptools

setuptools.setup(
    name = "dbrest",
    packages = setuptools.find_packages(),
    version = "0.0.6",
    license = "MIT",
    description = "A Python library created to easily use the Databricks REST API with Python",
    long_description = "A Python library created to easily use the Databricks REST API with Python",
    author = "Saikrishna Cheruvu",
    author_email = "odbc.krishna@gmail.com",
    url = "https://github.com/odbckrishna/databricks-rest-api-python",
    keywords = ["databricsks", "rest", "api", "rest api"],
    install_requires = [
        "requests"
    ],
    classifiers = [
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6"
    ]
)
