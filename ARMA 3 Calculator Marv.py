import math
import tkinter as tk
from tkinter import messagebox


"""
    Computes the elevation angle (Θ) needed to hit a target.

    Parameters:
        v (float): Initial velocity (m/s)
        g (float): Gravity (m/s²)
        x (float): Horizontal distance to the target (m)
        y (float): Vertical height of the target (m)
        sign (str): '+' for the higher angle, '-' for the lower angle

    Returns:
        float: Elevation angle in degrees, or None if no real solution exists.
    """


def calcTime(x, v, theta):
    return x / (v*math.cos(theta))


def calcMuzzleVelocity(g, x, theta, y):
    theta = theta * (2 * math.pi / 360)
    v = ((-g * (x**2) * (math.tan(theta)**2 + 1)) / (2*y - 2*x*math.tan(theta)))**.5
    return v

def calcFireRange(v, g, theta, y):
    theta = theta * (2 * math.pi / 360)
    r = (-2 * v**2 * math.tan(theta) - ((2 * v**2 * math.tan(theta))**2 - 4 * (-g*(math.tan(theta)**2 + 1) * -2 * y * v**2))**.5) / (-2 * g * (math.tan(theta)**2 + 1))
    return r

def calcTheta(v, g, x, y):
    angles = {}
    angles["high"] = math.atan((v**2 + (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    angles["low"] = math.atan((v**2 - (v**4 - g*(g*x**2 + 2*y*v**2))**.5) / (g*x))
    return angles


def compute_elevation(v, g, x, y, sign='+'):
    """Computes the elevation angle (Θ) needed to hit a target."""
    v_squared = v ** 2
    v_fourth = v ** 4
    term_inside_sqrt = v_fourth - g * (g * x ** 2 + 2 * y * v_squared)

    if term_inside_sqrt < 0:
        return None  # No valid trajectory

    sqrt_value = math.sqrt(term_inside_sqrt)

    if sign == '+':
        numerator = v_squared + sqrt_value
    else:
        numerator = v_squared - sqrt_value

    denominator = g * x
    if denominator == 0:
        return None

    theta_rad = math.atan(numerator / denominator)
    return math.degrees(theta_rad)  # Convert to degrees

def compute_azimuth(x, y):
    """Computes the azimuth angle (ϕ) based on target position."""
    azimuth_rad = math.atan2(y, x)
    return math.degrees(azimuth_rad)  # Convert to degrees

def calculate_angles():
    """Handles user input and computes elevation & azimuth angles."""
    try:
        v = float(entry_velocity.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        g = 9.81  # Gravity (m/s²)

        elevation_plus = compute_elevation(v, g, x, y, '+')
        elevation_minus = compute_elevation(v, g, x, y, '-')
        azimuth = compute_azimuth(x, y)

        if elevation_plus is None:
            messagebox.showerror("Error", "Target is unreachable (No real solution).")
            return

        result_text.set(f"Elevation Angle (+) : {elevation_plus:.2f}°\n"
                        f"Elevation Angle (-) : {elevation_minus:.2f}°\n"
                        f"Azimuth Angle       : {azimuth:.2f}°")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("Projectile Motion Calculator")

# Labels and Entry Fields
tk.Label(root, text="|Close range: 34 to 499 metres |Medium range: 139 to 1,998 metres |Long range: 284 to 4,078 metres|").grid(row=0, column=0, padx=10, pady=5)

tk.Label(root, text="Initial Velocity (m/s):").grid(row=1, column=0, padx=10, pady=5)
entry_velocity = tk.Entry(root)
entry_velocity.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Target Horizontal Range (m):").grid(row=2, column=0, padx=10, pady=5)
entry_x = tk.Entry(root)
entry_x.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Target Vertical Height (m):").grid(row=3, column=0, padx=10, pady=5)
entry_y = tk.Entry(root)
entry_y.grid(row=3, column=1, padx=10, pady=5)

# Calculate Button
btn_calculate = tk.Button(root, text="Calculate", command=calculate_angles)
btn_calculate.grid(row=4, column=0, columnspan=2, pady=10)

# Result Display
result_text = tk.StringVar()
label_result = tk.Label(root, textvariable=result_text, justify="left", font=("Arial", 12), fg="blue")
label_result.grid(row=5, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
