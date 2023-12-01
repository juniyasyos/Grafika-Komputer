import numpy as np
import matplotlib.pyplot as plt

def quarter_circle(center_x, center_y, radius, num_points=100):
    theta = np.linspace(0, np.pi / 2, num_points)
    x = center_x + radius * np.cos(theta)
    y = center_y + radius * np.sin(theta)
    return x, y

# Contoh penggunaan
center_x, center_y = 0, 0
radius = 5

x, y = quarter_circle(center_x, center_y, radius)
print(x)
print(y)

plt.plot(x, y)
plt.axis('equal')
plt.title('Seperempat Lingkaran')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.grid(True)
plt.show()
