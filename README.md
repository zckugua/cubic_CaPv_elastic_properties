# Elastic Data Calculation Script associated to the paper "Strong Precursor softening in cubic CaSiO3 perovskite"

This document provides detailed instructions for using the elastic data calculation script. The script enables users to calculate elastic constants, moduli, and velocities based on input temperature and density or pressure ranges.

## 1. **Introduction**
The script calculates elastic properties such as volume, pressure, and elastic constants (C11, C12, C44), as well as elastic moduli and wave velocities (Vp and Vs) under varying conditions of temperature and density or temperature and pressure. The user can input data either manually or by providing a file containing the input parameters.

---

## 2. **Usage Instructions**
### **Step 1: Run the Script**
To execute the script, simply run the following command in your terminal:

\`\`\`
python main.py
\`\`\`

---

### **Step 2: Choose the Input Method**
Upon running the script, you will be prompted to select an input method:

1. **Input from keyboard**: Manually enter temperature and density or pressure ranges.  
2. **Read from file**: Provide a file containing the input data.

Enter your choice by typing \`1\` or \`2\`.

---

### **Step 3: Select the Input Mode**
If you choose to input from the keyboard, the script will ask you to select one of the following modes:

1. **Temperature and Density Range**  
2. **Temperature and Pressure Range**

Enter your choice by typing \`1\` or \`2\`.

#### **For Temperature and Density Input**
- Enter the lower and upper limits of temperature (in Kelvin).  
- Enter the lower and upper limits of density (in g/cm³).

The script will generate 100 evenly spaced points within the specified ranges and calculate the corresponding elastic properties.

#### **For Temperature and Pressure Input**
- Enter the lower and upper limits of pressure (in GPa).  
- Enter the lower and upper limits of temperature (in Kelvin).

The script will generate 100 evenly spaced points within the specified ranges and calculate the corresponding elastic properties.

---

### **Step 4: Reading from a File**
If you choose to read input data from a file, follow these steps:

1. Select the file type:  
   - Type \`1\` for \`.dat\` file  
   - Type \`2\` for \`.xlsx\` file

2. Enter the file path and name when prompted.  
3. Select the data type:  
   - Type \`1\` for Temperature and Density  
   - Type \`2\` for Temperature and Pressure

---

### **Step 5: Output**
The script will save the calculation results to a \`.dat\` file in the following format:

\`\`\`
# Temperature(K)\tDensity(g/cm^3)\tPressure(GPa)\tVolume(A^3)\tC11(GPa)\tC12(GPa)\tC44(GPa)\tB(GPa)\tG(GPa)\tVp_h(km/s)\tVs_h(km/s)
\`\`\`

Each row contains the calculated values for each temperature and density/pressure point.

- **For Temperature and Density Input**: The results are saved in \`temp_density_results.dat\`.  
- **For Temperature and Pressure Input**: The results are saved in \`temp_pressure_results.dat\`.  
- **For File Input**: The results are saved in \`file_temp_density_results.dat\` or \`file_temp_pressure_results.dat\`.

---

## 3. **Output Explanation**

| Column Name       | Description                          |
|-------------------|--------------------------------------|
| Temperature (K)   | Temperature in Kelvin                |
| Density (g/cm³)   | Density in grams per cubic centimeter |
| Pressure (GPa)    | Pressure in gigapascals              |
| Volume (A³)       | Volume in cubic angstroms            |
| C11 (GPa)         | Elastic constant C11 in gigapascals  |
| C12 (GPa)         | Elastic constant C12 in gigapascals  |
| C44 (GPa)         | Elastic constant C44 in gigapascals  |
| B (GPa)           | Bulk modulus in gigapascals          |
| G (GPa)           | Shear modulus in gigapascals         |
| Vp_h (km/s)       | P-wave velocity (VRH average) in km/s |
| Vs_h (km/s)       | S-wave velocity (VRH average) in km/s |

---

## 4. **Notes**
- This script is designed exclusively for calculating the elastic properties of cubic CaPv. Therefore, please ensure that the input temperature and density or temperature and pressure values fall within the stability range of the cubic phase. Data outside the cubic phase may not be accurate.  
- If using a file for input, ensure that the file format and structure match the expected format (two columns: temperature and density/pressure).  
- In case of an error, the script will display a message indicating the temperature and density/pressure point that caused the issue. Check your input values for correctness.

---

## 5. **Example Run**

### **Example 1: Keyboard Input**
\`\`\`
Please select the data input method:  
1: Input from keyboard  
2: Read from file  
> 1  

Please select the input mode:  
1: Enter temperature and density range  
2: Enter temperature and pressure range  
> 1  

Please enter the lower limit of the temperature range (unit: K): 700  
Please enter the upper limit of the temperature range (unit: K): 1700  
Please enter the lower limit of the density range (unit: g/cm³): 4.45  
Please enter the upper limit of the density range (unit: g/cm³): 4.45  
\`\`\`

### **Example 2: File Input**
\`\`\`
Please select the data input method:  
1: Input from keyboard  
2: Read from file  
> 2  

Please select the file type:  
1: .dat file  
2: .xlsx file  
> 1  

Please enter the file name (including the path): data/input_data.dat  

Please select the data type:  
1: Temperature and density  
2: Temperature and pressure  
> 2  
\`\`\`

---
