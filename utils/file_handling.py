import os
import streamlit as st
from typing import List

UPLOAD_DIR = "data/uploads"

def save_uploaded_files(uploaded_files, project_id, room_id) -> List[str]:
    saved_paths = []
    target_dir = os.path.join(UPLOAD_DIR, str(project_id), str(room_id))
    os.makedirs(target_dir, exist_ok=True)
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(target_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
        
    return saved_paths
