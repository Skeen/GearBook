#!/usr/bin/env python
import os
import math
from fpdf import FPDF
from PIL import Image
import qrcode

# Constants
mm2pt = 72/25.4
logo_filename = 'logo.png'
make_grid = False
base_url = 'http://ralph.atlas.magenta.dk/item/'

# Pages
pages = 2

# Dimensions of our paper (A4)
paper_height = 297
paper_width = 210

# Information about labels
# Number of columns / rows
columns = 5
rows = 13
# Size of each label / cell
cell_height = 21.2 + 0.8
cell_width = 38.0 + 1.25

## Number of columns / rows
#columns = 3
#rows = 8
## Size of each label / cell
#cell_height = 36
#cell_width = 70

# Start ID
start_id = 1
# Maximum number of digits in ID
max_digits = 4
# max_digits = int(math.log10(start_id+(columns*rows)))+1

## Information about margins
# Calculate our total margins
margins_height = float(paper_height - (cell_height * rows))
margins_width = float(paper_width - (cell_width * columns))
# Calculate our margins (assumes centered)
margin_left = margins_width / 2
margin_right = margins_width / 2
margin_top = margins_height / 2
margin_bottom = margins_height / 2

# Find smallest dimension (for QR code max-size)
max_dimension = min(cell_height, cell_width)

# Set our border size (used to seperate things)
image_border = max_dimension/10

# Open our PDF document
pdf = FPDF()
pdf.set_margins(left=margin_left, top=margin_top)

# Figure out our font-size
# We need to know the format of our logo
logo_ratio = None
with Image.open(logo_filename) as img:
    width, height = img.size
    logo_ratio = float(height)/width
# Calculate the logo size
logo_width = cell_width-max_dimension-image_border
logo_height = logo_width*logo_ratio
# Calculate how much space will be left under the logo
height_left = cell_height - logo_height - image_border
width = None
# Start with pt=0, and go to our max height, trying to maximize width
pdf.set_font('Arial', '', 0)
for size in range(int(height_left*mm2pt)):
    width = pdf.get_string_width("x" * max_digits)
    # Stop if we get too wide
    if width > logo_width:
        break
    pdf.set_font('Arial', '', size)
pdf.set_text_color(r=0, g=0, b=0)

image_folder = 'img/'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

for page in range(pages):
    pdf.add_page()
    pdf.set_y(margin_top)
    for row in range(rows):
        pdf.set_x(margin_left)
        for column in range(columns):
            cell_id = start_id + (column + row*columns)
            qr_filename = image_folder + str(cell_id) + ".png"
            url = base_url + str(cell_id)
            # Generate QR CODE
            img = qrcode.make(url, border=0)
            img.save(qr_filename, "PNG")
            # Write in our QR code
            pdf.image(
                x=pdf.get_x()+image_border, 
                y=pdf.get_y()+image_border,
                w=max_dimension-image_border*2, 
                h=max_dimension-image_border*2, 
                name=qr_filename, 
                link=url,
            )
            # Add the logo
            pdf.image(
                x=pdf.get_x()+max_dimension, 
                y=pdf.get_y()+image_border,
                w=logo_width,
                h=logo_height,
                name=logo_filename,
            )
            # Print the id
            pdf.text(
                # Place centered under the logo (only center with max_digits)
                x=pdf.get_x()+max_dimension+logo_width/2-width/2,
                # Place on the bottom of the cell minus one border
                y=pdf.get_y()+cell_height-image_border,
                txt=str(cell_id)
            )
            if make_grid:
                pdf.rect(x=pdf.get_x(), y=pdf.get_y(), w=cell_width, h=cell_height)
            pdf.set_x(pdf.get_x() + cell_width)
            
        pdf.set_y(pdf.get_y() + cell_height)
    start_id += rows*columns

pdf.output('out.pdf', 'F')
