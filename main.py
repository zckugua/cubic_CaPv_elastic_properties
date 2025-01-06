import numpy as np
import pandas as pd
from thermal_P import Thermal
from elastic_constants_calculator import ElasticConstantsCalculator
from elastic_constants_convertion import ElasticConstantsConvertion
from elastic_modulus_velocity_calculator import ElasticModulusAndVelocityCalculator
from inverse_eos_calculator import InverseEOSCalculator

# Get user input for temperature and density range
def get_temperature_and_density_input():
    """
    Get the input for temperature and density range
    Returns: lower and upper limits of the temperature and density range
    """
    try:
        T_min = float(input("Please enter the lower limit of the temperature range (unit: K): "))
        T_max = float(input("Please enter the upper limit of the temperature range (unit: K): "))
        rho_min = float(input("Please enter the lower limit of the density range (unit: g/cm³): "))
        rho_max = float(input("Please enter the upper limit of the density range (unit: g/cm³): "))
    except ValueError:
        raise ValueError("Invalid input, please make sure to enter numeric values.")
    return T_min, T_max, rho_min, rho_max

# Get user input for temperature and pressure range
def get_temperature_and_pressure_input():
    """
    Get the input for temperature and pressure range
    Returns: lower and upper limits of the temperature and pressure range
    """
    try:
        T_min = float(input("Please enter the lower limit of the temperature range (unit: K): "))
        T_max = float(input("Please enter the upper limit of the temperature range (unit: K): "))
        P_min = float(input("Please enter the lower limit of the pressure range (unit: GPa): "))
        P_max = float(input("Please enter the upper limit of the pressure range (unit: GPa): "))
    except ValueError:
        raise ValueError("Invalid input, please make sure to enter numeric values.")
    return T_min, T_max, P_min, P_max

def read_data_from_file(filename, filetype):
    """
    Read temperature and density or pressure data from a file
    filename: file path
    filetype: file type ('dat' or 'xlsx')
    Returns: lists of temperatures and density or pressure
    """
    if filetype == 'dat':
        data = np.loadtxt(filename)
    elif filetype == 'xlsx':
        data = pd.read_excel(filename).to_numpy()
    else:
        raise ValueError("Unsupported file type")

    temperatures = data[:, 0]
    values = data[:, 1]
    return temperatures, values

def save_to_dat_file(filename, data):
    """
    Save the calculation results to a .dat file, keeping two decimal places
    filename: file name
    data: results to be saved (list)
    """
    with open(filename, 'w') as f:
        # Write column headers, starting with `#`, columns separated by Tab (\t)
        f.write("# Temperature(K)\tDensity(g/cm^3)\tPressure(GPa)\tVolume(A^3)\tC11(GPa)\tC12(GPa)\tC44(GPa)\tB(GPa)\tG(GPa)\tVp_h(km/s)\tVs_h(km/s)\n")
        # Write data, with columns also separated by Tab (\t), keeping two decimal places
        for row in data:
            f.write("\t".join(f"{value:.2f}" for value in row) + "\n")

