What is AirflowDAGGenerator?
============================

Dynamically generates Python Airflow DAG file based on given Jinja2
Template and YAML configuration to encourage reusable code. It also
validates the correctness (by checking DAG contains cyclic dependency
between tasks, invalid tasks, invalid arguments, typos etc.) of the
generated DAG automatically by leveraging airflow DagBag, therefore it
ensures the generated DAG is safe to deploy into Airflow.

Why is it useful?
=================

Most of the time the Data processing DAG pipelines are same except the
parameters like source, target, schedule interval etc. So having a
dynamic DAG generator using a templating language can greatly benefit
when you have to manage a large number of pipelines at enterprise level.
Also it ensures code re-usability and standardizing the DAG, by having a
standardized template. It also improves the maintainability and testing
effort.

How is it Implemented?
======================

By leveraging the de-facto templating language used in Airflow itself,
that is Jinja2 and the standard YAML configuration to provide the
parameters specific to a use case while generating the DAG.

Requirements
============
Python 3.6 or later

Note: Tested on 3.6, 3.7 and 3.8 python environments, see tox.ini for details

How to use this Package?
========================

1. First install the package using:

  .. code-block:: bash

   pip install airflowdaggenerator

2. Airflow Dag Generator should now be available as a command line tool to execute. To verify run

  .. code-block:: bash

   airflowdaggenerator -h

3. Airflow Dag Generator can also be run as follows:

  .. code-block:: bash

   python -m airflowdaggenerator -h

Sample Usage:
=============
If you have installed the package then:
   .. code-block:: bash

    airflowdaggenerator \
        -config_yml_path path/to/config_yml_file \
        -config_yml_file_name  config_yml_file \
        -template_path path/to/jinja2_template_file \
        -template_file_name jinja2_template_file \
        -dag_path path/to/generated_output_dag_py_file \
        -dag_file_name generated_output_dag_py_file

OR
   .. code-block:: bash

    python -m airflowdaggenerator \
              -config_yml_path path/to/config_yml_file \
              -config_yml_file_name  config_yml_file \
              -template_path path/to/jinja2_template_file \
              -template_file_name jinja2_template_file \
              -dag_path path/to/generated_output_dag_py_file \
              -dag_file_name generated_output_dag_py_file

If you have cloned the project source code then you have sample jinja2 template and YAML configuration file present under
tests/data folder, so you can test the behaviour by opening a terminal window under project root directory and run the
following command:

   .. code-block:: bash

    python -m airflowdaggenerator \
              -config_yml_path ./tests/data \
              -config_yml_file_name dag_properties.yml \
              -template_path ./tests/data \
              -template_file_name sample_dag_template.py.j2 \
              -dag_path ./tests/data/output \
              -dag_file_name test_dag.py

And you can see that test_dag.py is created under ./tests/data/output folder.
