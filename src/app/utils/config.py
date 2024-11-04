import yaml
import os

def load_config(config_name='settings.yaml'):
    """Charge le fichier de configuration spécifié.

    Args:
        config_name (str): Nom du fichier de configuration.

    Returns:
        dict: Dictionnaire contenant les configurations.
    """
    config_path = os.path.join('config', config_name)
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
