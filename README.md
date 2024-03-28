# Code Repository for Securing Application Data in Temporal (Python)
This repository provides code used for exercises and demonstrations
included in the Python version of the 
[Securing Application Data](https://learn.temporal.io/courses/appdatasec) 
training course.

It's important to remember that the example code used in this course was designed to support learning a specific aspect of Temporal, not to serve as a ready-to-use template for implementing a production system.

## Hands-On Exercises

Directory Name                     | Exercise
:--------------------------------- | :-------------------------------------------------------
`exercises/custom-converter`       | [Exercise 1](exercises/custom-converter/README.md)
`exercises/codec-server`           | [Exercise 2](exercises/codec-server/README.md)

Samples
| Directory Name                | Description                                                                                                                   |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `samples/composite-converter` | [Sample of how to provide an additional Payload Converter to your Composite Converter](samples/composite-converter/README.md) |

## Reference
The following links provide additional information that you may find helpful as you work through this course.
- [General Temporal Documentation](https://docs.temporal.io/)
- [Temporal Python SDK Documentation](https://python.temporal.io/)
- [Python Language Documentation](https://docs.python.org/3/)
- [Python Packaging and Virtual Environment Documentation](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments)
- [GitPod Documentation: Troubleshooting](https://www.gitpod.io/docs/troubleshooting)

### Set Up Your Python Virtual Environment

All Python libraries for this course should be installed in a virtual environment.
If you are running these exercises in the course's GitPod environment, there
is a virtual environment already setup for you and you can skip this section.
If you are running these exercises locally, be sure you are using Python 3.7+.

1. Open a terminal window in the environment and change directories to the root directory of the
   `edu-appdatasec-python-code` repository
2. Run the following command to create a virtual environment

```
$ python3 -m venv env
```

3. Activate the virtual environment

**Linux/Mac**:

```
$ source env/bin/activate
```

**Windows**:

```
$ env\Scripts\activate
```

Once the environment is active you should see `(env)` prepended to your prompt similar
to below

```
(env) $
```

4. Install the necessary packages into the virtual environment

```
python -m pip install -r requirements.txt
```

5. For every new terminal you open, you will need to activate the environment using
   the following command

**Linux/Mac**:

```
$ source env/bin/activate
```

**Windows**:

```
$ env\Scripts\activate
```

However, the packages are already installed, so there is no need to run pip again.


## Exercise Environment for this Course
You can launch an exercise environment for this course in GitPod by 
clicking the button below:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/temporalio/edu-appdatasec-python-code)

Alternatively, you can follow 
[these instructions](https://learn.temporal.io/getting_started/python/dev_environment/) to 
set up your own Temporal Cluster with Docker Compose, which you can use as an 
exercise environment.
