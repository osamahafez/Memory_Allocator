from tkinter import *

import tkinter.simpledialog


root = Tk()
root.title("Process Allocator")
root.geometry("320x520+500+100")

class Process:
    def __init__(self):
        self.base = 0
        self.limit = 0
        self.number = 0
        self.hole_num = 0

class Hole:
    def __init__(self):
        self.base = 0
        self.limit = 0
        self.number = 0

def first_fit(h_list, alloc_list, p_list, p_num):
    found = False
    for item in p_list:
        if(int(item.number) == int(p_num)):
            for y in h_list:
                if (int(y.limit) >= int(item.limit)):
                    item.base = int(y.base)
                    item.hole_num = int(y.number)
                    y.base = int(y.base) + int(item.limit)
                    y.limit = int(y.limit) - int(item.limit)
                    alloc_list.append(item)
                    found = True
                    break
        if(found):
            break

def best_fit(h_list, alloc_list, p_list, p_num):
    my_sorted = sorted(h_list, key=lambda x: int(x.limit))
    found = False
    for item in p_list:
        if (int(item.number) == int(p_num)):
            for y in my_sorted:
                if (int(y.limit) >= int(item.limit)):
                    item.base = int(y.base)
                    item.hole_num = int(y.number)
                    y.base = int(y.base) + int(item.limit)
                    y.limit = int(y.limit) - int(item.limit)
                    alloc_list.append(item)
                    found = True
                    break
        if (found):
            break

def print_processes(my_list, main_frame):
    frame_right = Frame(main_frame)
    frame_right.pack(side=RIGHT, fill=BOTH, expand=True)
    if(my_list):
        title_right = Label(frame_right, text='Process Allocation Table')
        title_right.grid(row=0, column=0, columnspan=10, sticky=W)
        shif_down = int(0)
        for objj in my_list:
            address_right = Label(frame_right, text="base -> " + str(objj.base))
            address_right.grid(row=3+shif_down, column=0, columnspan=2, sticky=W)
            size_right = Label(frame_right, text="P" + str(objj.number) + " (size = " + str(objj.limit) + ")")
            size_right.grid(row=3+shif_down, column=2, columnspan=2, sticky=W)
            shif_down += 1

    else:
        title_right2 = Label(frame_right, text='Process Allocation Table')
        title_right2.grid(row=0, column=0, columnspan=10, sticky=W)
        empty_right = Label(frame_right, text="Table is empty")
        empty_right.grid(row=1, column=0, sticky=W)

def print_holes(my_list, main_frame, state):
    state_left = Label(main_frame, text=state)
    state_left.pack()
    frame_left = Frame(main_frame)
    frame_left.pack(side=LEFT, fill=BOTH, expand=True)
    if(my_list):
        title_left = Label(frame_left, text='Holes Allocation Table |')
        title_left.grid(row=0, column=0, columnspan=10, sticky=W)
        shif_down=int(0)
        for objj in my_list:
            if(objj.limit != 0):
                address_left = Label(frame_left, text="base -> " + str(objj.base))
                address_left.grid(row=3+shif_down, column=0, columnspan=2, sticky=W)
                size_left = Label(frame_left, text="size = " + str(objj.limit))
                size_left.grid(row=3+shif_down, column=2, columnspan=2, sticky=W)
                shif_down += 1

    else:
        title_left2 = Label(frame_left, text='Holes Allocation Table')
        title_left2.grid(row=0, column=0, columnspan=10, sticky=W)
        empty_left = Label(frame_left, text="Table is empty")
        empty_left.grid(row=1, column=0, sticky=W)

alloc_method = tkinter.simpledialog.askstring("Allocation Mehtod", "Choose:\n- first fit \n- best fit")

hole_list = []
process_list = []
allocation_done = []
ans2 = False

frame1 = Frame(root)
frame1.pack()

if(alloc_method == "first fit" or alloc_method == "best fit"):

    # ------------------ HOLE INPUTS -----------------------

    ans = "yes"
    ans2 = "yes"
    num=int(-1)
    while(ans == "yes"):
        h = Hole()
        num += int(1)
        h.base = tkinter.simpledialog.askinteger("Hole Address", "Enter hole's address")
        h.limit = tkinter.simpledialog.askinteger("Hole Size", "Enter hole's size")
        h.number = int(num) # Hole ID number
        hole_list.append(h)
        ans = tkinter.simpledialog.askstring("New Hole", "Add another hole?\n- yes  - no")

    my_state = "Initial State:"
    print_holes(hole_list, frame1, my_state)
    print_processes(allocation_done, frame1)


    #---------------------- PROCESS INPUTS ---------------------

    total_processes = tkinter.simpledialog.askinteger("Processes", "Enter total number of processes")

    for x0 in range(total_processes):
        p = Process()
        process_list.append(p)

    for x1 in range(len(process_list)):
        process_list[x1].number = x1
        process_list[x1].limit = tkinter.simpledialog.askinteger("Process Size", "Enter P"+ str(x1) + " size ")
        frame1.pack_forget()  # REMOVE TABLE
        frame1 = Frame(root)
        frame1.pack()

        if(alloc_method == "first fit"):
            first_fit(hole_list, allocation_done, process_list, x1)
        elif(alloc_method == "best fit"):
            best_fit(hole_list, allocation_done, process_list, x1)


        my_state = "After P"+str(process_list[x1].number)+" Allocation..."
        print_holes(hole_list, frame1, my_state)
        print_processes(allocation_done, frame1)

# --------------------------------------------DEALLOCATION-------------------------------------------------------------

while(ans2 == "yes"):

    dealloc_process_number =tkinter.simpledialog.askinteger("Deallocation", 'Type " 0 " to deallocate P0 and type " 1 " to deallocate P1 etc...')

    frame1.pack_forget()  # REMOVE TABLE
    frame1 = Frame(root)
    frame1.pack()

    allocation_done_copy = list(allocation_done)

    done = False
    for pro in allocation_done_copy:
        if(pro.number == dealloc_process_number):
            for hole in hole_list:
                if(pro.hole_num == hole.number):
                    hole.base = int(hole.base) - int(pro.limit)
                    hole.limit = int(hole.limit) + int(pro.limit)
                    allocation_done.remove(pro)
                    done = True
                    break
        if(done):
            break


    my_state = "After P" + str(dealloc_process_number) + " deallocation..."
    print_holes(hole_list, frame1, my_state)
    print_processes(allocation_done, frame1)

    ans2 = tkinter.simpledialog.askstring("Deallocation", "Deallocate another process?\n- yes  - no")

root.mainloop()