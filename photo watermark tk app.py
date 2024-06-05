from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import os, time

root =Tk()
root.title('Watermark Photos')
root.resizable(0,0)
displaycanvas = Canvas(root,width = 320, height = 430)
displaycanvas.pack()

def app_guide():
    messagebox.showinfo('app guide','''1. Click on Choose your watermark photo
2. Click on Choose your pictures' folder path and choose the wanted folder
3. Click on Choose a folder path to save watermarked images
4. Choose a position to locate the watermark on your pictures
5. Choose a margin to keep a distance between the watermark and margins of the photo
6. Enter the desired width (if this field left 0, it will be the width of the original photo)
7. Enter the desired height (if this field left 0, it will be the height of the original photo)
8. Click on WaterMark to start the process
''')
def app_creator():
    messagebox.showinfo('app creator','This app is created by Sajjad Hoseini & all rights reserved.')

menubar= Menu(root)
creditmenu=Menu(menubar,tearoff=0)
creditmenu.add_command(label='How to use the app?',command=app_guide)
creditmenu.add_separator()
creditmenu.add_command(label='Credit',command=app_creator)
menubar.add_cascade(label='Menu',menu=creditmenu)
root.config(menu=menubar)

textbox = Text(root,height=10,width=36)
#textbox.place(x=10,y=380)
textbox.pack(side='left',fill=Y)
scroll_bar=Scrollbar(root)
#scroll_bar.place(x=302,y=380)
scroll_bar.pack(side='right',fill=Y)
textbox.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=textbox.yview)

def browse_pic():
    filename = filedialog.askopenfilename(
        initialdir="/",  # Optional: Set initial directory
        title="Select a File",
        filetypes=[("", ("*.png","*.jpg","*.jpeg"))]  # Optional: Filter file types
    )

    if filename:
        p_entry.delete(0,END)
        p_entry.insert(0,filename)

p_var=StringVar()
p_entry=Entry(root,textvariable=p_var,width=50)
p_entry.place(x=10,y=35)
ttk.Button(root, text="Choose your watermark photo", command=browse_pic).place(x=10,y=10)

def browse_files_folder():
    folder_dir = filedialog.askdirectory(
        initialdir="/",  # Optional: Set initial directory
    )
    if folder_dir:
        op_entry.delete(0,END)
        op_entry.insert(0,folder_dir)
        
op_var=StringVar()
op_entry=Entry(root,textvariable=op_var,width=50)
op_entry.place(x=10,y=90)
ttk.Button(root, text="Choose your pictures' folder path", command=browse_files_folder).place(x=10,y=65)

def browse_folder_to_save():
    folder_dir = filedialog.askdirectory(
        initialdir="/",  # Optional: Set initial directory
    )
    if folder_dir:
        wp_entry.delete(0,END)
        wp_entry.insert(0,folder_dir)
        
wp_var=StringVar()
wp_entry=Entry(root,textvariable=wp_var,width=50)
wp_entry.place(x=10,y=145)
ttk.Button(root, text="Choose a folder path to save watermarked images", command=browse_folder_to_save).place(x=10,y=120)

Label(root,text='Position of Watermark:').place(x=10,y=175)
pos_var=StringVar()
position=ttk.Combobox(root,width=47,textvariable=pos_var)
position['values']=('top left','top center','top right',
                    'center left','center','center right',
                    'bottom left','bottom center','bottom right')
position.place(x=10,y=195)
position.current(8)

Label(root,text='Margin:').place(x=10,y=225)
mar_var=IntVar()
Spinbox(root,width=48,from_=0, to=100,textvariable=mar_var).place(x=10,y=245)

Label(root,text='If you want to resize the watermark photo,\nfill the entries below:',justify='left').place(x=10,y=275)
x_var=IntVar()
Label(root,text='Enter width:').place(x=10,y=310)
Entry(root,textvariable=x_var,width=50).place(x=10,y=330)

y_var=IntVar()
Label(root,text='Enter height:').place(x=10,y=350)
Entry(root,textvariable=y_var,width=50).place(x=10,y=370)

def watermark():
    t1 = time.time()
    folder_path = op_var.get()
    watermarked_pics_path=wp_var.get()
    pos=pos_var.get()
    margin=mar_var.get()
    watermark_path=p_var.get()
    new_width = x_var.get()
    new_height = y_var.get()
    wphoto = Image.open(watermark_path)
    watermark_width, watermark_height = wphoto.size
    if new_width==0 and new_height!=0:
        wphoto = wphoto.resize((watermark_width, new_height))
        watermark_width, watermark_height = watermark_width, new_height
    elif new_width!=0 and new_height==0:
        wphoto = wphoto.resize((new_width, watermark_height))
        watermark_width, watermark_height = new_width, watermark_height
    elif new_width!=0 and new_height!=0:
        wphoto = wphoto.resize((new_width, new_height))
        watermark_width, watermark_height = new_width, new_height
    i=1
    image_extensions = ('.jpg', '.JPG','.JPEG','.jpeg','png','PNG')
    length = len(os.listdir(folder_path))
    textbox.configure(state=NORMAL)
    textbox.delete('1.0',END)
    textbox.tag_configure('left',justify='left',font=('Times New Roman',10))
    textbox.insert(END,length)
    textbox.insert(END,'\n')
    textbox.tag_add('left',1.0,'end')
    root.update()
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            im = Image.open(image_path)
            width, height = im.size
            if pos=='top left':
                x = margin
                y = margin
            elif pos=='top center':
                x = (width//2)-(watermark_width//2)
                y = margin
            elif pos=='top right':
                x = width - (watermark_width + margin)
                y = margin
            elif pos=='center left':
                x = margin
                y = (height//2)-(watermark_height//2)
            elif pos=='center':
                x = (width//2)-(watermark_width//2)
                y = (height//2)-(watermark_height//2)
            elif pos=='center right':
                x = width - (watermark_width + margin)
                y = (height//2)-(watermark_height//2)
            elif pos=='bottom left':
                x = margin
                y = height - (watermark_height + margin)
            elif pos=='bottom center':
                x = (width//2)-(watermark_width//2)
                y = height - (watermark_height + margin)
            elif pos=='bottom right':
                x = width - (watermark_width + margin)
                y = height - (watermark_height + margin)

            im.paste(wphoto, (x, y))
            im.save(f'{watermarked_pics_path}\watermarked_{filename}')
            percent = round((i/length*100),2)
            textbox.insert(END,f'{filename}, Percentage completed: {percent}%')
            textbox.insert(END,'\n')
            textbox.tag_add('left',1.0,'end')
            i+=1
            root.update()
    t2 = time.time()
    exec_time = round(t2-t1,2)
    textbox.insert(END,f'Execution time: {exec_time} seconds')
    textbox.tag_add('left',1.0,'end')
    textbox.configure(state=DISABLED)
    root.update()

ttk.Button(root ,text = "WaterMark" ,command=watermark).place(x=115,y=400)

root.mainloop()

#author: Sajjad Hoseini
