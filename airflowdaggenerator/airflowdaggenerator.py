import argparse
import os
import sys

import yaml
from airflow.models import DagBag
from jinja2 import Environment, FileSystemLoader


def generate_dag(input_config_yaml_path, input_config_yaml_file_name, input_template_path, input_template_file_name,
                 output_dag_path, output_dag_file_name):
    """
    Generates DAG Py file based on the given DAG Jinja2 template file and the configuration yml file and write it to the
    provided output_dag_path folder with the name output_dag_file_name.

    :param input_config_yaml_path: Path to the DAG configuration input YAML file
    :param input_config_yaml_file_name: DAG configuration input yaml file name
    :param input_template_path: Path to the DAG Jinja2 Template file
    :param input_template_file_name: Input DAG Jinja2 Template file name (.j2 extension file)
    :param output_dag_path: Path for the generated DAG Py file
    :param output_dag_file_name: Name for the generated DAG Py file

    :returns: None

    :raises ValueError: when the user provided input is invalid. For example, if the output dag file name provided is not
     a .py file or the input YAML config file doesn't contain any parameters or is invalid
    """

    # Load DAG configuration input from the YAML file into Python dictionary
    if not output_dag_file_name.endswith('.py'):
        raise ValueError("Invalid output dag file name. It should be a .py extension file")

    config = yaml.load(open(input_config_yaml_path + os.path.sep + input_config_yaml_file_name), Loader=yaml.FullLoader)
    if config is None:
        raise ValueError("Invalid input configuration YML file")

    # Load input Jinja2 template
    env = Environment(loader=FileSystemLoader(input_template_path), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(input_template_file_name)

    # Write to the output Python DAG source file
    with open(output_dag_path + os.path.sep + output_dag_file_name, "w") as output_file:
        output_file.write(template.render(config))


def validate_dag(output_dag_path):
    """
    Validates the generated Python DAG file by leveraging airflow DagBag.

    :param output_dag_path: Path to the generated Python DAG file

    :returns: None

    :raises AssertionError: when there is validation error on the generated DAG files
    """
    dag_bag = DagBag(dag_folder=output_dag_path)
    if len(dag_bag.import_errors):
        print('DAG import failures. Errors: {}'.format(dag_bag.import_errors))
        raise AssertionError('DAG import failures. Errors: {}'.format(dag_bag.import_errors))


def __get_args__(input_args):
    parser = argparse.ArgumentParser(prog='airflowdaggenerator',
                                     description="Airflow DAG Generator (airflowdaggenerator.py)::")
    parser.add_argument("-config_yml_path", "--input_config_yaml_path", required=True,
                        help="Path to the DAG configuration input YAML file")
    parser.add_argument("-config_yml_file_name", "--input_config_yaml_file_name", required=True,
                        help="DAG configuration input yaml file name")
    parser.add_argument("-template_path", "--input_template_path", required=True,
                        help="Path to the DAG Jinja2 Template file")
    parser.add_argument("-template_file_name", "--input_template_file_name", required=True,
                        help="Input DAG Jinja2 Template file name (of .j2 extension file)")
    parser.add_argument("-dag_path", "--output_dag_path", required=True, help="Path for the generated Python DAG file")
    parser.add_argument("-dag_file_name", "--output_dag_file_name", required=True,
                        help="Name for the generated Python DAG file")
    return parser.parse_args(input_args)


def main():
    """
    The entry point for the Airflow DAG Generator. It orchestrates the validation of user provided inputs , generation
    of the output DAG file and the validation of the generated DAG file.

    :returns: None

    :raises ValueError: when the user provided input is invalid. For example, if the output dag file name provided is not a .py file or the input YAML config file doesn't contain any parameters or is invalid
    :raises AssertionError: when there is validation error on the generated DAG files
    """
    runtime_args = __get_args__(sys.argv[1:])
    print("Starting the Airflow DAG file Generation")
    generate_dag(runtime_args.input_config_yaml_path,
                 runtime_args.input_config_yaml_file_name,
                 runtime_args.input_template_path,
                 runtime_args.input_template_file_name,
                 runtime_args.output_dag_path,
                 runtime_args.output_dag_file_name)
    print("Successfully Generated the Airflow DAG Python file under '{0}'".format(runtime_args.output_dag_path))
    validate_dag(runtime_args.output_dag_path)
    print("Successfully Validated the generated Airflow DAG Python file")
