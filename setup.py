from setuptools import setup, find_namespace_packages

setup(
    name="ah_user_memory",
    version="1.0.0",
    packages=find_namespace_packages(include=["ah_user_memory", "ah_user_memory.*"]),
    install_requires=[
        'nanoid',
        'loguru'
    ],
    author="Assistant",
    author_email="assistant@example.com",
    description="Persistent user memory storage that appears in system messages",
    keywords="memory,plugin",
    package_dir={"": "src"}
)