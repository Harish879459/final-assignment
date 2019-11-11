from tkinter import *
from tkinter import ttk
import mysql.connector as mc
from tkinter import messagebox as mb


def add_info():
    try:
        std_id = int(entry_id.get())
        name = entry_name.get()
        address = entry_address.get()
        number = entry_number.get()
        degree = entry_degree.get()

        query = 'insert into my_table(id, name, address, number, degree) values(%s, %s, %s, %s, %s)'
        values = (std_id, name, address, number, degree)
        db_cursor.execute(query, values)
        mb.showinfo("Data inserted successfully.")
        connector.commit()
        clear()
        show()

    except ValueError as err:
        print(err)

    except mc.IntegrityError as err:
        print(err)


def partition(arr, low, high):
    if combo_sort.get() == 'Id':
        column = 0
    elif combo_sort.get() == 'Name':
        column = 1
    elif combo_sort.get() == 'Address':
        column = 2
    elif combo_sort.get() == 'Number':
        column = 3
    else:
        column = 4
    i = (low - 1)  # index of smaller element
    pivot = arr[high][column]  # pivot
    for j in range(low, high):
        if arr[j][column] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)

# Function to do Quick sort
def quickSort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(arr, low, pi - 1)
        quickSort(arr, pi + 1, high)


def sort():
    db_cursor.execute('select * from my_table')
    array = db_cursor.fetchall()
    quickSort(array, 0, len(array) - 1)

    student_table.delete(*student_table.get_children())

    for row in array:
        student_table.insert('', 'end', values=row)


def clear():
    entry_id.config(state='normal')
    entry_search.delete(0, END)
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    entry_address.delete(0, END)
    entry_number.delete(0, END)
    entry_degree.delete(0, END)


def show():
    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    query = 'select * from my_table'
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    for row in results:
        student_table.insert('', 'end', values=row)


def search(mylist=None):
    if not mylist:
        query = "select * from my_table"
        db_cursor.execute(query)
        results = db_cursor.fetchall()
    else:
        results = mylist

    records = student_table.get_children()

    for element in records:
        student_table.delete(element)

    target = entry_search.get()


    if combo_search.get() == 'Id':
        column = 0
        if target.isdigit():
            target = int(target)
        else:
            return
    elif combo_search.get() == 'Name':
        column = 1
    elif combo_search.get() == 'Address':
        column = 2
    elif combo_search.get() == 'Number':
        column = 3
    else:
        column = 4

    found = []
    for row in results:
        if target == row[column]:
            found.append(row)

    for row in found:
        student_table.insert('', 'end', values=row)

    return found


def update():
    try:
        name = entry_name.get()
        address = entry_address.get()
        number = entry_number.get()
        degree = entry_degree.get()

        query = 'update my_table set name=%s, address=%s, number=%s, degree=%s where id=%s'
        values = (name, address, number, degree, pointer())
        db_cursor.execute(query, values)
        connector.commit()
        clear()
        show()

    except ValueError as err:
        print(err)


def delete():
    query = 'delete from my_table where id=%s'
    values = (pointer(),)
    db_cursor.execute(query, values)
    connector.commit()
    show()
    clear()


def pointer():
    try:
        clear()
        point = student_table.focus()

        content = student_table.item(point)
        row = content['values']
        entry_id.insert(0, row[0])
        entry_name.insert(0, row[1])
        entry_address.insert(0, row[2])
        entry_number.insert(0, row[3])
        entry_degree.insert(0, row[4])
        return row[0]

    except IndexError:
        pass


try:
    connector = mc.connect(user='root', passwd='root', host='localhost', database='school')
    db_cursor = connector.cursor()
    db_cursor.execute('create table if not exists my_table(id int not null,'
                      'name varchar(40), address varchar(50), number varchar(13), degree varchar(40),'
                      'constraint pk_id primary key(id))')

except mc.DatabaseError as err:
    print(err)

root = Tk()
root.title("STUDENT MANAGEMENT SYSTEM")
root.geometry('900x750+400+80')
root.configure(bg="grey")

# Frames
top_frame = Frame(root)
top_frame.configure(bg="grey")
top_frame.pack()


show_frame = Frame(root, width=200, height=100, relief=RIDGE, bd=4)
show_frame.configure(bg="grey")
show_frame.pack()



combo_search = ttk.Combobox(top_frame, width=32, font='bold 12')
combo_search['values'] = ('Id', 'Name', 'Address', 'Number', 'Degree')
combo_search.set("Id")
combo_search.grid(row=0, column=1, pady=8)

