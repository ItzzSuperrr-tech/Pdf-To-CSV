import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from plyer import filechooser, notification
import tabula as tb
import pandas as pd
import os
import subprocess
import platform

kivy.require('2.3.0')  

class PdfToCsvApp(App):

    def build(self):
        self.pdf_path = None  # Initialize the pdf_path attribute
        return BoxLayout()

    def open_file_picker(self, instance):
        if platform.system() == 'Android':
            # For Android, use a custom file picker (requires implementation)
            self.filechooser_android()
        else:
            try:
                filechooser.open_file(filetypes=['*.pdf'], on_selection=self.on_file_selected)
            except Exception as e:
                self.root.ids.status_label.text = f'Error: {e}'

    def on_file_selected(self, selection):
        if selection:
            self.pdf_path = selection[0]
            self.root.ids.status_label.text = f'Selected file: {self.pdf_path}'
        else:
            self.root.ids.status_label.text = 'No file selected.'

    def convert_pdf_to_csv(self, instance):
        if not self.pdf_path:
            self.root.ids.status_label.text = 'No file selected.'
            return
        
        pdf_path = self.pdf_path
        csv_path = pdf_path.replace('.pdf', '.csv')

        try:
            dfs = tb.read_pdf(pdf_path, pages='all', multiple_tables=True)
            if not dfs:
                self.root.ids.status_label.text = 'No tables found in the PDF.'
                return

            combined_df = pd.concat(dfs, ignore_index=True)
            combined_df.to_csv(csv_path, index=False)
            self.root.ids.status_label.text = f'File saved to {csv_path}'

            if platform.system() == 'Windows':
                os.startfile(csv_path)
            elif platform.system() == 'Darwin':#MacOS
                subprocess.run(['open', csv_path])
            elif platform.system() == 'Linux':
                subprocess.run(['xdg-open', csv_path])
            elif platform.system() == 'Android':
                self.open_csv_file_android(csv_path)

        except Exception as e:
            self.root.ids.status_label.text = f'Error: {e}'

    def open_csv_file_android(self, csv_path):
        self.root.ids.status_label.text = f'File saved to {csv_path}. Manual opening required.'

    def filechooser_android(self):
        self.root.ids.status_label.text = 'File picker for Android is not yet implemented.'

if __name__ == '__main__':
    PdfToCsvApp().run()
    
