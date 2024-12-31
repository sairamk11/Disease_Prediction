import streamlit as st
import pickle
import numpy as np
import os

def load_model(file_path):
    try:
        return pickle.load(open(file_path, 'rb')), None
    except FileNotFoundError:
        return None, f"Model file not found at: {file_path}"
    except OSError as e:
        return None, f"Error loading model file: {e}"

st.sidebar.title("Disease Prediction Models")
selected_model = st.sidebar.selectbox(
    "Select a prediction model:",
    ["Parkinson's Disease", "Kidney Disease", "Liver Disease"]
)

# Parkinson's Disease
if selected_model == "Parkinson's Disease":
    st.title("Parkinson's Disease Prediction")
    model_path = "Parkinson.pkl"
    model, error = load_model(model_path)

    if error:
        st.error(error)
    else:
        try:
            feature_names = model.feature_names_in_
        except AttributeError:
            st.error("Feature names are not available in the model.")
            st.stop()

        st.write("Enter the features:")
        inputs = {feature: st.number_input(feature, value=0.0) for feature in feature_names}

        if st.button("Predict Parkinson's Disease"):
            features = np.array([list(inputs.values())])
            try:
                prediction = model.predict(features)
                result = "Parkinson's Disease Detected" if prediction[0] == 1 else "No Parkinson's Disease Detected"
                st.success(f"Prediction: {result}")
            except Exception as e:
                st.error(f"Error during prediction: {e}")

# Kidney Disease 
elif selected_model == "Kidney Disease":
    st.title("Kidney Disease Prediction")
    model_path = "Kidneyprediction.pkl"
    model, error = load_model(model_path)

    if error:
        st.error(error)
    else:
        st.markdown("Enter the details below:")
        age = st.number_input("Age", min_value=1, max_value=100, value=25, step=1)
        rbc = st.selectbox("Red Blood Cells (RBC)", ["Abnormal", "Normal"])
        pc = st.selectbox("Pus Cells (PC)", ["Abnormal", "Normal"])
        pcc = st.selectbox("Pus Cell Clumps (PCC)", ["Not Present", "Present"])
        ba = st.selectbox("Bacteria (BA)", ["Not Present", "Present"])
        htn = st.selectbox("Hypertension (HTN)", ["No", "Yes"])
        dm = st.selectbox("Diabetes Mellitus (DM)", ["No", "Yes"])
        cad = st.selectbox("Coronary Artery Disease (CAD)", ["No", "Yes"])
        appet = st.selectbox("Appetite (APPET)", ["Poor", "Good"])
        pe = st.selectbox("Pedal Edema (PE)", ["No", "Yes"])
        ane = st.selectbox("Anemia (ANE)", ["No", "Yes"])
        bp = st.number_input("Blood Pressure (mmHg)", min_value=0, step=1, value=80)
        sg = st.number_input("Specific Gravity", min_value=1.005, max_value=1.030, step=0.005, value=1.020)
        al = st.number_input("Albumin (g/dL)", min_value=0, step=1, value=1)
        su = st.number_input("Sugar (mg/dL)", min_value=0, step=1, value=0)
        bgr = st.number_input("Blood Glucose Random (BGR)", min_value=0.0, step=0.1, value=150.0)
        bu = st.number_input("Blood Urea (BU)", min_value=0.0, step=0.1, value=40.0)
        sc = st.number_input("Serum Creatinine (SC)", min_value=0.0, step=0.1, value=1.2)
        sod = st.number_input("Sodium (SOD)", min_value=0.0, step=0.1, value=135.0)
        pot = st.number_input("Potassium (POT)", min_value=0.0, step=0.1, value=4.5)
        hemo = st.number_input("Hemoglobin (HEMO)", min_value=0.0, step=0.1, value=12.5)
        pcv = st.number_input("Packed Cell Volume (PCV)", min_value=0.0, step=0.1, value=40.0)
        wc = st.number_input("White Blood Cell Count (WC)", min_value=0.0, step=0.1, value=8000.0)
        rc = st.number_input("Red Blood Cell Count (RC)", min_value=0.0, step=0.1, value=4.5)

        # Cate encode
        rbc_encoded = 1 if rbc == "Normal" else 0
        pc_encoded = 1 if pc == "Normal" else 0
        pcc_encoded = 1 if pcc == "Present" else 0
        ba_encoded = 1 if ba == "Present" else 0
        htn_encoded = 1 if htn == "Yes" else 0
        dm_encoded = 1 if dm == "Yes" else 0
        cad_encoded = 1 if cad == "Yes" else 0
        appet_encoded = 1 if appet == "Good" else 0
        pe_encoded = 1 if pe == "Yes" else 0
        ane_encoded = 1 if ane == "Yes" else 0

        input_data = np.array([
            age, rbc_encoded, pc_encoded, pcc_encoded, ba_encoded, htn_encoded,
            dm_encoded, cad_encoded, appet_encoded, pe_encoded, ane_encoded,
            bp, sg, al, su, bgr, bu, sc, sod, pot, hemo, pcv, wc, rc
        ]).reshape(1, -1)

        if st.button("Predict Kidney Disease"):
            try:
                prediction = model.predict(input_data)
                result = "Kidney Disease Detected" if prediction[0] == 1 else "No Kidney Disease Detected"
                st.success(f"Prediction: {result}")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

# Liver model
elif selected_model == "Liver Disease":
    st.title("Liver Disease Prediction")
    model_path = "Indianliverpatient.pkl"
    model, error = load_model(model_path)

    if error:
        st.error(error)
    else:
        st.markdown("Enter the details below:")
        age = st.number_input("Age", min_value=1, max_value=100, value=25, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        total_bilirubin = st.number_input("Total Bilirubin", min_value=0.0, step=0.1, value=1.0)
        direct_bilirubin = st.number_input("Direct Bilirubin", min_value=0.0, step=0.1, value=0.3)
        alkaline_phosphatase = st.number_input("Alkaline Phosphatase", min_value=10, step=10, value=200)
        alamine_aminotransferase = st.number_input("Alamine Aminotransferase", min_value=1, step=1, value=25)
        aspartate_aminotransferase = st.number_input("Aspartate Aminotransferase", min_value=1, step=1, value=30)
        total_proteins = st.number_input("Total Proteins", min_value=1.0, step=0.1, value=6.5)
        albumin = st.number_input("Albumin", min_value=1.0, step=0.1, value=3.5)
        albumin_globulin_ratio = st.number_input("Albumin and Globulin Ratio", min_value=0.0, step=0.1, value=1.0)

        gender_encoded = 1 if gender == "Male" else 0
        input_data = np.array([
            age, gender_encoded, total_bilirubin, direct_bilirubin, alkaline_phosphatase,
            alamine_aminotransferase, aspartate_aminotransferase, total_proteins,
            albumin, albumin_globulin_ratio
        ]).reshape(1, -1)
        
        if st.button("Predict Liver Disease"):
            try:
                prediction = model.predict(input_data)
                result = "Liver Disease Detected" if prediction[0] == 1 else "No Liver Disease Detected"
                st.success(f"Prediction: {result}")
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
