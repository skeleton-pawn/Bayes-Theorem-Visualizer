# Bayes-Theorem-Visualizer
A Python application that provides an interactive visualization of Bayes' Theorem using Tkinter and Matplotlib.
This repository contains Python code created for learning purposes, deeply inspired by the insightful work of 3Blue1Brown and Steve Brunton. Many thanks to both of them for their excellent educational content!

Bayes theorem, the geometry of changing beliefs by 3Blue1Brown
https://www.youtube.com/watch?v=HZGCoVF3YvM&t=224s

Bayes' Theorem Example: Drug Testing by Steve Brunton
https://www.youtube.com/watch?v=gE6RnZJixUw

## Overview
**Purpose**: Visualizes Bayes' Theorem concepts using interactive input and graphical representations.
This application serves as an educational tool to help users understand the principles of Bayes' Theorem in an engaging and interactive manner.

## Libraries Used:
**Tkinter**: For the graphical user interface (GUI).
**Matplotlib**: For creating visual representations of probabilities.
**Pillow (PIL)**: For handling and displaying images in the GUI.

## Key Features
**User-Friendly Input Interface**:
Users can input probabilities (P(H), P(e | H), and P(e | ¬H)).
The interface validates the inputs to ensure they are valid probabilities (between 0 and 1).

**Dynamic Graphical Visualization**: Displays a proportional representation of probabilities using rectangles and colors to denote different aspects of Bayes' Theorem.

**Error Handling**: Displays error messages if invalid probabilities are entered.

## How It Works
**Interactive Behavior**: Activating the 'Visualize' button calls the on_calculate method, responsible for validating inputs, computing results, and dynamically updating the display.



