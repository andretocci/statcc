from setuptools import setup


setup(
    name='minhas_hipoteses',
    version='0.0.2',
    description='Estudos de Estatistica',
    long_description='long_description',
    long_description_content_type="text/markdown",
    author='Andre Tocci',
    author_email='andrerussi002@gmail.com',
    url='https://github.com/andretocci/statcc',
    packages=setuptools.find_packages(),
    #package_dir={'minhas_hipoteses': 'stacc/minhas_hipoteses'},
    #package_data={'minhas_hipoteses': ['stacc/minhas_hipoteses/*.py']},
    install_requires=['numpy', 'scipy.stats' ],
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)