import os
import shutil

import pytest


@pytest.fixture
def input_config_yaml_path():
    """returns path to the DAG configuration input YAML file"""
    here = os.path.dirname(os.path.abspath(__file__))
    return here + "/data"


@pytest.fixture
def input_config_yaml_file_name():
    """returns DAG configuration input YAML file name"""
    return "dag_properties.yml"


@pytest.fixture
def input_template_path():
    """returns path to the input dag template file"""
    here = os.path.dirname(os.path.abspath(__file__))
    return here + "/data"


@pytest.fixture
def input_template_file_name():
    """returns input dag template file name"""
    return "sample_dag_template.py.j2"


@pytest.fixture
def output_dag_path():
    """returns path for the generated DAG Py file"""
    here = os.path.dirname(os.path.abspath(__file__))
    dag_path = here + os.path.sep + "output"

    if not os.path.exists(dag_path):
        os.mkdir(dag_path)

    yield dag_path
    shutil.rmtree(dag_path, ignore_errors=True)  # remove folder regardless of read only files


@pytest.fixture
def output_dag_file_name():
    """returns name for the generated DAG Py file"""
    return "test_dag.py"


@pytest.fixture
def input_template_having_cyclic_task_dependency_file_name():
    """returns input invalid dag template having cyclic task dependency file name"""
    return "dag_template_having_cyclic_task_dependency.py.j2" \
 \
 \
@pytest.fixture
def input_template_having_invalid_arguments_file_name():
    """returns input invalid dag template having cyclic task dependency file name"""
    return "dag_template_having_invalid_arguments.py.j2"


@pytest.fixture
def input_template_having_invalid_task_file_name():
    """returns input invalid dag template having cyclic task dependency file name"""
    return "dag_template_having_invalid_task.py.j2"


@pytest.fixture
def input_template_having_typos_file_name():
    """returns input invalid dag template having cyclic task dependency file name"""
    return "dag_template_having_typos.py.j2"
