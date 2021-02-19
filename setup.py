import setuptools

with open("README.md", "r", encoding="utf-8") as file_handle:
    long_description = file_handle.read()

setuptools.setup(
    name="ssh-session-manager",
    version="0.0.1",
    author="SYSCON International",
    author_email="dev@syscon-intl.com",
    description="Execute commands on multiple remote SSH sessions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Syscon-Plantstar/ssh-session-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "paramiko==2.7.2"
    ]
)
