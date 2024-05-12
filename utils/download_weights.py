import os
import requests


def check_and_download_files(model_base_path):
    """
    Check the existence of necessary model files and download them if they are not found.

    Parameters:
    model_base_path (str): Base directory where model files are stored.
    """
    necessary_files = {
        "gb_model.pkl": "https://o365ku-my.sharepoint.com/:u:/g/personal/kritt"
                        "in_set_live_ku_th/ER9rWF3MtZJDrtm_MpdxEmQBJbUNRQaB9FC"
                        "edepFMTHK-A?download=1",
        "scaler_temp_humid.pkl": "https://o365ku-my.sharepoint.com/:u:/g/perso"
                                 "nal/krittin_set_live_ku_th/EY_VySuygpVLqAWsY"
                                 "XSS1qcBxocc1umhGqYUmDyGgtfp_A?download=1",
        "scaler_other.pkl": "https://o365ku-my.sharepoint.com/:u:/g/personal/k"
                            "rittin_set_live_ku_th/ESHbQ1ssK9BAsFe_gbLhjqEBYIi"
                            "_X4j9j4vRF7P3VDaeRw?download=1",
        "best.pt": "https://o365ku-my.sharepoint.com/:u:/g/personal/krittin_se"
                   "t_live_ku_th/EbZbmlVxxL1JmbF28OqrWu4BGTeu2sk7Fzo6AFxczmMav"
                   "Q?download=1",
        "yolov9c.pt": "https://o365ku-my.sharepoint.com/:u:/g/personal/krittin"
                      "_set_live_ku_th/EWk21aJG3elNls57R037YfUBhVIOCX4Og7gtcqo"
                      "CzT-UYA?download=1",
        "sam_vit_b_01ec64.pth": "https://o365ku-my.sharepoint.com/:u:/g/person"
                                "al/krittin_set_live_ku_th/EUEUdHFzPv5KvtvUlY2"
                                "dTXMBbvw66EoR_LQXPBJVfl0HLg?download=1"
    }

    for file, url in necessary_files.items():
        full_path = os.path.join(model_base_path, file)
        if not os.path.exists(full_path):
            print(f"{file} not found. Downloading from URL...")
            response = requests.get(url)
            response.raise_for_status()
            with open(full_path, 'wb') as f:
                f.write(response.content)
            print(f"{file} downloaded successfully.")
