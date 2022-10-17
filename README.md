# Databricks REST API with Python

A Python library created to easily use the Databricks services REST API with Python.

## Getting started

### Installing

The library can be installed using pip:

```
pip install dbrest
```

## Using the libary

### Importing the library

To add the library to your Python project, use the following line:

```
import dbrest
```

### Connecting to the Azure Databricks REST API

To connect to the Azure databricks REST API, you need to have a Microsoft account with databricks seriives that has access to API REST Services and an [Azure Databricks application](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/). With all that, you can connect to the Databricsk REST API using the following function:

```

dbrest.connect(
    domain = [domain (required)],
    username = [username (no mandatory)],
    password = [password (no mandatory)],
    bearer = [bearer (required)]
)
```

### Example 1 Getting all the list of queries.

As an example, here's how you can get a list of all the queries using the databricsk restful services:

```
dbrest.retrieve_a_list_of_queries()
```

### Example 2 Start the databricks cluster using the REST call.

As an example, here's how you can Start the databricks cluster using the REST call.
```
dbrest.cluster_start(cluster_id)

```

## Documentation

[See the documentation](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/)

## Author

[**Sai Krishna Cheruvu**](https://github.com/odbckrishna) - *Reachout me [Linkedin](https://www.linkedin.com/in/saicheruvu/)*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