combo_sort = ttk.Combobox(top_frame, width=32, font='bold 12')
combo_sort['values'] = ('Id', 'Name', 'Address', 'Number', 'Degree')
combo_sort.set("Id")
combo_sort.grid(row=1, column=1, pady=8)


# widgets
lbl_search = Label(top_frame, text="Search", font='Arial 16', bg='grey')
lbl_sort = Label(top_frame, text="Sort", font='Arial 16', bg='grey')
lbl_id = Label(top_frame, text="ID :-", font='Arial 16', bg='grey')
lbl_name = Label(top_frame, text="Name :-", font='Arial 16', bg='grey')
lbl_address = Label(top_frame, text="Address :-", font='Arial 16', bg='grey')
lbl_number = Label(top_frame, text="Number:-", font='Arial 16', bg='grey')
lbl_degree = Label(top_frame, text="Degree :-", font='Arial 16', bg='grey')


lbl_search.grid(row=0, column=0, padx=8, pady=8)
lbl_sort.grid(row=1, column=0, padx=8, pady=8)

entry_search = Entry(top_frame, width=15, font='bold 12')
entry_search.grid(row=0, column=2, padx=15, pady=8)
btn_search = Button(top_frame, width=8, text='Search', font='bold 12', command=search, bg="dark green")
btn_search.grid(row=0, column=3, padx=20, pady=20)
btn_sort = Button(top_frame, width=8, text='Sort', font='bold 12', command=sort, bg="dark green")
btn_sort.grid(row=1, column=2, padx=20, pady=20)

lbl_id.grid(row=4, column=0, padx=15, pady=8)
lbl_name.grid(row=5, column=0, padx=15, pady=8)
lbl_address.grid(row=6, column=0, padx=15, pady=8)
lbl_number.grid(row=7, column=0, padx=15, pady=8)
lbl_degree.grid(row=8, column=0, padx=15, pady=8)

# Entry

entry_id = Entry(top_frame, width=28, font='bold 14')
entry_name = Entry(top_frame, width=28, font='bold 14')
entry_address = Entry(top_frame, width=28, font='bold 14')
entry_number = Entry(top_frame, width=28, font='bold 14')
entry_degree = Entry(top_frame, width=28, font='bold 14')

entry_search.bind('<Return>', lambda e: search())

entry_id.grid(row=4, column=1, padx=15, pady=8)
entry_name.grid(row=5, column=1, padx=15, pady=8)
entry_address.grid(row=6, column=1, padx=15, pady=8)
entry_number.grid(row=7, column=1, padx=15, pady=8)
entry_degree.grid(row=8, column=1, padx=15, pady=8)

# button
btn_add = Button(top_frame, width=10, text='Add', font='Times 14', command=add_info, bg="dark green")
btn_show = Button(top_frame, width=10, text='Show', font='Times 14', command=show, bg="dark green")
btn_delete = Button(top_frame, width=10, text='Delete', font='Times 14', command=delete,fg="red", bg="dark green")
btn_update = Button(top_frame, width=10, text='Update', font='Times 14', command=update, bg="dark green")
btn_clear = Button(top_frame, width=10, text='Clear', font='Times 14', command=clear, bg="dark green")


btn_add.grid(row=4, column=2, padx=20, pady=20)
btn_show.grid(row=5, column=2, padx=20, pady=20)
btn_delete.grid(row=8, column=2, padx=20, pady=20)
btn_update.grid(row=6, column=2, padx=20, pady=20)
btn_clear.grid(row=7, column=2, padx=20, pady=20)

# Tree view
scroll_x = Scrollbar(show_frame, orient=HORIZONTAL)
scroll_y = Scrollbar(show_frame, orient=VERTICAL)

student_table = ttk.Treeview(show_frame, column=('id', 'name', 'address', 'number', 'degree'), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
student_table.pack()

student_table.column('id', width=110)
student_table.column('name', width=110)
student_table.column('address', width=110)
student_table.column('number', width=110)
student_table.column('degree', width=110)
student_table['show'] = 'headings'

student_table.heading('id', text='ID', anchor=W)
student_table.heading('name', text='Name', anchor=W)
student_table.heading('address', text='Address', anchor=W)
student_table.heading('number', text='Number', anchor=W)
student_table.heading('degree', text='Degree', anchor=W)

scroll_x.config(command=student_table.xview)
scroll_y.config(command=student_table.yview)
student_table.bind('<ButtonRelease-1>', lambda e: pointer())


if __name__ == '__main__':
    root.mainloop()