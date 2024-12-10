import flet as ft

# Values for the visual identity of the pages
table_buttons_separation_width = 10 # The width of the empty space between the table and the side buttons on the main page
table_buttons_separation_height = 17 # The height of the empty space between the table and the side buttons on the main page
table_buttons_top_separation = 53 # The height of the empty space between the table and the side buttons on the main page
column_widths = [100, 250, 200, 200, 80]  # Widths of the columns of the data table in pixels
std_button_width = 250 # The width of all the buttons in all windows except 'Back' buttons, (value in pixels)
std_button_color = "#2C3E50" # The color of all the buttons in all windows and the warnings toggle
alt_button_color = "#015214" # The color of the export to excel button
std_button_text_color = "#EEEEF6" # The color of the text of all the buttons in all windows
alt_button_text_color = "#EEF6EE" # The color of the text of the export to excel button
std_button_height = 50 # The height of all the buttons in all windows
std_dropdown_width = 300 # The width of all the dropdowns in all windows except
tables_padding = ft.padding.only(left=30, right=30, bottom=30) # Padding of all the tables in the pages
expanded_spacing_width = 20 # The width of the empty space between the buttons and the table in the main page
std_spacing_width = 40 # The width of the empty space between components in all pages

# Class for the buttons like "Analyze by Fleet", "Fleet Component Analysis", etc.
# Provides an ft.ElevatedButton with preset colors and size
class Std_button_cl(ft.ElevatedButton):

    def __init__(self,text,on_click,is_export=False):
        super().__init__()
        self.width = std_button_width
        self.height = std_button_height
        self.bgcolor = std_button_color if not is_export else alt_button_color
        self.color = std_button_text_color if not is_export else alt_button_text_color
        self.text = text
        self.on_click = on_click

# Class for the toggle that can switch between showing all indications or only warnings
class Show_warnings_toggle_cl(ft.Switch):
    def update_me(self, state):
        self.value = state
    def __init__(self,on_change,init_state):
        super().__init__()
        self.label="  Show both alarms and warnings"
        self.value= init_state # By default, only warnings are shown
        self.active_color=std_button_color  # Match button color
        self.label_position=ft.LabelPosition.RIGHT # On which side of the toggle will the label appear
        self.on_change = on_change
    def text(self,*args):
        if self.value == True:
            return '1'
        else:
            return '2'

# Class for dropdown with time interval options that will be used in all pages
class Time_interval_selector_cl (ft.Dropdown):
        def __init__(self,on_change):
            super().__init__()
            self.on_change = on_change
            self.label="Time interval selector"
            self.width= std_dropdown_width
            self.options=[ # Options' text must be exactly as written because of logic module's handling
                ft.dropdown.Option("In last week"),
                ft.dropdown.Option("In last 2 weeks"),
                ft.dropdown.Option('In last 3 weeks'),
                ft.dropdown.Option("Last month"),
                ft.dropdown.Option("Last 2 months"),
                ft.dropdown.Option('Last 3 months')]
                # If you modify these you must also modify the logic module

# Class for dropdown with fleet options that will be used in all pages
class Fleet_selector_cl (ft.Dropdown):
    def __init__(self,on_change):
        super().__init__()
        self.on_change = on_change
        self.label="Fleet selector"
        self.width=std_dropdown_width
        self.options=[ # Options' text must be exactly as written because of logic module's handling
            ft.dropdown.Option("All"),
            ft.dropdown.Option("All Siemens Vehicles"),
            ft.dropdown.Option("All Stadler Vehicles"),
            ft.dropdown.Option("FLIRT 3 GABY"),  # Stadler
            ft.dropdown.Option("GABW Stadler FLIRT3 EMU3"), # Stadler
            ft.dropdown.Option("GABW Stadler FLIRT3 EMU4"),
            ft.dropdown.Option("GABW Stadler FLIRT3 EMU5"),
            ft.dropdown.Option("GABW Stadler FLIRT3 EMU6"),
            ft.dropdown.Option("GABW Stadler FLIRT3 EMU9"),
            ft.dropdown.Option("Siemens Desiro GABY"), # Siemens
            ft.dropdown.Option("Siemens Mireo GABY"), # Siemens
            # If you modify these you must also modify the logic module
        ]

