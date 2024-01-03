import scipy.stats as stats

def generate_exponential_form(distribution_name):
    """
    Generate the exponential form of a distribution.

    Parameters:
        distribution_name (str): Name of the distribution.

    Returns:
        str: Exponential form of the distribution.
    """
    try:
        distribution = getattr(stats, distribution_name)
        exponential_form = distribution.pdf
        return exponential_form
    except AttributeError:
        return "This distribution cannot be expressed in its exponential form!"

def calculate_likelihood(distribution_name, parameters, x):
    """
    Calculate the likelihood of a distribution at a given point.

    Parameters:
        distribution_name (str): Name of the distribution.
        parameters (tuple): Parameters of the distribution.
        x (float): Point at which to calculate the likelihood.

    Returns:
        float: Likelihood value.
    """
    try:
        distribution = getattr(stats, distribution_name)
        likelihood = distribution.pdf(x, *parameters)
        return likelihood
    except AttributeError:
        return "Invalid distribution name."

# Example usage:
distribution_name = "Normal"  # Example distribution name (exponential distribution)
exponential_form = generate_exponential_form(distribution_name)
print(f"The exponential form of {distribution_name} is: {exponential_form}")

# Example likelihood calculation for the exponential distribution
parameters = (0, 1)  # Example parameters for the exponential distribution
x_value = 2  # Example point at which to calculate the likelihood
likelihood = calculate_likelihood(distribution_name, parameters, x_value)
print(f"The likelihood of {distribution_name} at {x_value} is: {likelihood}")
