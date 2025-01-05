class InverseEOSCalculator:
    def __init__(self, thermal):
        """
        Initialize the class with an instance of the Thermal class for calculations.
        thermal: An instance of the Thermal class
        """
        self.thermal = thermal

    def find_volume(self, P, T, tolerance=0.1, max_iterations=10000):
        """
        Calculate the volume V from the given pressure P and temperature T using the equation of state (EOS).
        P: Pressure (GPa)
        T: Temperature (K)
        tolerance: Calculation tolerance to determine if the condition is met
        max_iterations: Maximum number of iterations
        """
        # Define the initial volume range
        v_upper = 50
        v_lower = 30
        
        for iteration in range(max_iterations):
            v_guess = (v_lower + v_upper) / 2
            P_guess = self.thermal.P_MGD(v_guess, T)  # Use the P_MGD function from the Thermal class
            
            # Check if the current guess is close enough to the target pressure P
            if abs(P_guess - P) < tolerance:
                return v_guess  # Return the volume
            
            # Adjust the volume range based on the calculated pressure
            if P_guess < P:
                v_upper = v_guess
            else:
                v_lower = v_guess
                
        raise ValueError("Unable to find a volume that meets the condition.")

    def calculate_density(self, pressures, temperatures):
        """
        Calculate the corresponding density and temperature from the given pressure and temperature lists.
        pressures: List of pressures (GPa)
        temperatures: List of temperatures (K)
        Returns: Lists of densities, temperatures, and volumes
        """
        densities = []
        volumes = []
        for P, T in zip(pressures, temperatures):
            # Calculate the volume from the pressure and temperature
            volume = self.find_volume(P, T)
            volumes.append(volume)
            
            # Calculate the density from the volume
            rho = self.thermal.V_to_rho(volume)
            densities.append(rho)
        
        return densities, temperatures, volumes
