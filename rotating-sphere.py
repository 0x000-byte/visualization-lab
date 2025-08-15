# example_sphere.py
from manim import *

class RotatingSphere(ThreeDScene):
    def construct(self):
        # Set an angled view so we see the 3D nature
        self.set_camera_orientation(phi=PI/6, theta=PI/4)

        # Create a 3D sphere
        sphere = Sphere(radius=1, resolution=(24, 24))
        sphere.set_color(BLUE)

        # Add sphere to the scene
        self.add(sphere)

        # Animate its rotation
        self.play(
            Rotating(
                sphere,
                axis=UP,             # Rotate around the vertical (Y) axis
                radians=2 * PI,      # Full rotation
                run_time=5,          # Duration of 5 seconds
                rate_func=linear     # Constant speed
            )
        )

        self.wait(1)

