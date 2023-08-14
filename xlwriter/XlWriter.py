import xlsxwriter
from datetime import date

class Writer : 
    
    def __init__(self, file_name : str) :
        self.wb = xlsxwriter.Workbook(file_name)

    def add_worksheet(self, w_name : str, data : list[tuple], header : list[str]) : 
        ws = self.wb.add_worksheet(w_name)
        
        for col, i in enumerate(header): 
            ws.write(0, col, i)  

        for i, d in enumerate(data) : 
            for j, c in enumerate(d) : 
                if type(c) == date : 
                    c= str(c)
                ws.write(i+1, j, c)


    def finish_task(self) :
        self.wb.close()


