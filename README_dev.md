conda create -n pyart_test python=3.7
conda install -c mantid/label/nightly mantid-framework=6 --file requirements.txt --file requirements_dev.tx
conda install -c anaconda pyqt
