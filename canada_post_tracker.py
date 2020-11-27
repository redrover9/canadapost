from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import tkinter as tk
from tkinter import Frame
from tkinter import messagebox
class App(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets()
        super().__init__()
    def make_widgets(self):
        self.winfo_toplevel().title("Package Tracker")
 
        tk.Label(self, text="Enter a tracking number to check whether a package has been delivered: ", name="myLabel").grid(row=0, column=0)
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1)
 
        btn = tk.Button(self, text="Submit", command=self.on_submit)
        btn.grid(row=2, column=0, columnspan=2, sticky="ew")
 
    def on_submit(self):
        inputNum = self.entry.get()
        os.environ['MOZ_HEADLESS'] = '1'
        driver = webdriver.Firefox("/usr/local/bin/")
        driver.get("https://www.canadapost.ca/cpc/en/home.page")
        assert "Canada Post" in driver.title
        trackingNumber = driver.find_element_by_name("trackingNumber")
        trackingNumber.clear()
        trackingNumber.send_keys(inputNum)
        #7060220906288741
        #7060220551634771
        trackingNumber.send_keys(Keys.RETURN)
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "track_package_result_details")))
            assert "Notice card" in driver.page_source
            tk.messagebox.showinfo("Attention", "The package has been delivered.")
        except AssertionError:
            tk.messagebox.showerror("Attention", "The package has not yet been delivered.")
        except TimeoutException:
            tk.messagebox.showerror("Attention", "The package has not yet been delivered.")
        driver.close()
 
 
if __name__ == '__main__':
    App().mainloop()
