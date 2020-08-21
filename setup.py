from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.md') as history_file:
#     history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'apache-airflow', 'psycopg2', 'PyYAML', 'jinja2<2.11.0,>=2.10.1',
]

test_requirements = [
    'pytest', 'pytest-pep8', 'pytest-cov'
]

setup(
    name='airflowdaggenerator',
    version='0.0.2',
    description="Dynamically generates and validates Python Airflow DAG file based on a Jinja2 Template and a YAML "
                "configuration file to encourage code re-usability",
    long_description=readme,
    # long_description=readme + '\n\n' + history,
    author="Felix K Jose",
    author_email='felixkjose@gmail.com',
    url='https://github.com/FelixKJose/AirflowDAGGenerator',
    packages=["airflowdaggenerator"],
    entry_points={
        "console_scripts": ['airflowdaggenerator = airflowdaggenerator.airflowdaggenerator:main']
    },
    install_requires=requirements,
    license="Apache-2.0 License",
    zip_safe=False,
    keywords='airflow, dynamic, dag, generator, jinja2',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <4',
    tests_require=test_requirements
)
