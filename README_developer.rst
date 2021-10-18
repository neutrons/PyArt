**********************
PyArt Developer README
**********************


Set up Github Action (Try and Error)
####################################

Refer to: https://docs.github.com/en/actions/quickstart

1. Create a `.github/workflows` directory in the repository
2. Create file `.github/workflows/github-action-pyart.yml`


Set up developing environment
#############################

.. code-block:: shell

   $ conda create -n pyart_test python=3.7
   $ conda install -c mantid/label/nightly mantid-framework=6 --file requirements.txt --file requirements_dev.tx
   $ conda install -c anaconda pyqt


