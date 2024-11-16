from ultralytics import YOLO
import json
import cv2
import os

model = YOLO("license_plate_detector.pt")

results = model.predict(source="./datasets/test/images", save=True, save_txt=False, save_conf=False)

output_data = []

for result in results:
    image_path = result.path
    img = cv2.imread(image_path)

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        plate_no = float(box.conf)
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'Plate No: {plate_no:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        output_data.append({
            "img_coordinates": [x1, y1, x2, y2],
            "plate_no.": plate_no
        })
        
        cropped_img = img[y1:y2, x1:x2]
        cropped_save_path = os.path.join("./cropped_output", os.path.basename(image_path))
        os.makedirs("./cropped_output", exist_ok=True)
        cv2.imwrite(cropped_save_path, cropped_img)
    
    save_path = os.path.join("./predicted_outputs", os.path.basename(image_path))
    os.makedirs("./predicted_outputs", exist_ok=True)
    cv2.imwrite(save_path, img)

with open("output_results.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("Detection complete. Results saved to 'output_results.json', images saved to './predicted_outputs', and cropped images saved to './cropped_output'.")
