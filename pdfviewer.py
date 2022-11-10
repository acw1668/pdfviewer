import tkinter as tk
import fitz

class PDFViewerTk(tk.Frame):
    def __init__(self, master=None, **kw):
        file = kw.pop('file', None)
        factor = kw.pop('factor', None)
        super().__init__(master, **kw)
        self._viewer = tk.Text(self, bg='gray', spacing3=5)
        self._xscrollbar = tk.Scrollbar(self, orient='horizontal', command=self._viewer.xview)
        self._yscrollbar = tk.Scrollbar(self, orient='vertical', command=self._viewer.yview)
        self._viewer.config(xscrollcommand=self._xscrollbar.set, yscrollcommand=self._yscrollbar.set)
        
        self._viewer.grid(row=0, column=0, sticky='nsew')
        self._xscrollbar.grid(row=1, column=0, sticky='ew')
        self._yscrollbar.grid(row=0, column=1, sticky='ns')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        if file:
            self.open(file, factor)

    def open(self, file, factor=None):
        doc = fitz.open(file)
        mat = fitz.Matrix(factor, factor) if factor else None
        self._images = []
        self._viewer.delete('1.0', 'end')
        self._read(doc, mat)
    
    def _read(self, doc, mat=None, n=0):
        try:
            page = doc.load_page(n)
            pix = page.get_pixmap(matrix=mat)
            if pix.alpha:
                pix = fitz.Pixmap(pix, 0)
            imgdata = pix.tobytes('ppm')
            tkimg = tk.PhotoImage(data=imgdata)
            self._viewer.image_create('end', image=tkimg)
            self._viewer.insert('end', '\n')
            self._images.append(tkimg)
            self.after(5, self._read, doc, mat, n+1)
        except Exception as e:
            #print(e)
            pass

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        print(f'Usage: python {sys.argv[0]} <filename>')
        sys.exit(0)
    factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1
    root = tk.Tk()
    viewer = PDFViewerTk(root, width=800, height=800, file=sys.argv[1], factor=factor)
    viewer.pack(fill='both', expand=1)
    root.mainloop()
