import json
import streamlit as st

file_path = "input_data.json"

# load data detail 
def load_data():
    try:
        with open(file_path , "r", encoding="UTF-8") as f:
            temp_data = json.load(f)
            return temp_data

    except FileNotFoundError as e:
        return []

    except (json.JSONDecodeError, ValueError) as e:
        st.warning(f"Error : {e}")
        return []

    except Exception as e:
        st.warning(f"Error : {e}")
        return[]
    
# save data detail 
def save_data():
    try:
        with open(file_path , "w", encoding="UTF-8") as f:
            json.dump(st.session_state.project_data , f, ensure_ascii=False, indent=2)
            return True

    except PermissionError as e:
        st.warning(f"Error : {e}")
        return False
    
    except TypeError as e:
        st.warning(f"Error : {e}")
        return False
    except Exception as e:
        st.warning(f"Error : {e}")
        return False    

