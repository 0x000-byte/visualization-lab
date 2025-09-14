# manim_demos/commutative_diagram.py
from manim import *

class CommutativeDiagram(Scene):
    def construct(self):
        # --- Layout (tweak these if you want more/less spacing)
        x_gap = 3.0
        y_gap = 2.0
        # Coordinates for nodes:
        P0 = ORIGIN + LEFT*x_gap/2 + UP*y_gap/2   # top-left : 0
        PA = ORIGIN + RIGHT*x_gap/2 + UP*y_gap/2  # top-right: A
        PB = ORIGIN + LEFT*x_gap/2 + DOWN*y_gap/2 # bottom-left: B
        PC = ORIGIN + RIGHT*x_gap/2 + DOWN*y_gap/2# bottom-right: C

        # --- Dots + labels
        dot0 = Dot(P0); lbl0 = MathTex("0").next_to(dot0, UP, buff=0.2)
        dotA = Dot(PA); lblA = MathTex("A").next_to(dotA, UP, buff=0.2)
        dotB = Dot(PB); lblB = MathTex("B").next_to(dotB, DOWN, buff=0.2)
        dotC = Dot(PC); lblC = MathTex("C").next_to(dotC, DOWN, buff=0.2)

        nodes = VGroup(dot0, dotA, dotB, dotC, lbl0, lblA, lblB, lblC)

        # --- Arrows (B↑0, 0↘C, B→C, A↓C)
        a_B0 = Arrow(PB, P0, buff=0.1)
        a_0C = Arrow(P0, PC, buff=0.1)
        a_BC = Arrow(PB, PC, buff=0.1)
        a_AC = Arrow(PA, PC, buff=0.1)

        arrows = VGroup(a_B0, a_0C, a_BC, a_AC)

        # --- Side labels: "B + 0" (left) and "A + C" (right)
        left_label  = MathTex("B + 0").move_to(LEFT*4.2)
        right_label = MathTex("A + C").move_to(RIGHT*4.2)

        # --- Build the scene
        self.play(FadeIn(nodes, shift=0.2*UP))
        self.play(Create(a_B0), Create(a_0C))
        self.play(Create(a_BC), Create(a_AC))
        self.play(FadeIn(left_label), FadeIn(right_label))
        self.wait(1)

