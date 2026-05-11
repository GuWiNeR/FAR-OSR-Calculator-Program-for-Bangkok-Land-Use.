import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import io

from calculation import calculatorareas
from data_manager import save_data
from data_regulation import far_osr_data, optional_far, far_osr_type
from fpdf import FPDF


def export_data(project_name, cal_far, cal_osr, far, osr, sel_name_data, far_osr_t, bonus):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("THSarabunPSK", "", "fonts/THSarabun.ttf", uni = True)

    pdf.set_font("THSarabunPSK", size = 30)


    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, text = f"PROJECT : {project_name}", ln = 1, align = 'c')
    
    pdf.ln(10)

    pdf.set_font("THSarabunPSK", size = 20)
    pdf.cell(200, 10, text="PROJECT INFORMATION", ln = 1)
    pdf.ln(2)

    pdf.set_font("THSarabunPSK", size = 16)
    pdf.cell(100, 10, text=f"ชื่อโครงการ : {sel_name_data[0]['name']}", ln = 1)
    pdf.cell(100, 10, text=f"เขต : {sel_name_data[0]['district']}", ln = 0)
    pdf.cell(100, 10, text=f"ขนาดที่ดิน : {sel_name_data[0]['areas']:,.2f} sq.m.", ln = 0)
    pdf.cell(100, 10, text=f"เขตสี : {sel_name_data[0]['zoning']}", ln = 1)
    pdf.cell(100, 10, text=f"รหัส : {sel_name_data[0]['sub_zoning']}", ln = 0)
    pdf.cell(100, 10, text=f"ที่ดินประเภท : {far_osr_t}", ln = 1)
    pdf.ln(10)

    pdf.set_font("THSarabunPSK", size = 20)
    pdf.cell(200, 10, text="FAR/OSR RATIO", ln = 1)
    pdf.ln(2)
    dat = pd.DataFrame(
        {"landused": [cal_far, cal_osr]},
        index=["FAR area", "OSR area"]
    )
    fig, ax = plt.subplots(figsize=(4, 4))
    dat.plot.pie(
        y="landused", ax=ax,
        colors=["#C2D6F5", "#b5c5ccff"],
        autopct='%1.2f%%',
        legend=False,
        textprops={'color': "#5a5863ff"}
    )

    plt.tight_layout()  

    pdf.set_font("THSarabunPSK", size=16)
    pdf.cell(95, 10, text=f"FAR Ratio: {far}", ln=0)
    pdf.cell(95, 10, text=f"OSR Ratio: {osr}", ln=1)
    pdf.cell(95, 10, text=f"FAR Area: {cal_far:,.2f} sq.m.", ln=0)
    pdf.cell(95, 10, text=f"OSR Area: {cal_osr:,.2f} sq.m.", ln=1)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)

    pdf.set_font("THSarabunPSK", size=14)
    pdf.image(buf, x = 50, w = 100) 
    



    if bonus:
        pdf.set_text_color(0, 128, 0) 
        pdf.cell(200, 10, text="* Applied 20% FAR Bonus", ln=1)
    
    return bytes(pdf.output())

    
def result_table(cal_far, cal_osr, far, osr, far_osr_t, bonus = False):
    type = str(far_osr_t)
    dat = pd.DataFrame(
        {"landused": [cal_far, cal_osr]}, 
        index = ["FAR area", "OSR area"],
        )
    
    fig, ax = plt.subplots(figsize=(4, 4)) 
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    plot = dat.plot.pie(y= "landused",
                        ax = ax,  
                        colors = ["#C2D6F5", "#b5c5ccff"],
                        autopct='%1.2f%%',
                        legend = False,
                        textprops={'color':"#5a5863ff"})
    plt.tight_layout()                   
    st.pyplot(fig, clear_figure=True, transparent=True)
    col1, col2 = st.columns(2)

    far_new = far + (far*(20/100))
    difference = far_new - far
    display_data = far_new if bonus == True else far 
    result = difference if bonus == True else far - far

    with col1:
        st.metric(label="FAR ratio", value= display_data, delta = round(result, 2))
        if bonus == True:
            st.write(f"FAR : {far} ")
            st.write(f"FAR bonus (20%) : {far_new}")
            st.write(" ")
        else:
            st.write(f"FAR area")
            st.space("medium")
        st.subheader(f"{cal_far:,.2f} sq.m.")

    with col2:
        st.metric(label="OSR ratio", value= osr, delta = 0)
        st.write(f"OSR : {osr}")
        st.space("medium")
        st.subheader(f"{cal_osr:,.2f} sq.m.")

    return {
        "calculated_far" : cal_far,
        "calculated_osr" : cal_osr,
        "ratio_show" : display_data,
        "difference" : result,
        "building_type" : type
    }

def calculate_data():

    #--------------- show information --------------------------

    data = st.session_state.project_data

    st.subheader("calculate data".upper())

    data_list = ([p['name'] for p in data])
    if not data_list:
        st.text("No data")
    else:
        sel_data = st.selectbox("Selected your project", options = data_list)

        st.text("Project information")
        sel_name_data = [p for p in data if p['name'] == sel_data]

        display = pd.DataFrame(sel_name_data).style.format(subset=['areas'], formatter = "{:,.2f}")
        st.table(display)

        data_detail = sel_name_data[0]['sub_zoning']
        far_osr_rule = far_osr_data.get(data_detail)

        far = far_osr_rule['far']
        osr = far_osr_rule['osr']

        data_type_detail = sel_name_data[0]['zoning']
        far_osr_t = far_osr_type.get(data_type_detail)


        st.write(f"ที่ดินประเภท : {far_osr_t }")


        st.divider()

        #------------- FAR BONUS --------------------------

        st.subheader("Far bonus".upper())
        
        with st.expander("FAR bonus lists check"):
            bonus = False
            for info in optional_far:
                checked = st.checkbox(info)
                if checked:
                    bonus = True
                

        st.text ("หมายเหตุ : ทุกแบบรวมกัน เพิ่ม FAR ได้ไม่เกินร้อยละ 20")

        st.divider()

        #---------------------calculation---------------------

        if st.button("calculate", use_container_width=True, type="primary"):
            #far calculation 

            data_dict = sel_name_data[0]
            cal_data = calculatorareas(data_dict)
            cal_far = cal_data.calculate_far(bonus)
            cal_osr = cal_data.calculate_osr(bonus)

        
        #-----------------show result------------------------

            result = result_table(cal_far, cal_osr, far, osr, far_osr_t, bonus)
            st.divider()

            #------------ data management ----------------

            pdf_data = export_data(
                project_name = sel_data,
                cal_far = result['calculated_far'],
                cal_osr = result['calculated_osr'],
                far = far,
                osr = osr,
                bonus = bonus, 
                sel_name_data = sel_name_data,
                far_osr_t = far_osr_t,
            )
            st.download_button(
                label = "export data to PDF",
                data = pdf_data,
                file_name = f"FAR/OSR_{sel_data}.pdf",
                icon = ":material/download:",
                )
            




        


            


 