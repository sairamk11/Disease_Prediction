import streamlit as st
import pickle

# Load models
@st.cache_resource
def load_model(file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)

parkinson_model = load_model('/mnt/data/Parkinson.pkl')
liver_model = load_model('/mnt/data/Indianliverpatient.pkl')
kidney_model = load_model('/mnt/data/Kidneyprediction.pkl')

# App configuration
st.title("Health Prediction App")
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

tabs = ["Parkinson's Prediction", "Liver Patient Prediction", "Kidney Prediction"]
selected_tab = st.sidebar.radio("Go to", tabs)

if selected_tab == "Parkinson's Prediction":
    st.header("Parkinson's Disease Prediction")
    st.write("Enter the required details to predict Parkinson's disease.")

    # Input fields
    fo = st.number_input("MDVP:Fo(Hz) - Average vocal fundamental frequency", min_value=0.0, step=0.1)
    fhi = st.number_input("MDVP:Fhi(Hz) - Maximum vocal fundamental frequency", min_value=0.0, step=0.1)
    flo = st.number_input("MDVP:Flo(Hz) - Minimum vocal fundamental frequency", min_value=0.0, step=0.1)
    shimmer = st.number_input("Shimmer - Variation in amplitude", min_value=0.0, step=0.001)
    spread2 = st.number_input("Spread2 - Spread of frequency", min_value=-100.0, step=0.1)

    # Predict button
    if st.button("Predict Parkinson's Disease"):
        input_data = [[fo, fhi, flo, shimmer, spread2]]
        prediction = parkinson_model.predict(input_data)
        result = "Positive for Parkinson's" if prediction[0] == 1 else "Negative for Parkinson's"
        st.success(f"Prediction: {result}")

elif selected_tab == "Liver Patient Prediction":
    st.header("Indian Liver Patient Prediction")
    st.write("Enter the required details to predict liver disease.")

    # Input fields
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    tb = st.number_input("Total Bilirubin", min_value=0.0, step=0.1)
    db = st.number_input("Direct Bilirubin", min_value=0.0, step=0.1)
    alkphos = st.number_input("Alkaline Phosphotase", min_value=0, step=1)

    # Predict button
    if st.button("Predict Liver Disease"):
        gender_value = 1 if gender == "Male" else 0
        input_data = [[age, gender_value, tb, db, alkphos]]
        prediction = liver_model.predict(input_data)
        result = "Positive for Liver Disease" if prediction[0] == 1 else "Negative for Liver Disease"
        st.success(f"Prediction: {result}")

elif selected_tab == "Kidney Prediction":
    st.header("Kidney Disease Prediction")
    st.write("Enter the required details to predict kidney disease.")

    # Input fields
    sg = st.number_input("Specific Gravity", min_value=1.000, max_value=1.030, step=0.001)
    al = st.number_input("Albumin", min_value=0, max_value=5, step=1)
    sc = st.number_input("Serum Creatinine", min_value=0.0, step=0.1)
    hemo = st.number_input("Hemoglobin", min_value=0.0, step=0.1)
    pcv = st.number_input("Packed Cell Volume", min_value=0, step=1)

    # Predict button
    if st.button("Predict Kidney Disease"):
        input_data = [[sg, al, sc, hemo, pcv]]
        prediction = kidney_model.predict(input_data)
        result = "Positive for Kidney Disease" if prediction[0] == 1 else "Negative for Kidney Disease"
        st.success(f"Prediction: {result}")
