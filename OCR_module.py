
import requests
import uuid
import time
import json
import csv
import cv2
import tkinter.messagebox as msgbox

def OCR_start(image_file):
    # URL, key, 이미지 파일명 입력
    api_url = 'YOUR URL'
    secret_key = 'YOUR KEY'
    #image_file = '코로나.jpg'

    # json 요구문
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }   

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(image_file,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    # 결과 request
    response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

    # response를 dict로 전환
    json_data=json.loads(response.text)

    # dict를 json으로 저장
    with open('test.json', 'w', encoding='utf-8') as make_file:
        json.dump(json_data, make_file, indent="\t")
    return json_data

def OCR_post(json_data,save_file):
    '''변수 초기화'''
    prev_point2_y=0
    lines_data=[]
    line_data=[]

    for single_data in json_data["images"][0]["fields"]:
        #text 좌표 저장
        current_point1_y=single_data["boundingPoly"]["vertices"][0]["y"]

        #다음줄
        if prev_point2_y<current_point1_y:
            lines_data.append(line_data)
            line_data=[]
            line_data.append(single_data["inferText"])
        #같은줄
        else:
            line_data.append(single_data["inferText"])
        prev_point2_y=single_data["boundingPoly"]["vertices"][3]["y"]
   
    print(lines_data)
    del lines_data[0]

    '''후처리'''
    idx_date=0
    idx_phone=1
    idx_temp=2

    '''csv 저장하기'''
    with open(save_file, 'w',encoding='utf-8',newline='') as csv_file:
        csv_writer=csv.writer(csv_file)
        for line_data in lines_data:
            csv_writer.writerow(line_data)
    return lines_data

def OCR_CAM():
    cam=cv2.VideoCapture(0)
    cv2.namedWindow("Camera")
    cam.set(3,1280)
    cam.set(4,720)
    while True:
        ret_val, img=cam.read()
        cv2.imshow("test",img)
        img_name="captured_image.jpg"
        k=cv2.waitKey(1)

        if k%256==27:
            print("Escape hit, closing...")
            break
        elif k%256==32:
            cv2.imwrite(img_name,img)
            print("{} witten!".format(img_name))
            msgbox.showinfo("알림","정상적으로 캡쳐 완료")
            break

    cam.release()
    cv2.destroyAllWindows()
    return 