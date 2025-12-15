from setuptools import setup, find_packages

setup(
    name="zwutils",
    version="0.1.0",
    description="Lightweight Python library for payroll and salary slip generation",
    author="Munyaradzi Chirove",
    author_email="chirovemunyaradzi@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Jinja2>=3.0",
        "WeasyPrint>=59.0",
    ],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