# Main program
if __name__ == "__main__":
    # Initialize Thermal class
    th = Thermal()

    # Instantiate InverseEOSCalculator class
    inverse_calculator = InverseEOSCalculator(th)

    # Let the user choose the data input method
    print("Please select the data input method:")
    print("1: Input from keyboard")
    print("2: Read from file")

    input_mode = input("Please enter your choice (1 or 2): ")

    if input_mode == "1":
        # Let the user choose the input mode
        print("Please select the input mode:")
        print("1: Enter temperature and density range")
        print("2: Enter temperature and pressure range")

        mode = input("Please enter your choice (1 or 2): ")

        if mode == "1":
            # Enter temperature and density range, calculate volume, pressure, elastic constants, and velocities
            T_min, T_max, rho_min, rho_max = get_temperature_and_density_input()

            # Generate 100 evenly spaced temperature and density points
            if T_min == T_max:
                temperatures = np.full(100, T_min)
            else:
                temperatures = np.linspace(T_min, T_max, 100)

            if rho_min == rho_max:
                densities = np.full(100, rho_min)
            else:
                densities = np.linspace(rho_min, rho_max, 100)

            # Initialize ElasticConstantsCalculator class
            calculator = ElasticConstantsCalculator()

            # Initialize ElasticConstantsConvertion class
            convertion = ElasticConstantsConvertion()

            results = []
            for T, rho in zip(temperatures, densities):
                try:
                    volume = th.rho_to_V(rho)
                    pressure = th.P_MGD(volume, T)

                    c11_value, c12_value, c44_value = calculator.calculate_elastic_constants(rho, T)
                    converted_c11, converted_c12 = convertion.adiabatic_elastic_constants(th, volume, T, c11_value, c12_value)

                    # Calculate elastic moduli and velocities
                    modulus_velocity_calculator = ElasticModulusAndVelocityCalculator(converted_c11, converted_c12, c44_value, rho)
                    B_hill, G_hill, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r = modulus_velocity_calculator.compute_modulus_and_velocity()

                    row = [T, rho, pressure, volume, c11_value, c12_value, c44_value, B_hill, G_hill, Vp_h, Vs_h]
                    results.append(row)

                except Exception as e:
                    print(f"Error encountered while calculating for temperature {T} K and density {rho} g/cm³: {e}")

            # Save the results
            save_to_dat_file("temp_density_results.dat", results)
            print(f"\nThe results have been saved to 'temp_density_results.dat'")

        elif mode == "2":
            # Enter temperature and pressure range, calculate volume and density, then calculate elastic constants and velocities
            T_min, T_max, P_min, P_max = get_temperature_and_pressure_input()

            # Generate 100 evenly spaced pressure and temperature points
            if P_min == P_max:
                pressures = np.full(100,P_min)
            else:
                pressures = np.linspace(P_min, P_max, 100)
                
            if T_min == T_max:
                temperatures = np.full(100, T_min)
            else:
                temperatures = np.linspace(T_min, T_max, 100)

            # Use InverseEOSCalculator to calculate volume and density
            densities, temperatures, volumes = inverse_calculator.calculate_density(pressures, temperatures)

            # Initialize ElasticConstantsCalculator and ElasticConstantsCorrection classes
            calculator = ElasticConstantsCalculator()
            convertion = ElasticConstantsConvertion()

            results = []
            for i in range(len(pressures)):
                try:
                    T = temperatures[i]
                    rho = densities[i]
                    volume = volumes[i]
                    pressure = pressures[i]

                    # Calculate isothermal elastic constants
                    c11_value, c12_value, c44_value = calculator.calculate_elastic_constants(rho, T)

                    # Correct C11 and C12 to get adiabatic elastic constants
                    converted_c11, converted_c12 = convertion.adiabatic_elastic_constants(th, volume, T, c11_value, c12_value)

                    # Calculate elastic moduli and velocities
                    modulus_velocity_calculator = ElasticModulusAndVelocityCalculator(converted_c11, converted_c12, c44_value, rho)
                    B_hill, G_hill, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r = modulus_velocity_calculator.compute_modulus_and_velocity()

                    # Organize the results into rows
                    row = [T, rho, pressure, volume, c11_value, c12_value, c44_value, B_hill, G_hill, Vp_h, Vs_h]
                    results.append(row)

                except Exception as e:
                    print(f"Error encountered while calculating for temperature {T} K and pressure {pressure} GPa: {e}")

            # Save the results
            save_to_dat_file("temp_pressure_results.dat", results)
            print(f"\nThe results have been saved to 'temp_pressure_results.dat'")

    elif input_mode == "2":
        # Select the file type and read the file
        print("Please select the file type:")
        print("1: .dat file")
        print("2: .xlsx file")

        file_type_choice = input("Please enter your choice (1 or 2): ")

        if file_type_choice == "1":
            filetype = "dat"
        elif file_type_choice == "2":
            filetype = "xlsx"
        else:
            print("Invalid choice.")
            exit()

        filename = input("Please enter the file name (including the path): ")

        # Select the data mode
        print("Please select the data type:")
        print("1: Temperature and density")
        print("2: Temperature and pressure")

        data_mode = input("Please enter your choice (1 or 2): ")

        try:
            temperatures, values = read_data_from_file(filename, filetype)
        except Exception as e:
            print(f"Error reading the file: {e}")
            exit()

        if data_mode == "1":
            # Case for temperature and density
            densities = values
            pressures = [th.P_MGD(th.rho_to_V(rho), T) for rho, T in zip(densities, temperatures)]

            # Initialize ElasticConstantsCalculator and ElasticConstantsCorrection classes
            calculator = ElasticConstantsCalculator()
            convertion = ElasticConstantsConvertion()

            results = []
            for i in range(len(temperatures)):
                try:
                    T = temperatures[i]
                    rho = densities[i]
                    volume = th.rho_to_V(rho)
                    pressure = pressures[i]

                    # Calculate isothermal elastic constants
                    c11_value, c12_value, c44_value = calculator.calculate_elastic_constants(rho, T)

                    # Correct C11 and C12 to get adiabatic elastic constants
                    converted_c11, converted_c12 = convertion.adiabatic_elastic_constants(th, volume, T, c11_value, c12_value)

                    # Calculate elastic moduli and velocities
                    modulus_velocity_calculator = ElasticModulusAndVelocityCalculator(converted_c11, converted_c12, c44_value, rho)
                    B_hill, G_hill, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r = modulus_velocity_calculator.compute_modulus_and_velocity()

                    # Organize the results into rows
                    row = [T, rho, pressure, volume, c11_value, c12_value, c44_value, B_hill, G_hill, Vp_h, Vs_h]
                    results.append(row)

                except Exception as e:
                    print(f"Error encountered while calculating for temperature {T} K and density {rho} g/cm³: {e}")

            # Save the results
            save_to_dat_file("file_temp_density_results.dat", results)
            print(f"\nThe results have been saved to 'file_temp_density_results.dat'")

        elif data_mode == "2":
            # Case for temperature and pressure
            pressures = values

            # Use InverseEOSCalculator to calculate volume and density
            densities, temperatures, volumes = inverse_calculator.calculate_density(pressures, temperatures)

            # Initialize ElasticConstantsCalculator and ElasticConstantsCorrection classes
            calculator = ElasticConstantsCalculator()
            convertion = ElasticConstantsConvertion()

            results = []
            for i in range(len(pressures)):
                try:
                    T = temperatures[i]
                    rho = densities[i]
                    volume = volumes[i]
                    pressure = pressures[i]

                    # Calculate isothermal elastic constants
                    c11_value, c12_value, c44_value = calculator.calculate_elastic_constants(rho, T)

                    # Correct C11 and C12 to get adiabatic elastic constants
                    converted_c11, converted_c12 = convertion.adiabatic_elastic_constants(th, volume, T, c11_value, c12_value)

                    # Calculate elastic moduli and velocities
                    modulus_velocity_calculator = ElasticModulusAndVelocityCalculator(converted_c11, converted_c12, c44_value, rho)
                    B_hill, G_hill, Vp_h, Vs_h, Vp_v, Vs_v, Vp_r, Vs_r = modulus_velocity_calculator.compute_modulus_and_velocity()

                    # Organize the results into rows
                    row = [T, rho, pressure, volume, c11_value, c12_value, c44_value, B_hill, G_hill, Vp_h, Vs_h]
                    results.append(row)

                except Exception as e:
                    print(f"Error encountered while calculating for temperature {T} K and pressure {pressure} GPa: {e}")

            # Save the results
            save_to_dat_file("file_temp_pressure_results.dat", results)
            print(f"\nThe results have been saved to 'file_temp_pressure_results.dat'")

    else:
        print("Invalid choice, please enter 1 or 2.")
