# LusSTR GUI

This Streamlit application provides a graphical user interface (GUI) for the LusSTR tool, which is used to convert Next Generation Sequencing (NGS) data of forensic STR loci to different sequence representations and allele designations for downstream analyses.

## Installation

Before running the GUI, you need to install the LusSTR package. You can find the installation instructions at [LusSTR GitHub page](https://github.com/bioforensics/lusSTR). Make sure to activate an environment that has LusSTR installed.

## Running the GUI

Once you have installed LusSTR, you can run the GUI by executing the following command in your command terminal:

```
streamlit run lusstr_gui.py
```

## Important Note

The **working directory** for LusSTR is the directory where the `lusstr_gui.py` file is located. That means if you decide to place the `lusstr_gui.py` file in another location, that location will become the working directory for LusSTR. All input files and output files need to be specified in that directory. If you do decide to place it in a different folder, make sure to also transfer all other files from this repository to that folder: `.streamlit` and `logo.png`. Otherwise, the fancy fonts and themes of the GUI will be missing, but it will still be functional. 


