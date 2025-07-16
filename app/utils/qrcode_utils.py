import qrcode
import os

def generate_qr_code(ticket_id, upload_folder):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(ticket_id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_filename = f"ticket_{ticket_id}.png"
    qr_path = os.path.join(upload_folder, qr_filename)
    img.save(qr_path)
    return qr_filename
