from setuptools import setup
from setuptools import find_packages

setup(name='mlb_analytics',
        version='0.10',
        description='A python package that provides core functionality for advanced pitching and hitting analytics of major league baseball play by play datasets.',
        author='Blake A. Marshall',
        author_email='blake120289@yahoo.com',
        license='All rights reserved by Oracle.',
        # Specify which Python versions you support. In contrast to the
        # 'Programming Language' classifiers above, 'pip install' will check this
        # and refuse to install the project if the version does not match. See
        # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
        python_requires='>=3.9',
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src"),
        zip_safe=False,
        install_requires=['numpy','pandas','sqlalchemy','pyodbc','ipykernel'],
            ## Note: the space between the @ are acutally necessary!
            #'<some-gitlab-package>  @  git+ssh://git@<package-url-with-slashes>.git@master',
        extras_require={
            'dev': [
                'pytest',
                'mypy',
                'pylint',
                'coverage',
                'python-dotenv',
                'tox-conda',
                'ipykernel',
                'matplotlib',
                'plotnine',
                'seaborn',
            ]
        }
)