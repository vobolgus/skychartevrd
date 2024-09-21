from generate_report import generate_latex_report
from compile_report import compile_latex_to_pdf
import os
import subprocess
import shutil

def generate_skychart(lat, lon, skychart_filename, tex_filename, output_directory, number, contours, messier=None, stars=None):
    visible_messier_names, visible_stars = generate_latex_report(lat, lon, skychart_filename, output_filename=tex_filename, number=number, contours=contours, messier=messier, stars=stars)
    
    # Компиляция LaTeX в PDF
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            
            # Компиляция LaTeX в PDF
        subprocess.run(
                ["pdflatex", f"-output-directory={output_directory}", tex_filename],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
        )
        return visible_messier_names, visible_stars
    except subprocess.CalledProcessError as e:
            return
