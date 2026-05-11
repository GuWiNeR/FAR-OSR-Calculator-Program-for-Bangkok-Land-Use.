import streamlit as st
import pandas as pd 
from data_manager import save_data
from data_regulation import regulation_type_districts, district_zoning_rules

@st.dialog("New project")
def addproject():

    data = st.session_state.project_data

    project_name = st.text_input("Name your project","name project")
    col1, col2 = st.columns(2)

    with col1:
        info_disricts = list(district_zoning_rules.keys())
        districts = st.selectbox("District", options = info_disricts )
        areas = st.number_input("Site area (sq.m)", step=10.00, min_value=0.00)
    with col2:
        zoning = st.selectbox("Zoning map", options = district_zoning_rules[districts])
        sub_zoning = st.selectbox("Sub zoning", options = regulation_type_districts[zoning])
    
    if st.button("Save Data", use_container_width=True, type = "secondary" ):

        if any(p['name'] == project_name for p in data):
            st.error("Name have already taken!")

        else:
            project_create = {
                "name" : project_name,
                "district" : districts,
                "areas" : areas,
                "zoning" : zoning,
                "sub_zoning" : sub_zoning
            }
            data.append(project_create)
            save_data()
            st.success("save file successfully".capitalize())
            st.rerun()

@st.dialog("Edit project")
def editproject(selected):

    data = st.session_state.project_data
    info_disricts = list(district_zoning_rules.keys())

    sel_data = data[selected]

    st.table(sel_data)

    project_name = st.text_input("Edit your name", value=sel_data['name'])
    
    col1, col2 = st.columns(2) 

    with col1:

        indx_list = list(district_zoning_rules)

        d_index = indx_list.index(sel_data['district']) if sel_data in indx_list else 0 
        districts = st.selectbox("District", options = info_disricts , index = d_index)

        areas = st.number_input("Site area (sq.m)", step = 10.00, min_value = 0.00 , value = float(sel_data['areas']))

    with col2:
        #regulation type districts management 
        zoning_list = list(regulation_type_districts.keys())
        sel_zoning = sel_data.get('zoning')

        #change zone 
        zone_idx = zoning_list.index(sel_zoning) if sel_zoning in zoning_list else 0
        zoning = st.selectbox("Zoning map", options = district_zoning_rules[districts] , index = zone_idx)

        #change sub_zone
        sub_option = regulation_type_districts.get(zoning, ["N/A"])
        sel_subzoning = sel_data.get('sub_zoning')
        sub_zone_idx = sub_option.index(sel_subzoning) if  sel_subzoning in sub_option else 0 

        sub_zoning = st.selectbox("Sub zoning", options = sub_option, index = sub_zone_idx)
    
    if st.button("Save Data", use_container_width=True, type = "secondary" ):

        if any(p['name'] == project_name for i, p in enumerate(data) if i != selected):
            st.error("Name have already taken!")

        else:
            project_new = {
                "name" : project_name,
                "district" : districts,
                "areas" : areas,
                "zoning" : zoning,
                "sub_zoning" : sub_zoning
            }
            st.session_state.project_data[selected] = project_new
            save_data()
            st.success("Edit file successfully".capitalize())
            st.rerun()

@st.dialog("reset all project")
def reset_project():
    st.warning("All data will reset permanently!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("confirm", use_container_width = True, type = "primary"):
            st.session_state.project_data.clear()
            save_data()
            st.success("reset file successfully".capitalize())
            st.rerun()
    with col2:
        if st.button("cancel", use_container_width = True):
            st.rerun()

#---------------------- User interface ----------------------- 
#---------input--------------
def create_project():

    data = st.session_state.project_data
    col1, col2 = st.columns([0.7,1])
    with col2:
        st.subheader("project".upper())
    st.divider()

#------------------- new project 

    st.text ("Add project".upper()) 

    if st.button("+ Create New", use_container_width = True,type = "secondary"):
        addproject()

#------show list

    st.text ("Project lists".upper())
    if not data:
        st.table()
    else:
        display = pd.DataFrame(data)
        st.dataframe(display.style.format(subset=['areas'], formatter = "{:,.2f}"))


#---------------edit------------

    with st.expander("Edit project"):

        name = [p['name'] for p in data]

        if not name:
            st.text("empty")
        else:
            selected = st.selectbox("Select project", name)
            sel_index = name.index(selected)

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Edit project", use_container_width = True):
                    editproject(sel_index)


            with col2:
                if st.button("Delete", use_container_width=True):
                    st.session_state.project_data.pop(sel_index)
                    save_data()
                    st.rerun()

            with col3:
                if st.button("Reset all data", use_container_width=True):
                    reset_project()



    st.divider()

