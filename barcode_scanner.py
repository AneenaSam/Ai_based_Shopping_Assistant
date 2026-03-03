import cv2
import time
from pyzbar.pyzbar import decode
from api_product import get_product_from_api

def scan_barcode():

    cap = cv2.VideoCapture(0)

    start_time = time.time()
    scan_delay = 2   # seconds

    while True:
        success, frame = cap.read()

        # Show instruction
        cv2.putText(frame, "Scanning... Please wait",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 255), 2)

        elapsed_time = time.time() - start_time

        # Start detection only after 3 seconds
        if elapsed_time >= scan_delay:

            for barcode in decode(frame):
                barcode_number = barcode.data.decode("utf-8")

                # Indication: Scan completed
                cv2.putText(frame, "Scan Completed!",
                            (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 255, 0), 2)

                cv2.imshow("Barcode Scanner", frame)
                cv2.waitKey(1000)  # show message for 1 sec

                cap.release()
                cv2.destroyAllWindows()

                # Fetch product from API
                product = get_product_from_api(barcode_number)
                return product

        cv2.imshow("Barcode Scanner", frame)

        # Press ESC to cancel
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return None
