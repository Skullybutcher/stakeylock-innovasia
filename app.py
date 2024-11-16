from roboflow import Roboflow
rf = Roboflow(api_key="3ed8mhFasnhZQHyXVGmD")
project = rf.workspace("roboflow-universe-projects").project("license-plate-recognition-rxg4e")
version = project.version(8)
dataset = version.download("yolov8")