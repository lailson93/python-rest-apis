[![Build Status](https://dev.azure.com/lailson93/Azevedo/_apis/build/status/lailson93.python-sample-vscode-flask-tutorial?branchName=master)](https://dev.azure.com/lailson93/Azevedo/_build/latest?definitionId=1&branchName=master)

# python-rest-apis
Repositório voltado para estudos com REST APIs para Python


### Conda environment basic commands reference

Desativar o conda base environment como default
```
conda config --set auto_activate_base false
```

```
conda env list
conda create --name virtenv1 python=3.6
conda activate virtenv1

conda install jupyter notebook
jupyter notebook

conda deactivate

conda remove --name virtenv1 --all
conda env remove -n virtenv1

## lista todos os pacotes intalados no ambiente
pip freeze

### conda generate packages requirements file:
conda list -e > req.txt

### conda generate env file
conda env export > env.yml

#For other person to use the environment
conda env create -f env.yml
```

References

udemy course: https://www.udemy.com/course/rest-apis-com-python-e-flask/
