import request
import requests

files={'file_video': open('test2.mp4')}
payload = {'id_camera': 'C1', 'date': '2018-09-21 21:30', 'id_device': 'SN01', 'dif':'value'}
r = requests.post("http://localhost/KP/index.php/API/insertData", files=files, data=payload)
print(r.text)