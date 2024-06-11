import os
from qrcode.main import QRCode
from qrcode.constants import ERROR_CORRECT_L
from config import QR_BASE_FOLDER

def create_qr(link: str) -> QRCode:
    """
    Create a QR code
    @return key:str-> The hash
    @return qr_img:str-> The path of the QR code
    """
    info = link

    qr = QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=16,
        border=2,
    )
    qr.add_data(info)
    qr.make(fit=True)

    # img = qr.make_image(fill_color="purple", back_color="black")
    img = qr.make_image()

    qr_img_path = get_qr_path()
    img.save(qr_img_path)

    return qr

def get_qr_path() -> str:
    """
    Get the path of the QR code
    @param None
    """
    base_path = os.path.split(__file__)[0]
    path = os.path.join(base_path,"static",QR_BASE_FOLDER, "qr.png")
    return path


def create_random_str(length: int) -> str:
    """
    Create a random string of given length
    @param length:int-> length of the string
    @return: str-> random string
    """
    import random
    import string
    return ''.join(random.choice(
        string.ascii_letters+string.digits
    ) for _ in range(length))

def create_hash()->str:
    """
    Create a hash of the current time
    """
    return create_random_str(8)
