from setuptools import setup, find_packages

setup(
    name="surprise_travel",
    version="0.1.0",
    packages=find_packages(include=['surprise_travel*']),
    install_requires=[
        "crewai[tools]>=0.152.0",
        "crewai-tools>=0.58.0",
    ],
    entry_points={
        'console_scripts': [
            'surprise_travel=surprise_travel.main:run',
            'train=surprise_travel.main:train',
        ],
    },
)
