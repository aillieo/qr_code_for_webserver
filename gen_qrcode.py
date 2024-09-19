import socket
import qrcode
import argparse


def get_local_ip():
    try:
        # Create a UDP socket to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to a public DNS server (Google's 8.8.8.8)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Failed to get local IP address: {e}")
        return None


def generate_qr_code(url):
    qr = qrcode.QRCode(
        version=1,  # Version of the QR code (1-40), 1 is the smallest
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    return img


def main():

    parser = argparse.ArgumentParser(description="Create a QR code for your local IP address")
    parser.add_argument('--port', type=int, default=8080, help="Port number for the web service")
    parser.add_argument('--save', action='store_true', help="Save the QR code as an image file")

    args = parser.parse_args()

    ip = get_local_ip()
    if ip:
        url = f"http://{ip}:{args.port}/"
        print(f"URL: {url}")
        
        img = generate_qr_code(url)
        img.show()

        # Save the QR code as an image file if the --save flag is provided
        if args.save:
            img.save("web_service_qrcode.png")
            print("QR code saved as web_service_qrcode.png")
    else:
        print("Failed to get local IP address")


if __name__ == "__main__":
    main()
