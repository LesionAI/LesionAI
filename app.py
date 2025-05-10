def run_app(username):

    import streamlit as st
    import pandas as pd
    import os
    from datetime import datetime
    from PIL import Image
    import base64
    from fpdf import FPDF
    import requests

    from dotenv import load_dotenv
    load_dotenv()
    def format_info(value):
        if value in [None, '', 'nan'] or (isinstance(value, float) and str(value) == 'nan'):
            return "N/A"
        return str(value)

    st.title("LesionAI")

    base_dir = os.path.join("dossiers_patients", username)
    os.makedirs(base_dir, exist_ok=True)

    model_url = "https://serverless.roboflow.com/custom-workflow-single-label-classification-9ylyn/4"
    api_key = os.getenv('ROBOFLOW_API_KEY')

    def predict_with_roboflow(image_path):
        try:
            with open(image_path, "rb") as img_file:
                response = requests.post(f"{model_url}?api_key={api_key}", files={"file": img_file})
            if response.status_code == 200:
                data = response.json()
                preds = data.get("predictions", [])
                if preds:
                    pred = preds[0]
                    return f"{pred['class']} ({pred['confidence']*100:.1f}%)"
                return "No prediction"
            else:
                return f"Error {response.status_code}"
        except Exception as e:
            return str(e)

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Patient Report - LesionAI", ln=True, align="C")
            self.ln(10)

        def add_patient_info(self, info_dict):
            self.set_font("Arial", "", 12)
            for key, value in info_dict.items():
                self.cell(0, 10, f"{key}: {value}", ln=True)
            self.ln(5)

        def add_image_section(self, image_path, caption):
            self.set_font("Arial", "I", 11)
            self.cell(0, 10, caption, ln=True)
            self.image(image_path, w=150)
            self.ln(10)

    def generate_patient_pdf(info_dict, image_dir, output_path):
        pdf = PDF()
        pdf.add_page()
        pdf.add_patient_info(info_dict)
        images = sorted([f for f in os.listdir(image_dir) if f.endswith((".jpg", ".jpeg", ".png"))])
        for img in images:
            img_path = os.path.join(image_dir, img)
            caption = f"Image: {img}"
            pdf.add_image_section(img_path, caption)
        pdf.output(output_path)

    tab = st.tabs(["📁 Patient Records", "➕ Add Patient"])

    with tab[0]:
        st.header("📁 Patient Records")

        folders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
        patient_infos = []
        for folder in folders:
            path = os.path.join(base_dir, folder, "infos.csv")
            if os.path.exists(path):
                df = pd.read_csv(path)
                if not df.empty:
                    patient_infos.append((folder, df.iloc[0].to_dict()))

        search = st.text_input("🔎 Search patient (Name or NHC)").lower()

        if search:
            patient_infos = [
                p for p in patient_infos
                if search in str(p[1]["Nom"]).lower() or search in str(p[1]["NHC"]).lower()
            ]

        if patient_infos:
            for folder, info in patient_infos:
                with st.expander(f"👤 {info['Nom']} ({info['NHC']})"):
                    st.write(f"**Phone:** {format_info(info.get('Téléphone'))}")
                    st.write(f"**Email:** {format_info(info.get('Email'))}")
                    st.write(f"**First Consultation:** {format_info(info.get('Date de première consultation'))}")
                    st.write(f"**Allergies:** {format_info(info.get('Allergies'))}")
                    st.write(f"**Medications:** {format_info(info.get('Médicaments'))}")
                    st.write(f"**Comment:** {format_info(info.get('Commentaire'))}")
                    st.write(f"**AI Diagnosis:** {format_info(info.get('Résultat IA'))}")

                    photo_dir = os.path.join(base_dir, folder)
                    photos = sorted([f for f in os.listdir(photo_dir) if f.endswith((".jpg", ".jpeg", ".png"))])
                    for photo in photos:
                        img_path = os.path.join(photo_dir, photo)
                        st.image(img_path, caption=photo, width=600)

                    st.markdown("---")
                    st.markdown("📆 **Add Follow-up Image**")
                    followup_image = st.file_uploader("Upload follow-up image", type=["jpg", "jpeg", "png"], key=f"followup_{folder}")
                    if followup_image:
                        date_suivi = datetime.today().strftime("%Y-%m-%d")
                        followup_path = os.path.join(photo_dir, f"{date_suivi}_followup.jpg")
                        with open(followup_path, "wb") as f:
                            f.write(followup_image.getbuffer())
                        st.success("✅ Follow-up image saved successfully.")
                        st.image(followup_path, caption="Follow-up Image", width=600)

                    if st.button(f"📄 Generate PDF for {info['Nom']}", key="pdf_" + folder):
                        pdf_path = os.path.join(photo_dir, f"{str(info['Nom']).replace(' ', '_')}_report.pdf")
                        generate_patient_pdf(info, photo_dir, pdf_path)
                        with open(pdf_path, "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()
                            href = f'<a href="data:application/pdf;base64,{b64}" download="{info["Nom"].replace(" ", "_")}_report.pdf">📥 Download PDF</a>'
                            st.markdown(href, unsafe_allow_html=True)

                    if st.button(f"🗑️ Delete {info['Nom']}", key="delete_" + folder):
                        import shutil
                        shutil.rmtree(os.path.join(base_dir, folder))
                        st.warning(f"{info['Nom']}'s record deleted. Please refresh the page.")
        else:
            st.info("No patient record found.")

    with tab[1]:
        st.header("Add a New Patient")
        nhc = st.text_input("Clinical Record Number (NHC)")
        nom = st.text_input("Patient's Name")
        email = st.text_input("Email")
        telephone = st.text_input("Phone")
        date_premiere = st.date_input("First Consultation Date")
        photo = st.file_uploader("📸 Upload initial lesion image", type=["jpg", "jpeg", "png"])
        commentaire = st.text_area("Initial Comment")
        allergies = st.text_area("Allergies")
        medicaments = st.text_area("Current Medications")

        if st.button("Save Patient Record"):
            if nom and nhc and photo:
                patient_folder = os.path.join(base_dir, f"{nhc}_{nom.replace(' ', '_')}")
                os.makedirs(patient_folder, exist_ok=True)
                date_photo = datetime.today().strftime("%Y-%m-%d")
                photo_path = os.path.join(patient_folder, f"{date_photo}_initial.jpg")
                with open(photo_path, "wb") as f:
                    f.write(photo.getbuffer())

                diagnosis = predict_with_roboflow(photo_path)
                st.success(f"🧠 AI Diagnosis: {diagnosis}")

                info_path = os.path.join(patient_folder, "infos.csv")
                df = pd.DataFrame([{
                    "NHC": nhc,
                    "Nom": nom,
                    "Email": email,
                    "Téléphone": telephone,
                    "Date de première consultation": date_premiere,
                    "Allergies": allergies,
                    "Médicaments": medicaments,
                    "Commentaire": commentaire,
                    "Résultat IA": diagnosis
                }])
                df.to_csv(info_path, index=False)
                st.success(f"✅ {nom}'s record saved successfully.")
                st.image(photo, caption="Initial lesion image")
            else:
                st.warning("Please fill in all required fields and upload an image.")
