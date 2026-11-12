import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(page_title="Gemini AI UI", page_icon="🤖", layout="centered")

st.title("🤖 Gemini AI Web Assistant")
st.write("Apna sawal neeche puchein aur Gemini ka jawab UI par dekhein!")

# API Key set karein
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6IrhNdOY-RgdH1CiBGXyLB_Z_s1QP4yjzmgnHP37wnokg"

# User input field
user_input = st.text_input("Apna sawal yahan type karein:", "4+4")

Math_system_Prompt = """
Aap ek strictly restricted Mahematics Ai Assistant hain.

Strict Rules:
1.Aapko Sirf aur sirf math(Mathematics / Ganit ) se jude sawalo ke jawab dena hai.
2.Agar user Math ke alawa koi bhi doosra topic puche (Jaise General Knowledge, Science, Coumpter, Coding, History, Hindi, English, Personal question, etc.), toh aapko koi Jawab nahi dena hai.
3.Math ke alwa kisi bhi sawal par aapko sirf aur sirf ye exact error massege likhna hai: "Error : Yeh aake syllabus se bahar ka sawal hai. Main sirf Mathematics (Math) ke sawalo ka jawab de sakta hoon."
"""


# Button to generate response
if st.button("Generate Answer"):
    if user_input.strip() == "":
        st.warning("Kripya koi sawal enter karein.")
    else:
        with st.spinner("Gemini soch raha hai..."):
            try:
                # Gemini Client Initialization
                client = genai.Client()

                # Interaction create karna
                interaction = client.interactions.create(
                    model="gemini-3.8-flash",  # Model name standard rakhein agar 3.8 available na ho
                    input=user_input,
                    config={
                        "system_instruction": Math_system_Prompt
                        }
                )

                #output check karna ki error message hai ye jawab
                output = interaction.output_text
                if "Error:" in output or "syllabus se bahar"  in output:
                    st.error(output)
                else:
                    st.success("Jawab:")
                    st.write(output)

                
            except Exception as e:
                st.error(f"Koi error aa gaya: {e}")
