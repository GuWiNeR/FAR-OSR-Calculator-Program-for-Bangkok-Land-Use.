import streamlit as st 

from streamlit_option_menu import option_menu
from data_manager import load_data
from content import project, calculate_data, comparison_data 
from data_regulation import far_osr_type, district_zoning_rules

if 'project_data' not in st.session_state:
    st.session_state.project_data = load_data()



#-----------user interface----------------------------------

st.set_page_config(
    page_title = "site data analysis".upper(), 
    page_icon = "🗺"
    )


with st.sidebar:
    selected = option_menu(
        menu_title = "Main menu",
        options = ["Home", "Project", "Calculate data","Comparison data"],
        icons = ["house-fill", "file-plus","activity", "bar-chart-fill"],
        menu_icon = ["list"],
        default_index = 0,
        orientation="vertical",
        styles={
        "container": {"padding": "0!important", "background-color": "#ffffff00"},
        "icon": {"color": "#7B7373", "font-size": "20px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#000000C5"},
    }
    )

if selected == "Home":
    st.header("site data analysis".upper())
    st.subheader("FAR/OSR Calculator Program for Bangkok Land Use.")
    st.divider()
    st.write("โปรแกรมนี้ถูกออกแบบเพื่อวิเคราะห์ศักยภาพของที่ดินในเขตกรุงเทพฯ โดยการคำนวณค่า Floor Area Ratio (FAR) เเละ Open Space Ratio (OSR) ตามกฏหมายผังเมืองของกรุงเทพมหานคร ผู้ใช้สามารถป้อนรายละเอียดโครงการ คำนวณค่า FAR และ OSR เเละเปรียบเทียบโครงการต่างๆได้")
    st.markdown('''
    :red[***โปรแกรมนี้ถูกออกแบบเพื่อประเมินค่า FAR และ OSRเบื้องต้นเท่านั้น กรุณาตรวจสอบผลลัพธ์กับแหล่งข้อมูลทางการก่อนที่จะตัดสินใจตามผลลัพธ์ที่ได้]''')
    with st.expander("English translation"):
        st.write("This program is designed to calculate the Floor Area Ratio (FAR) and Open Space Ratio (OSR) for land use projects in Bangkok. It allows users to input project details, calculate FAR and OSR based on zoning regulations, and compare different projects.")
        st.markdown('''
                    :red[***This program is developed for educational purposes and is not intended for commercial use. The calculations are based on the regulations provided by the Bangkok Metropolitan Administration and may not reflect the most current zoning laws. Users should verify the results with official sources before making any decisions based on the calculations.]
                    ''')

    st.divider()

    st.subheader('What is FAR ?')
    st.text("FAR หรือ Floor Area Ratio คืออัตราส่วนของพื้นที่ใช้สอยทั้งหมดของอาคารเทียบกับขนาดของที่ดินที่สร้างอยู่ โดยคำนวณจากคือ อัตราส่วนพื้นที่อาคารรวมต่อพื้นที่ดิน เป็นตัวกำหนดว่าจะสามารถสร้างอาคารได้ขนาดเท่าไหร่ โดยมีวิธีคำนวณคือ")
    st.markdown('<p style="text-align: center; font-weight: 24px;">ค่า FAR X ขนาดพื้นที่ดิน = พื้นที่อาคารสูงสุดที่สร้างได้</p>', unsafe_allow_html=True)
    st.text("การมี FAR สูงหมายถึงการพัฒนาที่มีความหนาแน่นมากขึ้น ในขณะที่ FAR ต่ำหมายถึงการพัฒนาที่มีความหนาแน่นน้อยลง")
    st.subheader('What is OSR ?')
    st.text("OSR หรือ Open Space Ratio คืออัตราส่วนของพื้นที่เปิดโล่งเทียบกับพื้นที่ใช้สอยทั้งหมดของอาคาร โดยมีวิธีคำนวณคือ")
    st.markdown('<p style="text-align: center; font-weight: 24px;">ค่า OSR x พื้นที่อาคาร = พื้นที่เปิดโล่งบนที่ดิน</p>', unsafe_allow_html=True)
    st.text("การหารพื้นที่เปิดโล่งด้วยพื้นที่ใช้สอยทั้งหมดของอาคาร การมี OSR สูงหมายถึงมีพื้นที่เปิดโล่งมากขึ้น ในขณะที่ OSR ต่ำหมายถึงมีพื้นที่เปิดโล่งน้อยลง")
    with st.expander("English translation"):
        st.text("FAR (Floor Area Ratio) is a measure of the total floor area of a building in relation to the size of the land it is built on. It is calculated by dividing the total floor area of the building by the area of the land. A higher FAR indicates a denser development, while a lower FAR indicates a less dense development.")
        st.text("OSR (Open Space Ratio) is a measure of the amount of open space in relation to the total floor area of a building. It is calculated by dividing the area of open space by the total floor area of the building. A higher OSR indicates more open space, while a lower OSR indicates less open space.")
    
    st.divider()
    st.subheader("How to use this program?")
    st.text("1. ไปที่ส่วน 'Project' เพื่อสร้างโครงการใหม่โดยกรอกชื่อโครงการ และข้อมูลโครงการ ตรวจสอบรายละเอียดโครงการให้ถูกต้องและบันทึกข้อมูล")
    st.text("2. ไปที่ส่วน 'Calculate data' เพื่อเลือกโครงการและคำนวณค่า FAR และ OSR ตามกฎหมายผังเมืองกรุงเทพฯ")
    st.text("3. ในส่วน 'Comparison data' สามารถเลือกหลายโครงการเพื่อเปรียบเทียบค่า FAR และ OSR ทั้งยังสามารถเลือกที่จะใช้โบนัส FAR สำหรับการเปรียบเทียบเพิ่มเติมได้")
    with st.expander("English translation"):
        st.text("1. Go to the 'Project' section to create a new project by entering the project name and project details. Make sure to select the correct zoning for your project and save the data.")
        st.text("2. After creating a project, go to the 'Calculate data' section to select your project and calculate the FAR and OSR values based on the zoning regulations.")
        st.text("3. In the 'Comparison data' section, you can select multiple projects to compare their FAR and OSR values. You can also choose to apply a FAR bonus for additional comparison.")

    st.divider()

    st.subheader("Metric")
    col1, col2, col3 = st.columns(3)
    with col1:
        if not st.session_state.project_data:
            st.text("No project data available.")
        else:
            total_projects = len(st.session_state.project_data)
            st.metric(label = "Total projects", value = total_projects)
            with st.expander("Project information"):
                for project in st.session_state.project_data:
                    st.text(f"{project['name']}")
    with col2:
        color_name = list(far_osr_type.keys())
        color_zoning = len(color_name)
        color_list = ["#c2c500", "#ff9100", "#5C432F", "#ff0000", "#ff00dd", "#8c00ff", "#999999", "#008006", "#009fb4"]
        st.metric(label = "Color zoning", value = color_zoning)
        with st.expander("Color zoning information"):
            for color in color_name:
                st.markdown(
                    f'<span style="color:{color_list[color_name.index(color)]}; font-size: 16px;">{color} : {far_osr_type[color]}</span>',
                    unsafe_allow_html=True
                    )
    with col3:
        district_number = len(district_zoning_rules)
        st.metric(label = "Districts", value = district_number)
        with st.expander("District information"):
            for district, zoning in district_zoning_rules.items():
                st.text(f"{district}")

    st.divider()
    st.subheader("About me")
    st.write("สวัสดีทุกๆท่าน เราเป็นนักศึกษาจบใหม่จากคณะสถาปัตยกรรมศาสตร์ ที่มีความสนใจในการเขียนโปรแกรม โดยนำองค์ความรู้เบื้องต้นเกี่ยวกับกฏหมายผังเมืองกรุงเทพมหานครมาพัฒนาโปรแกรมวิเคราะห์ข้อมูลที่ดินในกรุงเทพฯ เพื่อช่วยให้ผู้ใช้สามารถคำนวณค่า FAR และ OSR ได้อย่างง่ายดายและรวดเร็ว โดยอ้างอิงข้อมูลการแบ่งเขตของกรุงเทพมหานครเป็นพื้นฐานในการคำนวณ หากมีคำถามหรือข้อเสนอแนะเกี่ยวกับโปรแกรมนี้ สามารถเข้ามาพูดคุยกันได้เลยนะคะ")
    with st.expander("English translation"):
        st.write("Hello everyone, I am a recent graduate from the Faculty of Architecture with an interest in programming. I have developed this program to analyze land data in Bangkok by utilizing basic knowledge of Bangkok's zoning regulations. This program allows users to easily and quickly calculate FAR and OSR values based on the zoning information of Bangkok. If you have any questions or suggestions about this program, feel free to reach out and discuss with me.")

if selected == "Project":
    project.create_project()

if selected == "Calculate data":
    calculate_data.calculate_data()

if selected == "Comparison data":
    comparison_data.comparison()

