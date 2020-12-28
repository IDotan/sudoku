from setuptools import find_packages, setup

setup(
    name='Sudoku Game',
    author="Itai Dotan",
    packages=find_packages(),
    description="Sudoku game with random boards and user entered board",
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'pygame'
    ],
    extras_require={"test": "pytest"},
)
