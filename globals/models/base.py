from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

Base = declarative_base()

metadata = MetaData()

loaded_models = {
}

## get model, e.g: "users.Users": "users/sa_model.py" with class: "Users"
def get_model(model_):

    if model_ in loaded_models:
        return loaded_models[model_]

    current =  __name__.split(".")
    path_ = current[0:-1] 
    model = model_.split(".")
    path_ += (model[0], 'sa_model')

    ## Get module MODULE/sa_model: 
    mod = __import__(".".join(path_))
    for i in path_[1:]:
        mod = getattr(mod, i)

    ## Get model by module attr:
    model__ = getattr(mod, model[1])

    ## Make new (SA)class of MODEL, Base:
    ##cls_ = type(model[1], (model__, Base), {})
    cls_ = model__
    loaded_models[model_] = cls_
    return get_model(model_)

