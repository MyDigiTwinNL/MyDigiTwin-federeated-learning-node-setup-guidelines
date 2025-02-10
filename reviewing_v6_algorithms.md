
# Reviewing a MyDigiTwin algorithm

This document provides a quick overview of how to review a vantage6 algorithms created for the MyDigiTwin project. It serves as a resource for node administrators during the process of white-listing a new algorithm in their respective node configuration.

## MyDigiTwin - vantage6 Algorithms

The vantage6 algorithms are distributed as Docker packages. These containers encapsulate a Python project developed by the algorithm creator, built on top of a series of standard vantage6 libraries. The [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6), a proof-of-concept algorithm developed for the platform will be used as a reference for these guidelines.

Like [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6), the source code of any algoritjm developed for the MyDigiTwin project will be hosted on the the https://github.com/MyDigiTwinNL organization. Likewise, the Docker package of these projects will be automatically built using the CI/CD features provided by GitHub actions, and hosted on the [organization's registry (ghcr.io/mydigitwinnl)](https://github.com/orgs/MyDigiTwinNL/packages). This way, the algorithm reviewers can easily refer to the precise version (or commit) of the source of the Docker package they are requested to whitelist. By convention, it is expected that the Docker images will be built using either the hash code of the Git commit, or the release version as a Tag. For example, in the image below, the image built for the [FedAvg](https://github.com/MyDigiTwinNL/FedAvg_vantage6) algorithm has, as a Tag, a hashcode that starts with 88027f24:

![alt text](image-1.png)

Which can be traced to one of the algorithms' source code commits:

![alt text](image.png)

## Image structure

Once the corresponding Tag/Commit has been identified, the following base structure can be used to explore the components of the algorithm:

```
Dockerfile
LICENSE
README.md
algorithm_store.json
docs
<algorithm_name>/
    __init__.py    
    central.py
    partial.py
requirements.txt
setup.py
test
```

### Dockerfile 

The following is a standard Dockerfile of a vantage6 algorithm. Here it is important to check that the based image is hosted on `harbor2.vantage6.ai`, and that any additional dependencies (e.g., installed with `pip install`) are reliable ones.

```Dockerfile
# basic python3 image as base
FROM harbor2.vantage6.ai/infrastructure/algorithm-base

ARG PKG_NAME="<algorithm_name>"

# install federated algorithm
COPY . /app
RUN pip install /app

ENV PKG_NAME=${PKG_NAME}

# Tell docker to execute `wrap_algorithm()` when the image is run. This function
# will ensure that the algorithm method is called properly.
CMD python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"

```

The **setup.py** file can be checked to ensure that the included dependencies are reliable ones. This involves verifying that the packages listed under `install_requires` are from trusted sources and have no known vulnerabilities:


```python
from os import path
from codecs import open
from setuptools import setup, find_packages

setup(
    name='<algorithm_name>',
    version="1.0.0",
    description='...',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'vantage6-algorithm-tools',
        'pandas',
        'psutil',
        '...'
    ]
)
```

### Algorithm internals

The `__init__.py` file in the Python package folder defines which functions can be accessed when the package is imported. From this you can identify which modules and functions can be eventually requested from an authorized vantage6 client (an example of how the client can do this [is included on the FedAvg algorithm](https://github.com/MyDigiTwinNL/FedAvg_vantage6/blob/main/sample_client/research_env_client_notebook.ipynb).

## `<algorithm_name>/__init__.py`
```python
from .central import *
from .partial import *
```

From the functions imported above, most vantage6 algorithms, as expected for a federated learning framework, include at least two functions: a 'central' one and a 'partial' one. The 'partial' function generally performs computations on the nodes, while the 'central' function orchestrates these computations. There are no strict naming conventions for these functions, but you can identify them based on what they do internally. For example, the following function can be considered 'central' not only because of its name but also because it requests the execution of 'partial' functions on all nodes within a collaboration. One hint to identify a central function is the lack of any input data, and the use of an `@algorithm_client` decorator, which provides only methods for making requesting to other nodes. 

## Module with a 'central' function (in this example: `<algorithm_name>/central.py`)

```python
...

@algorithm_client
def central(
    client: AlgorithmClient, argx, argy, argz
) -> Any:

    """ Central part of the algorithm """
    organizations = client.organization.list()
    org_ids = [organization.get("id") for organization in organizations]

    # Define input parameters for a subtask
    info("Defining input parameters")
    input_ = {
        "method": "partial",
        "kwargs": {
            "argx": argx,
            "argy": argy,
            "argz": argz,
        }
    }

    # create a subtask for all organizations in the collaboration.

    info("Creating subtask for all organizations in the collaboration")
    task = client.task.create(
        input_=input_,
        organizations=org_ids,
        name="Network diagnostics",
        description="Network diagnostics"
    )

    # wait for node to return results of the subtask.
    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Results obtained!")

    agg_res=aggregate_results(results)

    # return the aggregated results of the algorithm
    return agg_res
```

The 'partial' functions, which are expected to process data on the nodes, can be identified by the use of the `@data` decorator. Typically, a 'partial' function processes local data and returns the (partial) results, which are eventually aggregated in a 'central' function. Note that:

- The `DataFrame` provided by the framework to this method (throuth the `@data` decorator) corresponds to the database name requested by the client (see [Step 3 of the sample client workbook](https://github.com/MyDigiTwinNL/FedAvg_vantage6/blob/main/sample_client/research_env_client_notebook.ipynb)).
- On a given node, this database corresponds, in turn, to [the one set in the node configuration with the same name](https://github.com/MyDigiTwinNL/MyDigiTwin-federeated-learning-node-setup-guidelines#22-edit-the-corresponding-file).


## Module with a 'partial' function (accessing data). In this example: `<algorithm_name>/partial.py`)

```python
@data(1)
def partial_risk_prediction(
    df1: pd.DataFrame, argx, argy, argz
) -> Any:

    #Process the database
    m = df1.mean()
    ...

    return {
        "partial_result": ...
    }
```


A more in-depth overview of how a vantage6 algorithm is developed is available on the [vantage6 documentation](https://docs.vantage6.ai/en/main/algorithms/index.html).

