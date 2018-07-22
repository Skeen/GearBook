LabelMaker
----------
Inspired by the label generator; GearBook from Open Space Aarhus.

# labels.py
Produces a PDF with labels; one QR, one logo and the identifier number.

## Configuration
The script is adjustable with regards to several variables:

The size of the labels can be adjusted using:
* `columns`: The number of columns on the label paper.
* `rows`: The number of rows on the label paper.
* `cell_height`: The height of each individual label.
* `cell_width`: The width of each individual label.
Using these variables margins are calculated automatically under the assumption
that labels are centered on the page. If this is not the case, margins can be
set directly using the `margin_{left,right,top,bottom}` variables.

The paper size is configured for A4 by default, but can be configured using the
`paper_height` and `paper_width` variables.

The id of the first entry can be set using the `start_id` variable, while the
font-size for the identifier can be adjusted to fit a certain number of digits
using the `max_digits` setting.

The number of pages can be adjusted using the `pages` variable, ids continue
from the previous page.

Finally the url used for the QR codes in the labels can be adjusted using the
`base_url` string. It will have the id appended to it to generate the QR codes.

## Caveats
* The logo is assumed to be wider than it's high, if this is not the case, the
  script will not produce a usable output.

## Future work
* Reintroduce catagories of labels similar to what's done by the GearBook script.
