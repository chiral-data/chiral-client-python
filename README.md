# chiral-client-python: Python client for Chiral Computing Cloud API

## Versions
- 0.3.2 
    - (client version 0.3.1): new scripts example of gromacs
    - bug fix, windows directory seperators for upload_files & download_files
- 0.3.1: bug fix, ftp connection long idle
- 0.3.0: for chiral service V2
- 0.2.1: ReCGen for virtual molecular library; Large language model LLama2 from Meta;
- 0.1.0: gromacs

## Requirements for Running Examples
- python >= 3.12
- numpy, matplotlib, grpcio, jupyter

## Installation
- `conda install -c conda-forge grpcio protobuf` not valid any more, use `python -m pip install grpcio protobuf`
- `pip install notebook`

## Publish
```bash
# under virtual environment "chiral-dev"
python setup.py bdist_wheel
twine upload dist/*
```

## Roadmap

##  TODO
