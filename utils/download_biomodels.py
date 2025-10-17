

import os
from bioservices import BioModels
from tqdm import tqdm

# Initialize BioModels service
bio = BioModels()

save_dir = "biomodels"
os.makedirs(save_dir, exist_ok=True)



mdls = sorted ([(mdl["id"],mdl) for mdl in bio.get_all_models() if mdl["format"] == "SBML"])

# Retrieve all curated model IDs

# Directory to save models
# Function to download a model
def download_model(mdlid, mdlfile):
    mdl_filename = f"{mdlid}.xml"
    file_path = os.path.join(save_dir, mdl_filename)
    #sbml_content = bio.get_model_files(model_id, frmt="xml")
    #sbml_content = bio.get_model_download(model_id)
    sbml_content = bio.get_model_download(mdlid, filename=mdlfile, output_filename=file_path)
    #with open(file_path, "w") as file:
    #    file.write(sbml_content)




# Download each model
for mdlid,mdl in tqdm(mdls):
    desc = bio.get_model(mdlid)
    files = desc["files"]
    if mdl["format"] == "SBML":
        print ("downloading: ", mdl["id"])
        download_model(mdl["id"], files["main"][0]["name"])
