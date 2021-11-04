from setuptools import setup, find_packages

setup(
    name="messenger",
    platforms="all",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "aiohttp",
        "pydantic",
        "SQLAlchemy",
        "psycopg2-binary",
        "alembic",
        "asyncio"

    ],
    entry_points={
        'console_scripts': [
            'messenger-api = messenger:main'
        ]
    },
)