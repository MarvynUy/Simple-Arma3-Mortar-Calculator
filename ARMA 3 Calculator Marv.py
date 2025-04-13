import math
import tkinter as tk
from tkinter import messagebox, ttk

#Original code by Josiah Evans 2016
#Modified preferencial code by Marvyn Uy 2025
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

def calcA(tar, bat):
    c1 = int(tar[0:4])
    c2 = int(bat[0:4])
    result = c1 - c2
    return result

def calcB(tar, bat):
    c3 = int(tar[4:8])
    c4= int(bat[4:8])
    return  (c3 - c4)

def calcQ(tar, bat):
    c1 = int(tar[0:4])
    c2 = int(bat[0:4])
    if c1 > c2:
        return 90
    else:
        return 270

def calcRange(a, b):
    return 10 * (a**2 + b**2)**.5
    
def calcBearing(q, a, b):
    if a == 0:
        a = 1
    return q - math.degrees(math.atan(b / a))

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


def calculate_coords():
    battery = (entry_battery.get())
    target = (entry_target.get())
    
    Alpha = calcA(target, battery)
    Bravo = calcB(target, battery)
    bearingsQ = calcQ(target, battery)
    bearings = calcBearing(bearingsQ, Alpha, Bravo)
    distance = calcRange(Alpha, Bravo)
    
    result_text.set(f"Bearings : {bearings:.2f} degrees\n"
                    f"Range : {distance:.2f} m\n")
    return


def calculate_angles():
    """Handles user input and computes elevation & azimuth angles."""
    try:
        v = float(combo_velocity.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        g = 9.81  # Gravity (m/s²)
        


        elevation_plus = compute_elevation(v, g, x, y, '+')
        elevation_minus = compute_elevation(v, g, x, y, '-')
        azimuth = compute_azimuth(x, y)

        if elevation_plus is None:
            messagebox.showerror("Error", "Target is unreachable (No real solution).")
            return

        result_text1.set(f"Elevation Angle (+) : {elevation_plus:.2f}°\n"
                        f"Elevation Angle (-) : {elevation_minus:.2f}°\n"
                        f"Azimuth Angle       : {azimuth:.2f}°")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Create the main window
root = tk.Tk()
root.title("Glitch Marvelous MK6 mortar ARMA3 Calculator")

# Labels and Entry Fields


tk.Label(root, text="|Murv's Mortar Calculator|").grid(row=0, column=0, padx=10, pady=5)

#Calculating distance and bearings
tk.Label(root, text="Firing position:").grid(row=1, column=0, padx=10, pady=5)
entry_battery = tk.Entry(root)
entry_battery.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Target position:").grid(row=2, column=0, padx=10, pady=5)
entry_target = tk.Entry(root)
entry_target.grid(row=2, column=1, padx=10, pady=5)

# Calculate Button 1
btn_calculate = tk.Button(root, text="Calculate Range Bearing", command=calculate_coords)
btn_calculate.grid(row=3, column=0, columnspan=2, pady=10)

result_text = tk.StringVar()
label_result = tk.Label(root, textvariable=result_text, justify="left", font=("Arial", 12), fg="blue")
label_result.grid(row=4, column=0, columnspan=2, pady=10)

tk.Label(root, text="|Close range: 34 to 499 metres |Medium range: 139 to 1,998 metres |Long range: 284 to 4,078 metres|").grid(row=5, column=0, padx=10, pady=5)

tk.Label(root, text="Select Initial Velocity (m/s):").grid(row=6, column=0, padx=10, pady=5)
combo_velocity = ttk.Combobox(root, values=["70", "140", "200"], state="readonly")
combo_velocity.current(0)  # Default to 70
combo_velocity.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Target Horizontal Range (m):").grid(row=7, column=0, padx=10, pady=5)
entry_x = tk.Entry(root)
entry_x.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Target Vertical Height (m):").grid(row=8, column=0, padx=10, pady=5)
entry_y = tk.Entry(root)
entry_y.grid(row=8, column=1, padx=10, pady=5)

# Calculate Button
btn_calculate = tk.Button(root, text="Calculate", command=calculate_angles)
btn_calculate.grid(row=9, column=0, columnspan=2, pady=10)

# Result Display
result_text1 = tk.StringVar()
label_result1 = tk.Label(root, textvariable=result_text1, justify="left", font=("Arial", 12), fg="blue")
label_result1.grid(row=10, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
