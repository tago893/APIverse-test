model_backend = 'datastore'
if model_backend == 'datastore':
    from .model_datastore import UserModel
else:
    raise ValueError("No appropriate databackend configured. ")

appmodel = UserModel()

def get_model():
    return appmodel
