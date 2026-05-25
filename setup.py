# To ensure that project is installed in editable mode, we need to add -e . in the requirements.txt file. This will allow us to make changes to the code and see the changes reflected without having to reinstall the package every time.
# The -e and requirements .txt file is used to specify dwhich dependencies to install
from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
    '''
    This function will return the list of requirements mentioned in the requirements.txt file
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
    
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name='ml_project',
    version='0.0.1',
    author='Ashutosh Trivedi',
    author_email='ashutoshtrivedi9632@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)