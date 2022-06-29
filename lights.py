## This script calculates theh dimensions t

## Import libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def pattern(outter_radius:float, inner_radius:float, n_circles:int,  n_lights:int):
    """
        This function calculates the radius of multiple circles, as well as the distribution of [n] lights in each circle

        Parameters
        ----------
            outter_radius: float
                Radius of the larger circle to be used
            inner_radius: float
                Radius of the smallest circle to be used
            n_circles: int
                Number of circles including the largest and smallest ones
            n_lights: int
                Total number of lights to be distributed

        Returns
        -------
            circles_radius: array_like
                Array of the radius of each circle
            n_lights_circle: array_like
                Array with the number of lights included in each circle
    """

    # Calculate circles metrics
    circles_radius = np.linspace(inner_radius, outter_radius, n_circles)
    circles_weight = circles_radius / outter_radius

    sum_of_ratios = np.sum(circles_weight)

    # Calculate lights distribution
    n_lights_circle = np.zeros(n_circles)   # Number of ligths per circle

    for c, weight in enumerate(circles_weight):
        # For the last circle, put all the remaining lights
        if c == len(circles_weight)-1:    
            n_lights_circle[c] = n_lights - np.sum(n_lights_circle[:c])
        
        # For all the inner circles, calculate the percentage of lights needed
        else:
            n_lights_circle[c] = np.floor(weight * n_lights / sum_of_ratios)

    return circles_radius, n_lights_circle

def circles_plot(circles_radius:np.ndarray, n_lights_circle:np.ndarray, lights_dia:float, fig_size=(5,5)):
    """
        This function plots multiple circles with the lights overlaid

        Parameters
        ----------
            circles_radius: array_like
                Array with the radius of each circle
            n_lights_circle
                Array with the number of lights in each circle
            lights_dia: float
                Diameter of the lights
            fig_size
                Size of the figure. Specify in inches for template purposes

        Returns
        -------
            fig: Figure object
                Figure object from matplotlib
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
    """
        This function converts from polar to cartesian planes
    """
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))

    cart = np.array((x,y))    # Cartesian coordinates
    
    return cart

def cart2polar(x,y):
    """
        This function converts from cartersian to polar planes
    """
    r = x**2 + y**2
    theta_rad = np.arctan2(y,x)
    theta_deg = np.rad2deg(theta_rad)
    
    pol = np.array((r,theta_deg)) # Polar coordinates
    
    return pol