# Class for dropdown with vehicle options that will be used in all pages
class Vehicle_selector_cl (ft.Dropdown):
    '''    ft.dropdown.Option("All"),

            # Siemens Desiro GABY trains
            ft.dropdown.Option("2462.001"), ft.dropdown.Option("2462.002"), ft.dropdown.Option("2462.003"),
            ft.dropdown.Option("2462.004"), ft.dropdown.Option("2462.005"), ft.dropdown.Option("2462.006"), 
            ft.dropdown.Option("2462.007"), ft.dropdown.Option("2462.008"), ft.dropdown.Option("2462.009"),
            ft.dropdown.Option("2462.010"), ft.dropdown.Option("2462.011"), ft.dropdown.Option("2462.012"),

            # Siemens Mireo GABY
            ft.dropdown.Option("2463.001"), ft.dropdown.Option("2463.002"), ft.dropdown.Option("2463.003"),
            ft.dropdown.Option("2463.004"), ft.dropdown.Option("2463.005"), ft.dropdown.Option("2463.006"),
            ft.dropdown.Option("2463.007"), ft.dropdown.Option("2463.008"), ft.dropdown.Option("2463.009"),
            ft.dropdown.Option("2463.010"), ft.dropdown.Option("2463.011"), ft.dropdown.Option("2463.012"),
            ft.dropdown.Option("2463.013"), ft.dropdown.Option("2463.014"), ft.dropdown.Option("2463.015"),
            ft.dropdown.Option("2463.016"), ft.dropdown.Option("2463.017"), ft.dropdown.Option("2463.018"),
            ft.dropdown.Option("2463.019"), ft.dropdown.Option("2463.020"), ft.dropdown.Option("2463.021"),
            ft.dropdown.Option("2463.022"), ft.dropdown.Option("2463.023"), ft.dropdown.Option("2463.024"),
            ft.dropdown.Option("2463.025"), ft.dropdown.Option("2463.026"), ft.dropdown.Option("2463.027"),
            ft.dropdown.Option("2463.028"), ft.dropdown.Option("2463.029"), ft.dropdown.Option("2463.030"),
            ft.dropdown.Option("2463.031"), ft.dropdown.Option("2463.032"), ft.dropdown.Option("2463.033"),
            ft.dropdown.Option("2463.034"), ft.dropdown.Option("2463.035"), ft.dropdown.Option("2463.036"),
            ft.dropdown.Option("2463.037"), ft.dropdown.Option("2463.038"), ft.dropdown.Option("2463.039"),
            ft.dropdown.Option("2463.040"), ft.dropdown.Option("2463.041"), ft.dropdown.Option("2463.042"),
            ft.dropdown.Option("2463.043"), ft.dropdown.Option("2463.044"),

            # FLIRT 3 EMU 3 GABW
            ft.dropdown.Option("3.01"), ft.dropdown.Option("3.02"), ft.dropdown.Option("3.03"),
            ft.dropdown.Option("3.04"), ft.dropdown.Option("3.05"), ft.dropdown.Option("3.06"),
            ft.dropdown.Option("3.07"), ft.dropdown.Option("3.08"), ft.dropdown.Option("3.09"),
            ft.dropdown.Option("3.10"), ft.dropdown.Option("3.11"), ft.dropdown.Option("3.12"),
            ft.dropdown.Option("3.13"),

            # FLIRT 3 EMU 4 GABW
            ft.dropdown.Option("4.01"), ft.dropdown.Option("4.02"), ft.dropdown.Option("4.03"),
            ft.dropdown.Option("4.04"), ft.dropdown.Option("4.05"), ft.dropdown.Option("4.06"),
            ft.dropdown.Option("4.07"), ft.dropdown.Option("4.08"), ft.dropdown.Option("4.09"),

            # FLIRT 3 GABY
            ft.dropdown.Option("4.20"), ft.dropdown.Option("4.21"), ft.dropdown.Option("4.22"),
            ft.dropdown.Option("4.23"), ft.dropdown.Option("4.24"), ft.dropdown.Option("4.25"),
            ft.dropdown.Option("4.26"), ft.dropdown.Option("4.27"), ft.dropdown.Option("4.28"),
            ft.dropdown.Option("4.29"), ft.dropdown.Option("4.30"), ft.dropdown.Option("4.31"),
            ft.dropdown.Option("4.32"), ft.dropdown.Option("4.33"), ft.dropdown.Option("4.34"),
            ft.dropdown.Option("4.35"), ft.dropdown.Option("4.36"), ft.dropdown.Option("4.37"),
            ft.dropdown.Option("4.38"),

            # FLIRT 3 EMU 5 GABW
            ft.dropdown.Option("5.01"), ft.dropdown.Option("5.02"), ft.dropdown.Option("5.03"),
            ft.dropdown.Option("5.04"), ft.dropdown.Option("5.05"), ft.dropdown.Option("5.06"),
            ft.dropdown.Option("5.07"), ft.dropdown.Option("5.08"), ft.dropdown.Option("5.09"),
            ft.dropdown.Option("5.10"), ft.dropdown.Option("5.11"), ft.dropdown.Option("5.12"),
            ft.dropdown.Option("5.13"), ft.dropdown.Option("5.14"), ft.dropdown.Option("5.15"),
            ft.dropdown.Option("5.16"), ft.dropdown.Option("5.17"), ft.dropdown.Option("5.18"),
            ft.dropdown.Option("5.19"),

            # FLIRT 3 EMU 6 GABW
            ft.dropdown.Option("6.01"), ft.dropdown.Option("6.02"), ft.dropdown.Option("6.03"),
            ft.dropdown.Option("6.04"), ft.dropdown.Option("6.05"), ft.dropdown.Option("6.06"),
            ft.dropdown.Option("6.07"), ft.dropdown.Option("6.08"), ft.dropdown.Option("6.09"),
            ft.dropdown.Option("6.10"), ft.dropdown.Option("6.11"), ft.dropdown.Option("6.12"),
            ft.dropdown.Option("6.13"), ft.dropdown.Option("6.14"),

            # FLIRT 3 EMU 9 GABW
            ft.dropdown.Option("9.01"), ft.dropdown.Option("9.02"), ft.dropdown.Option("9.03"),
            ft.dropdown.Option("9.04"), ft.dropdown.Option("9.05"), ft.dropdown.Option("9.06"),
            ft.dropdown.Option("9.07"), ft.dropdown.Option("9.08"), ft.dropdown.Option("9.09"),
            ft.dropdown.Option("9.10"), ft.dropdown.Option("9.11")

            # If you modify these you must also modify the logic module'''
    def DesiroGabyVeh(self,*args):
        self.options.extend([ft.dropdown.Option("2462.001"), ft.dropdown.Option("2462.002"), ft.dropdown.Option("2462.003"),
            ft.dropdown.Option("2462.004"), ft.dropdown.Option("2462.005"), ft.dropdown.Option("2462.006"), 
            ft.dropdown.Option("2462.007"), ft.dropdown.Option("2462.008"), ft.dropdown.Option("2462.009"),
            ft.dropdown.Option("2462.010"), ft.dropdown.Option("2462.011"), ft.dropdown.Option("2462.012")])
    
    def MireoGabyVeh(self,*args):
        self.options.extend([ft.dropdown.Option("2463.001"), ft.dropdown.Option("2463.002"), ft.dropdown.Option("2463.003"),\
            ft.dropdown.Option("2463.004"), ft.dropdown.Option("2463.005"), ft.dropdown.Option("2463.006"),\
            ft.dropdown.Option("2463.007"), ft.dropdown.Option("2463.008"), ft.dropdown.Option("2463.009"),\
            ft.dropdown.Option("2463.010"), ft.dropdown.Option("2463.011"), ft.dropdown.Option("2463.012"),\
            ft.dropdown.Option("2463.013"), ft.dropdown.Option("2463.014"), ft.dropdown.Option("2463.015"),\
            ft.dropdown.Option("2463.016"), ft.dropdown.Option("2463.017"), ft.dropdown.Option("2463.018"),\
            ft.dropdown.Option("2463.019"), ft.dropdown.Option("2463.020"), ft.dropdown.Option("2463.021"),\
            ft.dropdown.Option("2463.022"), ft.dropdown.Option("2463.023"), ft.dropdown.Option("2463.024"),\
            ft.dropdown.Option("2463.025"), ft.dropdown.Option("2463.026"), ft.dropdown.Option("2463.027"),\
            ft.dropdown.Option("2463.028"), ft.dropdown.Option("2463.029"), ft.dropdown.Option("2463.030"),\
            ft.dropdown.Option("2463.031"), ft.dropdown.Option("2463.032"), ft.dropdown.Option("2463.033"),\
            ft.dropdown.Option("2463.034"), ft.dropdown.Option("2463.035"), ft.dropdown.Option("2463.036"),\
            ft.dropdown.Option("2463.037"), ft.dropdown.Option("2463.038"), ft.dropdown.Option("2463.039"),\
            ft.dropdown.Option("2463.040"), ft.dropdown.Option("2463.041"), ft.dropdown.Option("2463.042"),\
            ft.dropdown.Option("2463.043"), ft.dropdown.Option("2463.044")])

    def Flirt3Emu3Veh(self,*args):
        self.options.extend( [ft.dropdown.Option("3.01"), ft.dropdown.Option("3.02"), ft.dropdown.Option("3.03"),\
            ft.dropdown.Option("3.04"), ft.dropdown.Option("3.05"), ft.dropdown.Option("3.06"),\
            ft.dropdown.Option("3.07"), ft.dropdown.Option("3.08"), ft.dropdown.Option("3.09"),\
            ft.dropdown.Option("3.10"), ft.dropdown.Option("3.11"), ft.dropdown.Option("3.12"),\
            ft.dropdown.Option("3.13")])
            
    def Flirt3Emu4Veh(self,*args):
        self.options.extend( [ft.dropdown.Option("4.01"), ft.dropdown.Option("4.02"), ft.dropdown.Option("4.03"),\
            ft.dropdown.Option("4.04"), ft.dropdown.Option("4.05"), ft.dropdown.Option("4.06"),\
            ft.dropdown.Option("4.07"), ft.dropdown.Option("4.08"), ft.dropdown.Option("4.09")])
    
    def Flirt3GabyVeh(self,*args):
        self.options.extend([ft.dropdown.Option("4.20"), ft.dropdown.Option("4.21"), ft.dropdown.Option("4.22"),\
            ft.dropdown.Option("4.23"), ft.dropdown.Option("4.24"), ft.dropdown.Option("4.25"),\
            ft.dropdown.Option("4.26"), ft.dropdown.Option("4.27"), ft.dropdown.Option("4.28"),\
            ft.dropdown.Option("4.29"), ft.dropdown.Option("4.30"), ft.dropdown.Option("4.31"),\
            ft.dropdown.Option("4.32"), ft.dropdown.Option("4.33"), ft.dropdown.Option("4.34"),\
            ft.dropdown.Option("4.35"), ft.dropdown.Option("4.36"), ft.dropdown.Option("4.37"),\
            ft.dropdown.Option("4.38")])

    def Flirt3Emu5Veh(self,*args):
        self.options.extend([ft.dropdown.Option("5.01"), ft.dropdown.Option("5.02"), ft.dropdown.Option("5.03"),\
            ft.dropdown.Option("5.04"), ft.dropdown.Option("5.05"), ft.dropdown.Option("5.06"),\
            ft.dropdown.Option("5.07"), ft.dropdown.Option("5.08"), ft.dropdown.Option("5.09"),\
            ft.dropdown.Option("5.10"), ft.dropdown.Option("5.11"), ft.dropdown.Option("5.12"),\
            ft.dropdown.Option("5.13"), ft.dropdown.Option("5.14"), ft.dropdown.Option("5.15"),\
            ft.dropdown.Option("5.16"), ft.dropdown.Option("5.17"), ft.dropdown.Option("5.18"),\
            ft.dropdown.Option("5.19")])
    
    def Flirt3Emu6Veh(self,*args):
        self.options.extend( [ft.dropdown.Option("6.01"), ft.dropdown.Option("6.02"), ft.dropdown.Option("6.03"),\
            ft.dropdown.Option("6.04"), ft.dropdown.Option("6.05"), ft.dropdown.Option("6.06"),\
            ft.dropdown.Option("6.07"), ft.dropdown.Option("6.08"), ft.dropdown.Option("6.09"),\
            ft.dropdown.Option("6.10"), ft.dropdown.Option("6.11"), ft.dropdown.Option("6.12"),\
            ft.dropdown.Option("6.13"), ft.dropdown.Option("6.14")])

    def Flirt3Emu9Veh(self,*args):
        self.options.extend([ft.dropdown.Option("9.01"), ft.dropdown.Option("9.02"), ft.dropdown.Option("9.03"),\
            ft.dropdown.Option("9.04"), ft.dropdown.Option("9.05"), ft.dropdown.Option("9.06"),\
            ft.dropdown.Option("9.07"), ft.dropdown.Option("9.08"), ft.dropdown.Option("9.09"),\
            ft.dropdown.Option("9.10"), ft.dropdown.Option("9.11")])
    
    # This function will update vehicle options according to fleet
    # for example, if user selected fleet Emu4, no need to display the option
    # to then filter by vehicle from Emu5 for exapmle.
    def fleet_resolver(self,fleet,*args):
        print("In fleet resolver")
        print(fleet)
        self.options=[ft.dropdown.Option('All')] # Remove all of the old options
        
        if fleet == 'All': # These strings fleet is being compared to must be from fleet_selector_cl
            self.DesiroGabyVeh()
            self.MireoGabyVeh()
            self.Flirt3Emu3Veh()
            self.Flirt3Emu4Veh()
            self.Flirt3GabyVeh()
            self.Flirt3Emu5Veh()
            self.Flirt3Emu6Veh()
            self.Flirt3Emu9Veh()
        elif fleet == "All Siemens Vehicles":
            print("In all siemens vehicles")
            self.DesiroGabyVeh()
            self.MireoGabyVeh()
        elif fleet == "All Stadler Vehicles":
            print("In all stadler vehicles")
            self.Flirt3Emu3Veh()
            self.Flirt3Emu4Veh()
            self.Flirt3GabyVeh()
            self.Flirt3Emu5Veh()
            self.Flirt3Emu6Veh()
            self.Flirt3Emu9Veh()
        elif fleet == "FLIRT 3 GABY":
            self.Flirt3GabyVeh()
        elif fleet == "GABW Stadler FLIRT3 EMU3":
            self.Flirt3Emu3Veh()
        elif fleet == "GABW Stadler FLIRT3 EMU4":
            self.Flirt3Emu4Veh()
        elif fleet == "GABW Stadler FLIRT3 EMU5":
            self.Flirt3Emu5Veh()
        elif fleet == "GABW Stadler FLIRT3 EMU6":
            self.Flirt3Emu6Veh()
        elif fleet == "GABW Stadler FLIRT3 EMU9":
            self.Flirt3Emu9Veh()
        elif fleet == "Siemens Desiro GABY":
            self.DesiroGabyVeh()
        elif fleet == "Siemens Mireo GABY":
            self.MireoGabyVeh()
    


    def __init__(self,on_change,fleet):
        super().__init__()
        self.on_change = on_change
        self.label="Vehicle selector"
        self.width=std_dropdown_width
        self.options=[]
        self.fleet_resolver(fleet)
        

class Snack_bar_cl(ft.SnackBar): # Used for notifying the user when data update is in progress
    def __init__(self,text,dur=12345):
        super().__init__(
        bgcolor=std_button_color,
        content=ft.Text(f'                  {text}',size=18),
        duration=dur,)
