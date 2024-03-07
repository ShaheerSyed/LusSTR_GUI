## Shaheer Syed
## A Web-based GUI for LusSTR
## 2024

# ------------- Importing Necessary Packages ------------------ #

import streamlit as st
from streamlit_option_menu import option_menu
import yaml
import subprocess
import os



# ------------ Function to Generate config.yaml File ---------- #

def generate_config_file(config_data):
    with open('config.yaml', 'w') as file:
        yaml.dump(config_data, file)
        

# ------------ Front-End Logic for Navigation Bar-------------- #

def main():
    
    # Page Layout (Theme and Fonts have been established in .streamlit/config.toml)
    st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

    # Creating Navigation Bar
    
    selected = option_menu(
        menu_title=None,
        options=["Home", "How to Use", "Contact"],
        icons=["house", "book", "envelope"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )

    if selected == "Home":
        show_home_page()
        
    elif selected == "How to Use":
        show_how_to_use_page()
        
    elif selected == "Contact":
        show_contact_page()
        
# ---------------------  LusSTR Home Page --------------------- #

def show_home_page():
    
    image_path = "logo.png"
    
    st.image(image_path, width=1000)
    
    st.markdown("""
        lusSTR is a tool written in Python to convert Next Generation Sequencing (NGS) data of forensic STR loci to different sequence representations (sequence bracketed form) and allele designations (CE allele, LUS/LUS+ alleles) for ease in downstream analyses.
        For more information on LusSTR, visit our [GitHub page](https://github.com/bioforensics/lusSTR/tree/master).
        """, unsafe_allow_html=True)

    st.title("Configuration Settings")
    
    st.info('Please Select Settings Below for LusSTR! For Information Regarding the Settings, See the How to Use Tab.')
    
# -- Enter Settings Which Will Be Used to Generate Config File -- #
    
    # General Settings
    
    st.subheader("General Settings")

    analysis_software = st.selectbox("Analysis Software", options=["uas", "straitrazor", "genemarker"], help = "Indicate the analysis software used prior to lusSTR sex.")
    
    sex = st.checkbox("Include sex-chromosome STRs", help = "Check the box if yes, otherwise leave unchecked.")
    
    samp_input = st.text_input("Path to Input Directory or Sample File", "/path/to/input/directory/or/samples", help = "Be sure to see requirements in How to Use tab.")
    
    output = st.text_input("Path for Generated Output Files", "lusstr_output", help = "Be sure to see requirements in How to Use tab.")
    
    
    # Convert Settings
    
    st.subheader("Convert Settings")
    
    kit = st.selectbox("ForenSeq or PowerSeq Data", options = ["forenseq", "powerseq"])
    
    nocombine = st.checkbox("Do Not Combine Identical Sequences")
    
    # Filter Settings
    
    st.subheader("Filter Settings")
    
    output_type = st.selectbox("Output Type", options=["strmix", "efm", "mpsproto"])
    
    profile_type = st.selectbox("Profile Type", options=["evidence", "reference"])
    
    data_type = st.selectbox("Data Type", options=["ngs", "ce", "lusplus"])
    
    info = st.checkbox("Create Allele Information File")
    
    separate = st.checkbox("Create Separate Files for Samples", help = "If True, Will Create Individual Files for Samples; If False, Will Create One File with all Samples.")
    
    nofilters = st.checkbox("Skip all filtering steps", help = "Skip all Filtering Steps; Will Still Create EFM/MPSproto/STRmix Output Files")
    
    strand = st.selectbox("Strand Orientation", options=["uas", "forward"], help = "Indicates the Strand Orientation in which to Report the Sequence in the Final Output Table for STRmix NGS only.")
    

# ------------------ Generate Config File ------------------------- #
    
# --------------------------- Backend ----------------------------- #

    # Submit Button Instance
    if st.button("Submit"):
        
        # Check if all required fields are filled
        if analysis_software and samp_input and output:
        
            # Display loading spinner
            with st.spinner("Processing Your Data..."):
            
                # Construct config data
                config_data = {
                    "analysis_software": analysis_software,
                    "sex": sex,
                    "samp_input": samp_input,
                    "output": output,
                    "kit": kit,
                    "nocombine": nocombine,
                    "output_type": output_type,
                    "profile_type": profile_type,
                    "data_type": data_type,
                    "info": info,
                    "separate": separate,
                    "nofilters": nofilters,
                    "strand": strand
                    }

                # Generate YAML config file
                generate_config_file(config_data)

                # Run terminal command
                try:
                    subprocess.run(["lusstr", "strs", "all"], check=True)
                    st.success("Config File Generated and LusSTR Executed Successfully! Output Files Have Been Saved to Your Designated Directory")
                except subprocess.CalledProcessError as e:
                    st.error(f"Error: {e}")
                    st.info("Please make sure to check the 'How to Use' tab for common error resolutions.")
                    
        else:
            st.warning("Please fill out all required fields (Analysis Software, Path to Input Directory or Sample File, Path for Generated Output Files) before submitting.")

    
# ------------------- End of Home Page ---------------------------- #   
    
# ------------------- Start of 'How to Use Page' ------------------ #  
    
def show_how_to_use_page():
    
    st.title("Common Errors and Best Practices for Using LusSTR")
    
    st.header("1. File Path Formatting")
   
    st.write("When specifying file paths, ensure you use forward slashes ('/') instead of backslashes ('\\').")
    
    st.code("Incorrect: 'C:\\Users\\username\\Desktop\\file.txt'\nCorrect: C:/Users/username/Desktop/file.txt")


    st.header("2. Avoid Quotation Marks")
    
    st.write("Do not enclose file paths in quotation marks. Simply write the path without any additional characters.")
    
    st.code("Incorrect: 'path/to/file.txt'\nCorrect: path/to/file.txt")

    st.header("3. Output Folder Location")
    
    st.write("LusSTR creates the output folder for you! You do not need to manually create one. Just simply type in a name of the folder. Note: You can simply use default placeholder for output. Another Note: You need to be in your working directory")
    st.write("This ensures that output files are saved correctly.")
    
    st.code("Incorrect: 'working_directory/subfolder/subfolder'\nCorrect: working_directory/output # or just output, since you are likely already in working directory if you are using this GUI.")

    st.header("4. Output Folder Usage")
    
    st.write("Not all output results are stored in the specified output folder. Some results may be saved directly in the working directory.")
    
    st.write("Be aware of this behavior when checking for output files.")

    st.header("5. Working Directory Awareness")
    
    st.write("Always work within the working directory, especially when dealing with output files.")
    
    st.write("Ensure that paths and file operations are relative to the working directory to avoid confusion.")
    
    st.title("LusSTR")
    
    st.markdown("""
                        
    **_LusSTR Accommodates Four Different Input Formats:_**

    (1) UAS Sample Details Report, UAS Sample Report, and UAS Phenotype Report (for SNP processing) in .xlsx format (a single file or directory containing multiple files)

    (2) STRait Razor v3 output with one sample per file (a single file or directory containing multiple files)

    (3) GeneMarker v2.6 output (a single file or directory containing multiple files)

    (4) Sample(s) sequences in CSV format; first four columns must be Locus, NumReads, Sequence, SampleID; Optional last two columns can be Project and Analysis IDs.

   
    """, unsafe_allow_html = True)

    
    
    
# ------------------- End of How to Use Page ---------------------------- #  
    
    
# ------------------- Start of 'Contact Page' ------------------ #

def show_contact_page():
    st.title("Contact Us")
    st.write("For any questions or issues, please contact rebecca.mitchell@st.dhs.gov")

if __name__ == "__main__":
    main()
