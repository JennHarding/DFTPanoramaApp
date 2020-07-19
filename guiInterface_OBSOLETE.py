import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import  FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

from pandastable import Table, TableModel
import pandas as pd

from Corpus import full_corpus
from CalculationFunctions import score_to_data
import visuals as vis

LARGE_FONT = ("Verdana", 16)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
style.use("ggplot")
score_data = "none"
master_df = "none"

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()
    
    



class PanoramaGenerator(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "DFT Panorama Generator")
        
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda : popupmsg("Not functional yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        goto_menu = tk.Menu(menubar, tearoff=1)
        goto_menu.add_command(label="Home", command=lambda: self.show_frame(StartPage))
        goto_menu.add_command(label="Magnitudes", command=lambda: self.show_frame(MagnitudePage))
        goto_menu.add_command(label="Individual Components", command=lambda: self.show_frame(ComponentPage))
        menubar.add_cascade(label="Go To", menu=goto_menu)
        
        tk.Tk.config(self, menu=menubar)
        
        
        self.frames = {}
        
        for F in (StartPage, MagnitudePage, ComponentPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.show_frame(StartPage)
        

    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    
    
        

class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="DFT Panorama Generator.", font=LARGE_FONT)
        label.grid(row=0, column=0, columnspan=5)

        rep_label = ttk.Label(self, text="Select Repertoire")
        rep_label.grid(row=1, column=0)
        rep = tk.StringVar()
        rep_select = ttk.OptionMenu(self, rep, *full_corpus)
        rep_select.grid(row=1, column=1, columnspan=3, sticky="we", pady=20)
             
        
        def switch():
            if beg_select["state"] == tk.DISABLED:
                beg_select["state"] = tk.NORMAL
                end_select["state"] = tk.NORMAL
            else:
                beg_select["state"] = tk.DISABLED
                end_select["state"] = tk.DISABLED
        
        exc = tk.BooleanVar()
        exc_select = tk.Checkbutton(self, text="Use Excerpt", variable=exc, command=switch)
        exc_select.grid(row=2, column=0)
        
        beg_label = tk.Label(self, text="Begin in Measure:")
        beg_label.grid(row=2, column=1)
        beg = tk.IntVar()
        beg_select = tk.Entry(self, textvariable=beg, state=tk.DISABLED)
        beg_select.grid(row=2, column=2)
        end_label = tk.Label(self, text="End in Measure:")
        end_label.grid(row=3, column=1)
        end = tk.IntVar()
        end_select = tk.Entry(self, textvariable=end, state=tk.DISABLED)
        end_select.grid(row=3, column=2)
                
        window_label = tk.Label(self, text="Window Size:")
        window_label.grid(row=4, column=0)
        win_size = tk.IntVar()
        win_size.set(16)
        win_size_select = tk.Entry(self, textvariable=win_size)
        win_size_select.grid(row=4, column=1, pady=20)
        
        strategy_label = tk.Label(self, text="PC Counting\n Strategy:")
        strategy_label.grid(row=5, column=0)
        strat = tk.StringVar()
        strat.set("Onset")
        strats = ["Onset", "Duration", "Flat"]
        for i, s in enumerate(strats, 1):
            strat_select = ttk.Radiobutton(self, text=s, variable=strat, value=s)
            strat_select.grid(row=5, column=i, sticky="w")
        
        log_label = tk.Label(self, text="Weighting")
        log_label.grid(row=6, column=0)
        log = tk.BooleanVar()
        log.set(True)
        log_select = tk.Checkbutton(self, text="Use Log Weighting \n (Recommended)", variable=log)
        log_select.grid(row=6, column=1, pady=20)

        
        def calculate_dft():
            global master_df
            config = {
                "Repertoire": rep.get(),
                "Excerpt": exc.get(),
                "Excerpt Measures": (beg.get(), end.get()),
                "Window Size": win_size.get(),
                "Strategy": strat.get(),
                "Log Weighting": log.get()
            }
            score_data = score_to_data(config.values())
            master_df = vis.make_dataframes(score_data=score_data)

            
        
        calculate = ttk.Button(self, text="Calculate", command=calculate_dft)
        calculate.grid(row=7, column=0, columnspan=4, sticky="we")
              
        

class MagnitudePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # label = tk.Label(self, text="All Fourier Magnitudes", font=LARGE_FONT)
        # label.grid(row=0, column=1, columnspan=3)
        self.make_empty_graph()
        self.make_empty_dataframe()
        
        
    def make_empty_graph(self):
        fig = Figure(figsize=(10,2.5))
        sub = fig.add_subplot(111)
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget()
        canvas.get_tk_widget().grid(row=3, column=0, sticky="we", columnspan=3)
        
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=2, column=0, sticky="w")
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.pack()
        
        graph_button = ttk.Button(self, text="Generate Graph", command=lambda: self.make_mag_graph(canvas=canvas, sub=sub))
        graph_button.grid(row=0, column=0, sticky="w")
        
    def make_mag_graph(self, canvas, sub):
        global master_df
        sub.clear()
        for i in range(1, 7):
            sub.stackplot(range(len(master_df[f'f{i} Magnitude'])), 
                    master_df[f'f{i} Magnitude'], 
                    color=vis.xkcd_colors[f'f{i}_colors'][0],
                    alpha=0.4,
                    labels=[f'f{i} Magnitude'])
            sub.margins(x=0) 

        # sub.legend(loc="center left", bbox_to_anchor=(1, 0.5), borderaxespad=0, fancybox=True, shadow=True, prop={'size': 7})
        sub.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), borderaxespad=0, fancybox=True, shadow=True, prop={'size': 7}, ncol=6)
        canvas.draw()
        
        

    def make_empty_dataframe(self):
        empty_df = pd.DataFrame({})
        frame = tk.Frame(self)
        frame.grid(row=4, column=0, sticky="we", columnspan=3)
        pt = Table(frame, showtoolbar=True, showstatusbar=True, dataframe=empty_df)
        pt.show()
        
        df_button = ttk.Button(self, text="Show Magnitude Data", command=lambda: self.make_mag_data(table=pt))
        df_button.grid(row=1, column=0, sticky="w")       
        
        
    def make_mag_data(self, table):
        global master_df
        df = table.model.df
        df['Window Number'] = master_df['Window Number']
        df['Measure Range'] = master_df['Measure Range']
        df['Original Array'] = master_df['Original Array']
        for i in range(1, 7):
            df[f'f{i}'] = master_df[f'f{i} Magnitude']
        pd.set_option('display.max_colwidth', 40)
        table.redraw()
        

class ComponentPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.var = tk.IntVar()
        self.make_empty_graph()
        self.make_empty_dataframe()
               
        for i in range(1, 7):
            comp_button = ttk.Radiobutton(self, text=f'f{i}', variable=self.var, value=i)
            comp_button.grid(row=(i-1)%2, column=(i-1)//2 + 1)
        
    def make_empty_graph(self):
        fig = Figure(figsize=(10,2.5))
        sub_left = fig.add_subplot(111)
        sub_right = sub_left.twinx()
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget()
        canvas.get_tk_widget().grid(row=4, column=0, sticky="we", columnspan=7)
        
        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=3, column=0, sticky="w", columnspan=7)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.pack()
               
        graph_button = ttk.Button(self, text="Generate Graph", command=lambda: self.make_component_graph(canvas=canvas, left=sub_left, right=sub_right))
        graph_button.grid(row=0, column=0, sticky = "w")

    def make_component_graph(self, canvas, left, right):
        global master_df
        left.clear()
        right.clear()
        i = self.var.get()
        right.stackplot(range(len(master_df[f'f{i} Magnitude'])), 
                    master_df[f'f{i} Magnitude'], 
                    color=vis.xkcd_colors[f'f{i}_colors'][0],
                    alpha=0.3,
                    labels=[f'f{i} Magnitude'])
        right.grid(b=False)
        right.margins(x=0) 
        
        left.plot(range(len(master_df[f'f{i} Phase'])),
                   master_df[f'f{i} Phase'],
                   color=vis.xkcd_colors[f'f{i}_colors'][1],
                   label=f'f{i} Phase',
                   )
        left.plot(range(len(master_df[f'f{i} Quantized Phase'])),
                   master_df[f'f{i} Quantized Phase'],
                   color=vis.xkcd_colors[f'f{i}_colors'][2],
                   label=f'f{i} Quantized Phase',
                   )
        left.set_yticks(ticks=range(-180,210,30))
        left.grid(axis='x')
        left.margins(x=0)

        left.legend(loc="lower center", bbox_to_anchor=(0.5, 1.02), borderaxespad=0, fancybox=True, shadow=True, prop={'size': 7}, ncol=2)
        canvas.draw()
    
    
    def make_empty_dataframe(self):
        empty_df = pd.DataFrame({})
        frame = tk.Frame(self)
        frame.grid(row=5, column=0, columnspan=7, sticky="we")
        pt = Table(frame, showtoolbar=True, showstatusbar=True, dataframe=empty_df)
        pt.show()
        
        df_button = ttk.Button(self, text="Show Component Data", command=lambda: self.make_component_data(table=pt))
        df_button.grid(row=1, column=0, sticky = "w")
        
        
    def make_component_data(self, table):
        global master_df
        i = self.var.get()
        df = table.model.df
        df['Window Number'] = master_df['Window Number']
        df['Measures'] = master_df['Measure Range']
        df['Original Array'] = master_df['Original Array']
        df['Magnitude'] = master_df[f'f{i} Magnitude']
        df['Phase'] = master_df[f'f{i} Phase']
        df['Quantized Phase'] = master_df[f'f{i} Quantized Phase']
    
        table.redraw()



app = PanoramaGenerator()
# app.geometry("1280x720")
app.geometry("1024x768")
# app['bg'] = '#DBE0DF'

# makeGraph()
app.mainloop()