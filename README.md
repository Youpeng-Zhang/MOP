# MOP
MOP is an off-target prediction algorithm for CRISPR-Cas9 gene editing.
############################################################
########################Preparation#########################
############################################################

Please make the following preparations before using:

1. Install Python3 and add it to the global variable
   
   You can get the latest release version of Python3 at https://www.python.org

2. Install the required packages for python from the command line

   pip3 install scikit-learn==0.22 openpyxl

3.Prepare your input file in the format of example_input.fasta at the folder "MOP"

############################################################
#########################Prediction#########################
############################################################

##########################Command###########################

python3 /path/to/MOP/off_target_prediction.py parameters

#########################Parameters#########################

-h           #show help information

-c change    #input this parameter if you use CHANGE-Seq data

-p           #specify the path to the location of the folder "MOP"

-i           #specify the input file

-o           #specify the output file

##########################Example###########################

python3 /Users/Zhang/Downloads/MOP/off_target_prediction.py -p /Users/Zhang/Downloads/ -i /Users/Zhang/Downloads/MOP/example_input.fasta -o /Users/Zhang/Downloads/MOP/example_output.txt
