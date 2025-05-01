from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function reads a requirements file and returns a list of packages.
    It ignores comments and empty lines.
    """
    requirements:List[str] = []

    try:
        with open('requirements.txt', 'r') as file:
            # Read the file
            lines = file.readlines()
            # Process the lines
            for line in lines:
                requirement = line.strip()
                ## Ignore empty lines, comments and -e .
                if requirement and (requirement != '-e .' and not requirement.startswith('#')):
                    requirements.append(requirement)
    except FileNotFoundError:
        print(f"Warning: requirements.txt not found.")

    return requirements

setup(
    name='Network Security System',
    version='0.0.1',
    author='Zenith369',
    author_email='prasham.work@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
)