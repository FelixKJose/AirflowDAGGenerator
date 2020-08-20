import os
import sys

import jinja2
import pytest
from mock import patch

from airflowdaggenerator import airflowdaggenerator


def test_generate_dag_throws_exception_when_input_config_yaml_not_present(input_template_path, input_template_file_name,
                                                                          output_dag_path, output_dag_file_name):
    with pytest.raises(FileNotFoundError):
        airflowdaggenerator.generate_dag("", "test.yml", input_template_path, input_template_file_name,
                                         output_dag_path,
                                         output_dag_file_name)


def test_generate_dag_throws_exception_when_input_config_yaml_file_is_not_yml(input_config_yaml_path,
                                                                              input_template_path,
                                                                              input_template_file_name,
                                                                              output_dag_path, output_dag_file_name):
    with pytest.raises(ValueError):
        airflowdaggenerator.generate_dag(input_config_yaml_path, "test.txt", input_template_path,
                                         input_template_file_name,
                                         output_dag_path, output_dag_file_name)


def test_generate_dag_throws_exception_when_input_template_file_not_present(input_config_yaml_path,
                                                                            input_config_yaml_file_name,
                                                                            input_template_file_name,
                                                                            output_dag_path, output_dag_file_name):
    with pytest.raises(jinja2.exceptions.TemplateNotFound):
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name, ".",
                                         input_template_file_name,
                                         output_dag_path, output_dag_file_name)


def test_generate_dag_throws_exception_when_output_dag_file_name_is_not_a_py_file(input_config_yaml_path,
                                                                                  input_config_yaml_file_name,
                                                                                  input_template_file_name,
                                                                                  output_dag_path):
    with pytest.raises(ValueError):
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name, ".",
                                         input_template_file_name,
                                         output_dag_path, "test.txt")


def test_generate_dag_outputs_a_dag_py_file_from_valid_dag_template_and_yml_file(input_config_yaml_path,
                                                                                 input_config_yaml_file_name,
                                                                                 input_template_path,
                                                                                 input_template_file_name,
                                                                                 output_dag_path, output_dag_file_name):
    airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name, input_template_path,
                                     input_template_file_name, output_dag_path, output_dag_file_name)
    output_dag_file = output_dag_path + os.path.sep + output_dag_file_name

    assert os.path.exists(output_dag_file) and os.path.isfile(output_dag_file)


def test_validate_dag_throws_exception_when_generated_dag_file_has_cycle(input_config_yaml_path,
                                                                         input_config_yaml_file_name,
                                                                         input_template_path,
                                                                         input_template_having_cyclic_task_dependency_file_name,
                                                                         output_dag_path,
                                                                         output_dag_file_name):
    with pytest.raises(AssertionError):
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name,
                                         input_template_path,
                                         input_template_having_cyclic_task_dependency_file_name, output_dag_path,
                                         output_dag_file_name)

        airflowdaggenerator.validate_dag(output_dag_path)


def test_validate_dag_throws_exception_when_generated_dag_file_has_invalid_arguments(input_config_yaml_path,
                                                                                     input_config_yaml_file_name,
                                                                                     input_template_path,
                                                                                     input_template_having_invalid_arguments_file_name,
                                                                                     output_dag_path,
                                                                                     output_dag_file_name):
    with pytest.raises(AssertionError) as exception_info:
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name,
                                         input_template_path, input_template_having_invalid_arguments_file_name,
                                         output_dag_path, output_dag_file_name)

        airflowdaggenerator.validate_dag(output_dag_path)
    assert "__init__() got an unexpected keyword argument 'dag_ids'" in str(exception_info.value)


def test_validate_dag_throws_exception_when_generated_dag_file_has_invalid_tasks(input_config_yaml_path,
                                                                                 input_config_yaml_file_name,
                                                                                 input_template_path,
                                                                                 input_template_having_invalid_task_file_name,
                                                                                 output_dag_path, output_dag_file_name):
    with pytest.raises(AssertionError) as exception_info:
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name,
                                         input_template_path, input_template_having_invalid_task_file_name,
                                         output_dag_path, output_dag_file_name)

        airflowdaggenerator.validate_dag(output_dag_path)
    assert "name \'echo_task\' is not defined" in str(exception_info.value)


