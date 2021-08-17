from setuptools import find_packages, setup
import os

here = os.path.abspath(os.path.dirname(__file__))
exec(open(os.path.join(here, 'domain_classifier/_version.py')).read())

setup(
    name='domain_classifier',
    version=__version__,
    packages=find_packages(),
    description='Domain threat prediction model for phishing',
    url='https://github.com/IronNetCybersecurity/iron-predict-models',
    install_requires=[
        'cloudpickle',
        'h5py==2.9.0',
        'Keras==2.2.4',
        'numpy==1.18.2',
        'pandas',
        'progressbar',
        'pyahocorasick',
        'scikit-learn==0.20.3',
        'scipy==1.4.1',
        'tensorflow==1.15.0',
        'tldextract',
        'urllib3',
        # Internal ironnet projects
        'phishing_common==0.1.1_dev2'
    ],
    include_package_data=False
)
