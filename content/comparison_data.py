import streamlit as st 
import pandas as pd 

from calculation import calculatorareas

def display_comparison(bonus = False):
    chart_display = []
    for data in st.session_state.compare_lists:
        cal = calculatorareas(data)
        chart_display.append({
            "name" : data['name'],
            "far" : cal.calculate_far(bonus),
            "osr" : cal.calculate_osr()
        })
    
    df_compare = pd.DataFrame(chart_display)

    st.bar_chart(df_compare.set_index('name')[['far', 'osr']], use_container_width= True, stack= False)


def comparison():

    if 'compare_lists' not in st.session_state:
        st.session_state.compare_lists = []

    data = st.session_state.project_data

    st.subheader("comparison data".upper())

    data_lists = [p['name'] for p in data]
    
    if not data_lists:
        st.write("No data")
    
    else:

        sel_data = st.selectbox("selected your project", options = data_lists)
        info = next((p for p in data if p['name'] == sel_data), None)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Add to compare"):
                if any(info['name'] == p['name'] for p in st.session_state.compare_lists):
                    st.warning("This project is already in the compare list.")
                else:
                    st.session_state.compare_lists.append(info)
                    st.rerun()


        if st.checkbox("Add FAR bonus"):
            bonus = True
        else:
            bonus = False

        if not st.session_state.compare_lists:
            st.write("No data to compare")
        else:
            df = pd.DataFrame(st.session_state.compare_lists)
            st.dataframe(df.style.format(
                subset=['areas'], 
                formatter = '{:,.2f}'), 
                use_container_width = True
                )
            
            if calculatorareas(info).area <= 0:
                st.warning("Area must be greater than zero to perform calculations.")
            else:
                display_comparison(bonus)

        with col2:
            if st.button("Clear compare list"):
                st.session_state.compare_lists = []
                st.rerun()


        


    
    