def test_validate_dag_throws_exception_when_generated_dag_file_has_typos(input_config_yaml_path,
                                                                         input_config_yaml_file_name,
                                                                         input_template_path,
                                                                         input_template_having_typos_file_name,
                                                                         output_dag_path,
                                                                         output_dag_file_name):
    with pytest.raises(AssertionError) as exception_info:
        airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name, input_template_path,
                                         input_template_having_typos_file_name, output_dag_path, output_dag_file_name)

        airflowdaggenerator.validate_dag(output_dag_path)

    # /tests/output/test_dag.py", line 32 (jinja2 template variable {{bash_task_id}} is typoed as {{bash_task_ids}}
    assert 'The key () has to be made of alphanumeric characters, dashes, dots and underscores exclusively' in str(
        exception_info.value)


def test_validate_dag_throws_no_exception_when_generated_dag_file_is_valid(input_config_yaml_path,
                                                                           input_config_yaml_file_name,
                                                                           input_template_path,
                                                                           input_template_file_name,
                                                                           output_dag_path, output_dag_file_name):
    airflowdaggenerator.generate_dag(input_config_yaml_path, input_config_yaml_file_name, input_template_path,
                                     input_template_file_name, output_dag_path, output_dag_file_name)

    airflowdaggenerator.validate_dag(output_dag_path)


@pytest.mark.parametrize("input_args", [pytest.param([], id='no_arguments_provided'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_file_name", "dag_properties.yml",
                                                      "-template_path", "./tests/data", "-template_file_name",
                                                      "sample_dag_template.py.j2",
                                                      "-dag_path", "./tests/data/output", "-dag_file_name",
                                                      "test_dag.py"], id='config_yml_path_missing'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_path", "./tests/data",
                                                      "-template_path", "./tests/data", "-template_file_name",
                                                      "sample_dag_template.py.j2",
                                                      "-dag_path", "./tests/data/output", "-dag_file_name",
                                                      "test_dag.py"], id='config_yml_file_name_missing'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_path", "./tests/data",
                                                      "-config_yml_file_name", "dag_properties.yml",
                                                      "sample_dag_template.py.j2",
                                                      "-dag_path", "./tests/data/output", "-dag_file_name",
                                                      "test_dag.py"], id='template_path_missing'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_path", "./tests/data",
                                                      "-config_yml_file_name", "dag_properties.yml",
                                                      "-template_path", "./tests/data",
                                                      "-dag_path", "./tests/data/output", "-dag_file_name",
                                                      "test_dag.py"], id='template_file_name_missing'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_path", "./tests/data",
                                                      "-config_yml_file_name", "dag_properties.yml",
                                                      "-template_path", "./tests/data",
                                                      "-template_file_name", "sample_dag_template.py.j2",
                                                      "-dag_file_name", "test_dag.py"], id='dag_path_missing'),
                                        pytest.param(["airflowdaggenerator",
                                                      "-config_yml_path", "./tests/data",
                                                      "-config_yml_file_name", "dag_properties.yml",
                                                      "-template_path", "./tests/data",
                                                      "-template_file_name", "sample_dag_template.py.j2",
                                                      "-dag_path", "./tests/data/output"], id='dag_file_name_missing'),
                                        ])
def test_main_throws_exception_when_required_input_arguments_are_not_provided(input_args):
    with patch.object(sys, 'argv', input_args):
        with pytest.raises(SystemExit):
            airflowdaggenerator.main()


def test_main_generates_output_dag_file_when_required_input_arguments_are_provided(input_config_yaml_path,
                                                                                   input_config_yaml_file_name,
                                                                                   input_template_path,
                                                                                   input_template_file_name,
                                                                                   output_dag_path,
                                                                                   output_dag_file_name):
    with patch.object(sys, 'argv', ["prog",
                                    "-config_yml_path", input_config_yaml_path,
                                    "-config_yml_file_name", input_config_yaml_file_name,
                                    "-template_path", input_template_path,
                                    "-template_file_name", input_template_file_name,
                                    "-dag_path", output_dag_path, "-dag_file_name", output_dag_file_name]):
        airflowdaggenerator.main()
    output_dag_file = output_dag_path + os.path.sep + output_dag_file_name

    assert os.path.exists(output_dag_file) and os.path.isfile(output_dag_file)
