'''GUI'''
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as msgbox
from tkinter import*
import tkinter as tk
import os
'''OCR'''
from OCR_module import OCR_start #타 헤더 파일 호출
from OCR_module import OCR_post
from OCR_module import OCR_CAM


root = Tk()
root.title("출입 명부 관리 프로그램")

# add file
def add_file():
    files = filedialog.askopenfilenames(title="이미지 파일을 선택하세요.",
                                        filetypes=(("jpeg files", "*.jpg"), ("all", "*.*")), 
                                        initialdir="C:/")

    # output
    for file in files:
        list_file.insert(END, file)


# delete list
def del_file():
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

# save path
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected == '':
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)


# after start button
def start():
    if list_file.size() == 0:
        msgbox.showinfo(title="error", message="파일을 선택해주세요.")
        return

    if len(txt_dest_path.get()) == 0:
        msgbox.showinfo(title="error", message="저장할 경로를 선택해주세요.")
        return

    if len(txt_dest_path.get()) == 0:
        msgbox.showinfo(title="No merged file name", message="choose new file name")
        return
    
    #파일 저장
    img_list=list_file.get(0,END)
    i=0
    for img_file in img_list:
        save_file="result_{}.csv".format(i)
        lines_data=OCR_post(OCR_start(img_file),save_file)

    #실행
    result_window(lines_data)

def cam_mode():
    OCR_CAM()
    return 

def result_window(lines_data):
    outcome=Tk()
    outcome.title("결과화면")
    outcome.geometry("700x600")
    
    #결과 Frame
    txt_frame=Frame(outcome)
    lbl_list=Label(txt_frame, text="결과",relief="sunken",width=68)
    lbl_list.pack(side="top")

    scrollbar=Scrollbar(txt_frame)
    scrollbar.pack(side="right",fill="y")

    txt=Text(txt_frame, yscrollcommand=scrollbar.set)
    
    #txt 내용 들어가야함
    for i in lines_data:
        txt.insert(END,i)
        txt.insert(END,'\n')
    
    txt.pack(side=LEFT)
    scrollbar.config(command=txt.yview)
    txt_frame.pack()
   
    #입력 frame
    input_frame=tk.LabelFrame(outcome,text="입력")
    input_frame.pack(fill="both",padx=5, pady=5, ipady=5)
    #체온 및 이름 입력
    text_entry1 = tk.Entry(input_frame)
    text_entry1.pack(side="left",fill="x",expand=True, padx=5, pady=5, ipady=4)

       
    def temp_btncmd():
        txt2.delete("1.0",END)
        tempInput=text_entry1.get()
        tempInput=float(tempInput)
        cnt=0
        for i in lines_data:
            if cnt!=0:
                tempData=float(i[4])
                if tempData>=tempInput:
                    txt2.insert(END,i)
                    txt2.insert(END,'\n')
            cnt+=1

    temp_btn=Button(input_frame, text="체온으로 찾기", command=temp_btncmd,width=10)
    temp_btn.pack(side="left",padx=5, pady=5)

    def name_btncmd():
        txt2.delete("1.0",END)
        nameInput=text_entry1.get()
        for i in lines_data:
            cnt=i[2].find(nameInput,0)
            if cnt!=-1:
                txt2.insert(END,i)
                txt2.insert(END,'\n')
        
    name_btn=Button(input_frame,text="이름으로 찾기",command=name_btncmd,width=10)
    name_btn.pack(side="right",padx=5,pady=5)

    #검색 결과 frame
    output_frame=LabelFrame(outcome,text="검색결과")
    output_frame.pack(side=LEFT, fill="both",padx=5, pady=5, ipady=5)
    scrollbar2=Scrollbar(output_frame)
    scrollbar2.pack(side="right",fill="y")
    txt2=Text(output_frame, yscrollcommand=scrollbar2.set)
    txt2.pack(side=LEFT,padx=15, pady=15, ipady=15)
    scrollbar2.config(command=txt2.yview)
    output_frame.pack()

    outcome.mainloop()
    return

'''GUI'''
# 파일 프레임
file_frame = Frame(root)
file_frame.pack(padx=5, pady=5, fill='x')

lbl_name = Label(file_frame, text="파일 추가 : ", width=8, anchor="e")
lbl_name.pack(side="left", fill="x", expand=True)

new_name = Entry(file_frame)
new_name.pack(side="left", expand=True, padx=2, pady=2, ipady=4)

btn_add_file = Button(file_frame, padx=5, pady=5, width=10, text="찾아오기", command=add_file)
btn_add_file.pack(side="left", padx=5, pady=5)

btn_del_file = Button(file_frame, padx=5, pady=5, width=10, text="삭제", command=del_file)
btn_del_file.pack(side="right", padx=5, pady=5)

# 리스트 창
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

lbl_list = Label(list_frame, text="파일 목록", relief="sunken", width=68)
lbl_list.pack(side="top")

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)

# 저장 경로
path_frame = LabelFrame(root, text="결과 파일 저장 경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4)

btn_dest_path = Button(path_frame, text="경로선택", width=10, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)

# 실행 프레임

frame_run = Frame(root, padx=5, pady=5)
frame_run.pack(fill="x", ipady=5)
btn_CAM=Button(frame_run,padx=5,pady=5,text="카메라모드",width=12,command=cam_mode)
btn_CAM.pack(side="left",padx=5,pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="종료", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="실행", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()