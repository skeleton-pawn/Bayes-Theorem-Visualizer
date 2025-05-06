import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from PIL import Image, ImageTk
import tkinter.font as tkFont

class BayesTheoremVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.lift()
        self.root.attributes('-topmost', False)
        self.root.title("Bayes' Theorem Visualizer")
        
        # Set minimum window size to prevent tiny initial window
        self.root.minsize(800, 600)

        # Define a font for the input widgets
        self.input_font = tkFont.Font(size=14)

        # Create frames and UI elements
        self.setup_ui()
        
        # Generate visualization before showing the window
        self.on_calculate()
        
        # Update the window to ensure it's properly sized before showing
        self.root.update_idletasks()

    def setup_ui(self):
        # Create a main container frame to center the input panel
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True)
        
        # Create a left spacer for centering
        self.left_spacer = tk.Frame(self.main_container)
        self.left_spacer.pack(side='left', fill='both', expand=True)
        
        # Center input panel
        self.input_frame = tk.Frame(self.main_container, borderwidth=2, relief=tk.RIDGE, bg='#f0f0f0')
        self.input_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        # Right visualization panel
        self.viz_frame = tk.Frame(self.main_container)
        self.viz_frame.pack(side='left', fill='both', expand=True)
        
        # Apply the font to Labels, Entries, and Button
        tk.Label(self.input_frame, text="P(H): ", font=self.input_font, bg='#f0f0f0').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_ph = tk.Entry(self.input_frame, width=6, font=self.input_font)
        self.entry_ph.insert(0, "0.1")
        self.entry_ph.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="P(e | H): ", font=self.input_font, bg='#f0f0f0').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_peh = tk.Entry(self.input_frame, width=6, font=self.input_font)
        self.entry_peh.insert(0, "0.9")
        self.entry_peh.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="P(e | ¬H): ", font=self.input_font, bg='#f0f0f0').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_penh = tk.Entry(self.input_frame, width=6, font=self.input_font)
        self.entry_penh.insert(0, "0.2")
        self.entry_penh.grid(row=2, column=1, padx=5, pady=5)

        # Add separator
        tk.Frame(self.input_frame, height=2, bg='gray').grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

        # Visualization button
        self.visualize_button = tk.Button(self.input_frame, text="Visualize", command=self.on_calculate, font=self.input_font, 
                                         bg='#e0e0e0', activebackground='#d0d0d0')
        self.visualize_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Add separator
        tk.Frame(self.input_frame, height=2, bg='gray').grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=5)

        # Results text with improved formatting
        self.result_text = tk.Text(self.input_frame, height=9, width=20, wrap='word', state='disabled', 
                                  font=('Noto Sans KR', 14), bg='#f8f8f8', relief=tk.SUNKEN, padx=5, pady=5)
        self.result_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Right side image preview - now in the viz_frame
        self.image_label = tk.Label(self.viz_frame)
        self.image_label.pack(fill='both', expand=True, padx=10, pady=10)

    def draw_bayes_visual(self, P_H, P_e_given_H, P_e_given_not_H, canvas_label):
        # Increased dimensions for the visualization
        width_px = 600
        height_px = 600

        # Base proportions
        P_not_H = 1 - P_H
        total = width_px
        
        # Add padding to improve visual appearance
        padding = 5

        # Calculate widths and heights in pixels
        width_H = int(round(P_H * total))
        width_not_H = total - width_H  # Ensure total = 600 exactly

        # Ensure heights are properly calculated and constrained
        height_H_e = int(round(P_e_given_H * height_px))
        height_H_e = min(height_H_e, height_px)  # Ensure it doesn't exceed box
        
        height_not_H_e = int(round(P_e_given_not_H * height_px))
        height_not_H_e = min(height_not_H_e, height_px)  # Ensure it doesn't exceed box

        # Plot with square aspect ratio to ensure proportional visualization
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)  # Increased figure size
        ax.set_xlim(-padding, width_px + padding)
        ax.set_ylim(-padding, height_px + padding)
        ax.set_aspect('equal')  # Force square aspect ratio
        ax.axis('off')

        # Compute Bayes posterior
        P_H_given_e = (P_H * P_e_given_H) / (
            P_H * P_e_given_H + P_not_H * P_e_given_not_H
        )

        ax.set_title(f"P(H|e) = {P_H_given_e:.3f}", fontsize=20)

        # Patches: Base hypothesis areas with borders - High Contrast color scheme
        ax.add_patch(Rectangle((0, 0), width_H, height_px, 
                              facecolor='#FF7F0E',  # Orange
                              label='P(H)',
                              edgecolor='black', 
                              linewidth=3.0))
        ax.add_patch(Rectangle((width_H, 0), width_not_H, height_px, 
                              facecolor='#2CA02C',  # Green
                              label='P(¬H)',
                              edgecolor='black', 
                              linewidth=3.0))

        # Patches: Evidence areas with borders - High Contrast color scheme
        ax.add_patch(Rectangle((0, 0), width_H, height_H_e, 
                              facecolor='#1F77B4',  # Blue
                              label='P(e | H)',
                              edgecolor='black', 
                              linewidth=3.0))
        ax.add_patch(Rectangle((width_H, 0), width_not_H, height_not_H_e, 
                              facecolor='#D62728',  # Red
                              label='P(e | ¬H)',
                              edgecolor='black', 
                              linewidth=3.0))

        # Legend
        legend = ax.legend(loc='upper right', fontsize=14, title="Legend", title_fontsize=16, fancybox=True, framealpha=0.3)
        for text in legend.get_texts():
            text.set_fontsize(14)

        # Display in Tkinter
        canvas = FigureCanvasAgg(fig)
        buf = io.BytesIO()
        canvas.print_png(buf)
        buf.seek(0)
        img = Image.open(buf)
        img.thumbnail((600, 600))  # Increased thumbnail size
        tk_img = ImageTk.PhotoImage(img)
        canvas_label.config(image=tk_img)
        canvas_label.image = tk_img

        # Explanation
        explanation = (
            f" P(H) = {P_H:.2f}\n"
            f" P(¬H) = {P_not_H:.2f}\n"
            f" P(e | H) = {P_e_given_H:.2f}\n"
            f" P(e | ¬H) = {P_e_given_not_H:.2f}\n"
            f"\n"
            f" P(e ∩ H) = {P_H * P_e_given_H:.3f}\n"
            f" P(e ∩ ¬H) = {P_not_H * P_e_given_not_H:.3f}\n"
            f"\n"
            f" P(H | e) = {P_H_given_e:.3f}"
        )

        return explanation

    def on_calculate(self):
        try:
            P_H = float(self.entry_ph.get())
            P_e_given_H = float(self.entry_peh.get())
            P_e_given_not_H = float(self.entry_penh.get())

            if not (0 <= P_H <= 1 and 0 <= P_e_given_H <= 1 and 0 <= P_e_given_not_H <= 1):
                raise ValueError

            explanation = self.draw_bayes_visual(P_H, P_e_given_H, P_e_given_not_H, self.image_label)
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, explanation)
            self.result_text.config(state='disabled')

        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid probabilities between 0 and 1.")

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    
    # Create but don't show the window yet
    root.withdraw()
    
    # Initialize the application
    app = BayesTheoremVisualizer(root)
    
    # Center the window on screen with appropriate dimensions for centered layout
    window_width = 900
    window_height = 680
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Now show the fully prepared window
    root.deiconify()
    
    root.mainloop()