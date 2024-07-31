from setuptools import find_packages, setup

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='pixelperfect',
    version='0.0.4',
    python_requires='>=3.10',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(include=['pixelperfect', 'pixelperfect.*']),

    entry_points={
        'console_scripts': [
            'pixelperfect = pixelperfect.__main__:main'
        ]
    }
)
