import PySimpleGUI as sg
from libgen_api import LibgenSearch
import webbrowser

def split_list(lst):
    mid = len(lst)
    return lst[:mid], lst[mid:]

def search_downloads_by_author(author_name):
    search = LibgenSearch()
    results = search.search_title(author_name)


    if results:
        if len(results) <= 10:
            book_layout = [[sg.Text(f"Downloads found for author '{author_name}':")]]
            for i, book in enumerate(results):
                book_layout.append([sg.Radio(f"{i + 1}. {book['Title']}", "book_radio", key=f"-BOOK{i}-")])
        else:
            book_layout_left, book_layout_right = split_list(results)

            book_layout = [
                [
                    sg.Column(
                        [[sg.Text(f"Downloads found for author '{author_name}':")]] + \
                        [[sg.Radio(f"{i + 1}. {book['Title']}", "book_radio", key=f"-BOOK{i}-")] for i, book in enumerate(book_layout_left)],
                        element_justification="left"
                        
                    ),
                    sg.Column(
                        [[sg.Text("")]] + \
                        [[sg.Radio(f"{i + 1 + len(book_layout_left)}. {book['Title']}", "book_radio", key=f"-BOOK{i + len(book_layout_left)}-")] for i, book in enumerate(book_layout_right)],
                        element_justification="left"
                    )
                ]
            ]

        layout = [
            [sg.Column(book_layout, element_justification="left", size=(500, 500),scrollable=True)],
            [sg.Button("Generate", bind_return_key=True), sg.Button("Exit")]
        ]

        window = sg.Window("Book Downloader", layout)

        while True:
            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, "Exit"):
                break

            if event == "Generate":
                selected_book_index = next((i for i, val in enumerate(values.values()) if val), None)
                if selected_book_index is not None:
                    selected_book = results[selected_book_index]
                    links = [value for key, value in selected_book.items() if key.startswith("Mirror") and value]
                    link_layout = [[sg.Text("Download Links:")]]
                    for i, link in enumerate(links):
                        print(link)
                        link_layout.append([sg.Button(f"Mirror {i+1}", key=f"{link}", size=(10, 1))])

                    link_window = sg.Window("Download Links", link_layout)
                    while True:
                        event, values = link_window.read()
                        if event in (sg.WINDOW_CLOSED,):
                            break
                        if event.startswith(""):
                            webbrowser.open(event)

                    link_window.close()
                
        window.close()
    else:
        sg.popup(f"No downloads found for author '{author_name}'.")

# GUI layout
layout = [
    [sg.Text("Enter author name:")],
    [sg.Input(key="-AUTHOR-")],
    [sg.Button("Search", bind_return_key=True)]
]

# Create the window
window = sg.Window("Book Downloader", layout)

# Event loop
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    if event == "Search":
        author_name = values["-AUTHOR-"]
        search_downloads_by_author(author_name)

window.close()
