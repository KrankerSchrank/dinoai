import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.theme() as table_theme:
    with dpg.theme_component(dpg.mvTable):
        # dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (255, 0, 0, 100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

def clb_selectable(sender, app_data, user_data):
    return user_data

def render(self, board):

    with dpg.window(tag="Selectable Tables"):
        with dpg.table(tag="SelectCells", header_row=False) as selectablecells:
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            for i in range(9):
                with dpg.table_row():
                    for j in range(9):
                        if i < 3: a = 0
                        elif i <6: a = 1
                        else: a = 0
                        if j < 3: b = 0
                        elif j <6: b = 1
                        else: b = 0

                        if i == 0 or i == 3 or i == 7: c = 0
                        elif i == 1 or i == 4 or i == 8: c = 1
                        else: c = 2
                        if j == 0 or j == 3 or j == 7: d = 0
                        elif j == 1 or j == 4 or j == 8: d = 1
                        else: d = 2
                        text = "#" if board[a][b][c][d] == " " else board[a][b][c][d]
                        dpg.add_selectable(label=f"{text}", callback=self.clb_selectable, user_data=(a, b, c, d))
                if i == 2 or i == 5:
                    with dpg.table_row():
                        for j in range(9):
                            dpg.add_selectable(label=f"---", callback=self.clb_selectable, user_data=(99,99))
        dpg.bind_item_theme(selectablecells, table_theme)

    dpg.create_viewport(width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
