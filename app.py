import gradio as gr
import csv, jinja2, os, sys
from paypal import Paypal
from gls import GLS
from pathlib import Path
from io import StringIO 

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout

templateLoader = jinja2.FileSystemLoader(searchpath="./template")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template("camt.053.xml.j2")

def convert_to_camt_053(file):
    if not file:
        return None, None
    outfile_name = f"{Path(file.name).stem}.xml"
    with Capturing() as output:
        model = Paypal(file.name).transaction_model()
        if model == None:
            model = GLS(file.name).transaction_model()
        if model == None:
            return f"ERROR: Not a valid Paypal or GLS csv:\n  {Path(file.name).stem}{Path(file.name).suffix}", None
    
    out_xml = template.render(model)
    outfile = f"{os.path.dirname(file.name)}/{outfile_name}"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(out_xml)
    return  '\n'.join(output), outfile


demo = gr.Interface(fn=convert_to_camt_053, 
                    inputs=[gr.File(file_types=['.csv'])], 
                    outputs=[gr.Text(show_label=False, container=False), 
                             gr.File(file_types=['.xml'], label='camt.053.xml')],
                    title="Erdlinge e.V. Paypal+GLS csv to camt.053.xml converter",
                    allow_flagging="never",
                    live=True)
    
demo.queue().launch(share=False)   
