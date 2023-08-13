import xlsxwriter

class Writer : 
    
    def __init__(self, file_name : str) :
        self.wb = xlsxwriter.Workbook(file_name)

    def add_worksheet(self, w_name : str, data : list[tuple]) : 
        ws = self.wb.add_worksheet(w_name)

        for i, d in enumerate(data) : 
            for j, c in enumerate(d) : 
                ws.write(i, j, c)


    def finish_task(self) :
        self.wb.close()


