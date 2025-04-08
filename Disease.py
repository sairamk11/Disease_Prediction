import streamlit as st
import pickle
import pandas as pd
import base64

def set_background_image_local(image_path):
    with open(image_path, "rb") as file:
        data = file.read()
    base64_image = base64.b64encode(data).decode("utf-8")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-repeat: repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background_image_local(r"BG d2.jpg")  # Replace with your image path


# Load models
@st.cache_resource
def load_model(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

# Dropdown options
tabs = ["Select Model", "Parkinson's Prediction 🧠", "Liver Prediction 🩸", "Kidney Prediction 💊"]
selected_tab = st.sidebar.selectbox("Choose a Health Prediction Model", tabs)

# Load models
parkinson_model = load_model('Parkinson.pkl')
liver_model = load_model('Indianliverpatient.pkl')
kidney_model = load_model('Kidneyprediction.pkl')

# App configuration
st.title("Health Prediction App 🩺")
st.subheader("Please select a model to predict 🔎")
st.sidebar.title("Navigation")
st.sidebar.write("Use this sidebar to navigate between different health prediction models.")
st.sidebar.write("Each tab provides a form to input necessary data for predictions.")
st.sidebar.markdown("---")

# Add sidebar info for each model
st.sidebar.subheader("Models Information")
st.sidebar.write("- **Parkinson's Prediction**: Predict the likelihood of Parkinson's disease based on vocal features.")
st.sidebar.write("- **Liver Patient Prediction**: Identify potential liver disease in Indian patients using clinical data.")
st.sidebar.write("- **Kidney Prediction**: Assess the risk of kidney disease from lab test results.")
st.sidebar.markdown("---")

if selected_tab == "Parkinson's Prediction 🧠":
    st.header("Parkinson's Disease Prediction 🧠")
    st.write("Enter the required details to predict Parkinson's disease.")

    # Input fields for 22 features
    fo = st.number_input("Enter MDVP:Fo(Hz) - Average vocal fundamental frequency", value=None, step=0.1)
    fhi = st.number_input("Enter MDVP:Fhi(Hz) - Maximum vocal fundamental frequency", value=None, step=0.1)
    flo = st.number_input("Enter MDVP:Flo(Hz) - Minimum vocal fundamental frequency", value=None, step=0.1)
    jitter_percent = st.number_input("Enter Jitter(%)", value=None, step=0.001)
    jitter_abs = st.number_input("Enter Jitter(Abs)", value=None, step=0.00001)
    rap = st.number_input("Enter Relative amplitude perturbation", value=None, step=0.001)
    ppq = st.number_input("Enter Five-point period perturbation quotient", value=None, step=0.001)
    ddp = st.number_input("Enter Difference of perturbation", value=None, step=0.001)
    shimmer = st.number_input("Enter Shimmer", value=None, step=0.001)
    shimmer_db = st.number_input("Enter Shimmer(dB)", value=None, step=0.001)
    apq3 = st.number_input("Enter - Three-point amplitude perturbation quotient", value=None, step=0.001)
    apq5 = st.number_input("Enter - Five-point amplitude perturbation quotient", value=None, step=0.001)
    apq = st.number_input("Enter amplitude perturbation quotient", value=None, step=0.001)
    dda = st.number_input("Enter - Difference of amplitude perturbation", value=None, step=0.001)
    nhr = st.number_input("Enter - Noise-to-harmonics ratio", value=None, step=0.001)
    hnr = st.number_input("Enter - Harmonics-to-noise ratio", value=None, step=0.1)
    rpde = st.number_input("Enter - Recurrence period density entropy", value=None, step=0.001)
    dfa = st.number_input("Enter - Detrended fluctuation analysis", value=None, step=0.001)
    spread1 = st.number_input("Enter Spread1 - Spread of frequency", min_value=-100.0, step=0.1)
    spread2 = st.number_input("Enter Spread2 - Spread of frequency", value=None, step=0.1)
    d2 = st.number_input("Enter - Correlation dimension", value=None, step=0.001)
    ppe = st.number_input("Enter - Pitch period entropy", value=None, step=0.001)

    # Predict button
    if st.button("Predict Parkinson's Disease"):
        input_data = [[fo, fhi, flo, jitter_percent, jitter_abs, rap, ppq, ddp, shimmer,
                       shimmer_db, apq3, apq5, apq, dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe]]
        try:
            prediction = parkinson_model.predict(input_data)
            if prediction[0] == 1:  # Positive for Parkinson's
                result = "Positive for Parkinson's Disease"
                st.error(f"{result} 😢")
            else:  # Negative for Parkinson's
                result = "Negative for Parkinson's Disease"
                st.success(f"{result} 😊")
        except Exception as e:
            st.error(f"Error in prediction: {e}")


elif selected_tab == "Liver Prediction 🩸":
    st.header("Indian Liver Patient Prediction 🩸")
    st.write("Enter the required details to predict liver disease.")

    # Input fields
    age = st.number_input("Enter Age", value=None, step=1)
    gender = st.selectbox("Gender", ["Select" , "Male", "Female"])
    tb = st.number_input("Enter Total Bilirubin", value=None, step=0.1)
    db = st.number_input("Enter Direct Bilirubin", value=None, step=0.1)
    ap = st.number_input("Enter Alkaline_Phosphotase", value=None, step=1)
    aa = st.number_input("Enter Alamine_Aminotransferase", value=None, step=1)
    aa1 = st.number_input("Enter Aspartate_Aminotransferase", value=None, step=0.1)
    tp = st.number_input("Enter Total Proteins", value=None, step=0.1)
    alb = st.number_input("Enter Albumin", value=None, step=0.1)
    agr = st.number_input("Enter Albumin_and_Globulin_Ratio", value=None, step=0.1)
    
    # Predict button
    if st.button("Predict Liver Disease"):
        gender_value = 1 if gender == "Male" else 0
        input_data = [[age, gender_value, tb, db, ap, aa, aa1, tp, alb, agr]]
        try:
            prediction = liver_model.predict(input_data)
            if prediction[0] == 1:  # Positive for Liver Disease
                result = "Positive for Liver Disease"
                st.error(f"{result} 😢")
            else:  # Negative for Liver Disease
                result = "Negative for Liver Disease"
                st.success(f"{result} 😊")
        except Exception as e:
            st.error(f"Error in prediction: {e}")


elif selected_tab == "Kidney Prediction 💊":
    st.header("Kidney Disease Prediction 💊")
    st.write("Enter the required details to predict kidney disease.")

    # Input fields
    age = st.number_input('Enter your age', value=None)
    bp = st.number_input('Enter blood pressure (in mmHg)',value=None)
    sg = st.number_input('Enter specific gravity of urine',value=None)
    al= st.number_input('Enter albumin levels in urine',value=None)
    su=st.number_input('Enter sugar levels in urine',value=None)
    rbc_select=st.selectbox('Select Red blood cells-status',['Select','Normal','Abnormal'])
    rbc_map={'Normal':1,'Abnormal':0}
    rbc=rbc_map.get(rbc_select)
    pc_select=st.selectbox('Select pus cell count-status',['Select','Normal','Abnormal'])
    pc_map={'Normal':1,'Abnormal':0}
    pc=pc_map.get(pc_select)
    pcc_select=st.selectbox('Select pus cell clumps-status',['Select','Not present','Present'])
    pcc_map={'Present':1,'Not present':0}
    pcc=pcc_map.get(pcc_select)
    ba_select=st.selectbox('Select bacteria presence-status',['Select','Not present','Present'])
    ba_map={'Present':1,'Not present':0}
    ba=ba_map.get(ba_select)
    bgr= st.number_input('Enter blood glucose random levels',value=None)
    bu= st.number_input('Enter blood urea levels',value=None)
    sc= st.number_input('Enter serum creatinine levels',value=None)
    sod= st.number_input('Enter sodium levels',value=None)
    pot= st.number_input('Enter potassium levels',value=None)
    hemo= st.number_input('Enter hemoglobin levels',value=None)
    pcv= st.number_input('Enter packed cell volume',value=None)
    wc= st.number_input('Enter white blood cell count',value=None)
    rc= st.number_input('Enter Red blood cell count.',value=None)
    htn_select=st.selectbox('Select hypertension-status',['Select','No','Yes'])
    htn_map={'Yes':1,'No':0}
    htn=htn_map.get(htn_select)
    dm_select=st.selectbox('Select diabetes mellitus-status',['Select','No','Yes'])
    dm_map={'Yes':1,'No':0}
    dm=dm_map.get(dm_select)
    cad_select=st.selectbox('Select coronary artery disease-status',['Select','No','Yes'])
    cad_map={'Yes':1,'No':0}
    cad=cad_map.get(cad_select)
    appet_select=st.selectbox('Select appetite-status',['Select','Good','Poor'])
    appet_map={'Poor':1,'Good':0}
    appet=appet_map.get(appet_select)
    pe_select=st.selectbox('Select pedal edema-status',['Select','No','Yes'])
    pe_map={'Yes':1,'No':0}
    pe=pe_map.get(pe_select)
    ane_select=st.selectbox('Select anemia-status',['Select','No','Yes'])
    ane_map={'Yes':1,'No':0}
    ane=ane_map.get(ane_select)

    
    # Predict button for kidney disease
    if st.button("Predict Kidney Disease"):
        input_data = [[age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu, sc, sod, pot, hemo, 
                       pcv, wc, rc, htn, dm, cad, appet, pe, ane]]
        try:
            prediction = kidney_model.predict(input_data)
            if prediction[0] == 1:  # Positive for Kidney Disease
                result = "Positive for Kidney Disease"
                st.error(f"{result} 😢")
            else:  # Negative for Kidney Disease
                result = "Negative for Kidney Disease"
                st.success(f"{result} 😊")
        except Exception as e:
            st.error(f"Error in prediction: {e}")

st.text("Thank you for using the dashboard!🎊")
