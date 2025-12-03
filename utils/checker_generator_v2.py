#FOUR DISTINCT COLORS USING HSV COLOR SPACE WITH MAX SATURATION AND VALUE

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import math
import colorsys

def hsv_to_reportlab_color(h, s=1.0, v=1.0):
    """
    Convert HSV color to ReportLab Color object.
    h: Hue (0-360 degrees)
    s: Saturation (0-1, default 1.0 for maximum)
    v: Value/Brightness (0-1, default 1.0 for maximum)
    """
    # Convert hue from 0-360 to 0-1 range for colorsys
    h_normalized = h / 360.0
    
    # Convert HSV to RGB (0-1 range)
    r, g, b = colorsys.hsv_to_rgb(h_normalized, s, v)
    
    return colors.Color(r, g, b)

def create_checkered_pdf_with_margins(output_filename, box_size_mm=18, margin_cm=1.5):
    """
    Generates an A4 PDF with a checkered pattern using maximum saturation and value colors.
    Four colors are evenly distributed across the HSV hue spectrum (0°, 90°, 180°, 270°).
    All colors have S=1.0 (max saturation) and V=1.0 (max brightness) for clear distinction.
    A margin is added to all sides for printer compatibility.
    """
    
    # --- Four colors evenly distributed in HSV hue space ---
    # H = 0°, S = 100%, V = 100% → Pure Red
    color1 = hsv_to_reportlab_color(0)     # Red (H=0°)
    
    # H = 90°, S = 100%, V = 100% → Pure Yellow-Green
    color2 = hsv_to_reportlab_color(90)    # Yellow-Green (H=90°)
    
    # H = 180°, S = 100%, V = 100% → Pure Cyan
    color3 = hsv_to_reportlab_color(180)   # Cyan (H=180°)
    
    # H = 270°, S = 100%, V = 100% → Pure Blue-Magenta
    color4 = hsv_to_reportlab_color(270)   # Blue-Magenta (H=270°)
    
    # --- Assign colors to corners and checkerboard pattern ---
    top_left_color = color1        # Red (0°)
    top_right_color = color2       # Yellow-Green (90°)
    bottom_left_color = color1     # Cyan (180°)
    bottom_right_color = color2    # Blue-Magenta (270°)
    
    # For checkerboard pattern, use color1 and color3 (Red and Cyan - opposite hues)
    checkerboard_color1 = color3   # Red (0°)
    checkerboard_color2 = color4   # Cyan (180°)
    # ---
    
    # Get the dimensions of an A4 page
    page_width, page_height = A4
    
    # Define the margin size
    MARGIN_SIZE = margin_cm * cm
    print(f"Using a {margin_cm:.1f} cm margin on all sides.")
    
    # Calculate the 'drawable' area inside the margins
    drawable_width = page_width - (2 * MARGIN_SIZE)
    drawable_height = page_height - (2 * MARGIN_SIZE)
    
    # Convert box size from mm to points
    box_size = (box_size_mm / 10) * cm  # mm to cm, then to points
    
    # Calculate how many boxes fit in each dimension
    num_boxes_x = math.floor(drawable_width / box_size)
    num_boxes_y = math.floor(drawable_height / box_size)
    
    # Report the calculated size
    box_size_in_cm = box_size / cm
    print(f"Box size: {box_size_mm} mm ({box_size_in_cm:.2f} cm)")
    print(f"Generating PDF with a grid of {num_boxes_x}x{num_boxes_y} squares...")
    print(f"Corner colors: Red(0°), Yellow-Green(90°), Cyan(180°), Blue-Magenta(270°)")
    print(f"Checkerboard pattern: Red(0°) and Cyan(180°) alternating")
    
    c = canvas.Canvas(output_filename, pagesize=A4)
    
    # Loop through each row and column to draw the checkered pattern
    for row in range(num_boxes_y):
        for col in range(num_boxes_x):
            current_color = None
            
            # Check if this is one of the four corner squares
            if row == 0 and col == 0:  # Bottom-left corner
                current_color = bottom_left_color
            elif row == 0 and col == num_boxes_x - 1:  # Bottom-right corner
                current_color = bottom_right_color
            elif row == num_boxes_y - 1 and col == 0:  # Top-left corner
                current_color = top_left_color
            elif row == num_boxes_y - 1 and col == num_boxes_x - 1:  # Top-right corner
                current_color = top_right_color
            else:
                # Standard checkered pattern using Red (0°) and Cyan (180°)
                if (row + col) % 2 == 0:
                    current_color = checkerboard_color1  # Red
                else:
                    current_color = checkerboard_color2  # Cyan
            
            c.setFillColor(current_color)
            c.setStrokeColor(current_color)  # Set stroke to same color to prevent white lines
            
            # Offset the x and y coordinates by the margin
            x = MARGIN_SIZE + (col * box_size)
            y = MARGIN_SIZE + (row * box_size)
            
            c.rect(x, y, box_size, box_size, stroke=1, fill=1)
            
    c.save()
    print(f"Successfully created '{output_filename}' with HSV-based colors! ✅")
    print(f"All colors have maximum saturation (S=1.0) and brightness (V=1.0)")
    print(f"Hue values: 0° (Red), 90° (Yellow-Green), 180° (Cyan), 270° (Blue-Magenta)")

if __name__ == "__main__":
    # Box size in millimeters (18mm provides good calibration accuracy)
    BOX_SIZE_MM = 18
    
    # Margin size in centimeters (for printer compatibility)
    MARGIN_IN_CM = 1.5 
    
    create_checkered_pdf_with_margins(
        "checkered_calibration.pdf", 
        BOX_SIZE_MM, 
        MARGIN_IN_CM
    )


