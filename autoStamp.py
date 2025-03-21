import datetime
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# === CONFIGURATION ===
input_pdf_path = "input.pdf"             # your source file
output_pdf_path = "output_stamped.pdf"   # stamped output file
custom_text = "Confidential"             # bottom right text
font_size = 12                           # text font size
page_width, page_height = letter         # default: letter size 612 x 792 pts

# === Watermark Generator ===
def create_watermark(date_text, right_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", font_size)

    # --- Bottom left: Date ---
    left_x = 99       # 0.5 inch margin
    bottom_y = 49     # 0.25 inch from bottom
    can.drawString(left_x, bottom_y, date_text)

    # --- Bottom right: Custom text ---
    estimated_text_width = len(right_text) * font_size * 0.6  # approx width
    right_x = page_width - estimated_text_width - 50           # 0.5 inch from right
    can.drawString(right_x, bottom_y, right_text)

    can.save()
    packet.seek(0)
    return PdfReader(packet)

# === Create watermark content ===
today = datetime.datetime.now().strftime("%Y-%m-%d")
date_text = f"Date: {today}"
watermark_pdf = create_watermark(date_text, custom_text)
watermark_page = watermark_pdf.pages[0]

# === Apply watermark to each page ===
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark_page)
    writer.add_page(page)

with open(output_pdf_path, "wb") as f:
    writer.write(f)

print(f"✅ Stamped PDF saved as '{output_pdf_path}'")
