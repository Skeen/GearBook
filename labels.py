#!/usr/bin/env python
import os
from fpdf import FPDF
import qrcode

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

columns = 5
rows = 13

paper_height = 297
paper_width = 210

margin_top = 10
margin_bottom = 10
margin_left = 10
margin_right = 10

cell_height = float(paper_height - margin_top - margin_bottom) / rows
cell_width = float(paper_width - margin_left - margin_right) / columns

#label_width = 38
#label_height = 21.2
#
#cell_width_spacing = (cell_width - label_width) / columns
#cell_height_spacing = (cell_height - label_height) / columns
#
#print cell_width_spacing
#print cell_height_spacing

start_id = 0
image_folder = 'img/'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

current_y = 0
current_x = 0
for row in range(rows):
    current_x = 0
    for column in range(columns):
        cell_id = start_id + (column + row*columns)
        qr_filename = image_folder + str(start_id + columns*row) + ".png"
        url = 'http://ralph.atlas.magenta.dk/item/' + str(cell_id)
        # Generate QR CODE
        img = qrcode.make(url)
        img.save(qr_filename, "PNG")
        # Find smallest dimension (for QR code max-size)
        max_dimension = min(cell_height, cell_width)
        # Write in our QR code
        pdf.image(
            qr_filename, margin_left+current_x, margin_top+current_y,
            max_dimension, max_dimension, link=url
        )
        pdf.text(margin_left+current_x+max_dimension, margin_top+current_y+cell_height, str(row) + ':' + str(column) + " (" + str(cell_id) + ")")
        pdf.rect(margin_left+current_x, margin_top+current_y, cell_width, cell_height)

        current_x += cell_width
    current_y += cell_height

pdf.output('tuto1.pdf', 'F')
