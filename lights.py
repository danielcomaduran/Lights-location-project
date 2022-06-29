## This script calculates theh dimensions t

## Import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def pattern(outter_radius, inner_radius, n_circles,  n_lights):
    """
    """

    # Calculate circles metrics
    circles_radius = np.linspace(inner_radius, outter_radius, n_circles)
    circles_weight = circles_radius / outter_radius
    circles_index = np.arange(n_circles)

    sum_of_ratios = np.sum(circles_weight)

    # Calculate lights distribution
    n_lights_circle = np.zeros(n_circles)   # Number of ligths per circle

    for c, weight in enumerate(circles_weight):
        # For the last circle, put all the remaining lights
        if c == len(circles_weight):    
            n_lights_circle[c] = n_lights - np.sum(n_lights_circle[:c-1])
        
        # For all the inner circles, calculate the percentage of lights needed
        else:
            n_lights_circle[c] = np.floor(weight * n_lights / sum_of_ratios)

    return circles_radius, n_lights_circle

def circles_plot(circles_radius, n_lights_circle, lights_dia, fig_size=(5,5)):
    """
        This function plots multiple circles with the lights overlaid
    """

    circles_origin = (0,0)  # Circles origin in cartesian (0,0) [cm]
    
    fig, ax = plt.subplots(figsize=fig_size)
    ax.set_xlim(1.1*np.array([-circles_radius[-1], circles_radius[-1]]))
    ax.set_ylim(1.1*np.array([-circles_radius[-1], circles_radius[-1]]))

    for c,radius in enumerate(circles_radius):
        circle = Circle(circles_origin, radius, linestyle='--', edgecolor='k', facecolor='none')
        ax.add_patch(circle)

        lights_theta = np.linspace(0, 360, int(n_lights_circle[c]), endpoint=False) # Angles at which the lights centers should be in the circle
        lights_origin = polar2cart(radius, lights_theta+(c*90)) # Origin of the lights positions with 90 deg offset between circles

        for l in range(np.size(lights_origin,1)):
            light = Circle(lights_origin[:,l], lights_dia/2, facecolor='r')
            ax.add_patch(light)

    # plt.show()
    ax.grid()
    plt.tight_layout()

    return fig

def polar2cart(r, theta):
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))

    cart = np.array((x,y))    # Cartesian coordinates
    
    return cart

def cart2polar(x,y):
    r = x**2 + y**2
    theta_rad = np.arctan2(y,x)
    theta_deg = np.rad2deg(theta_rad)
    
    pol = np.array((r,theta_deg)) # Polar coordinates
    
    return pol
