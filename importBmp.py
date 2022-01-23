from tkinter import filedialog

class FLAG:
    def __init__(self, palette, data):
        self.palette = None
        self.data = None

    def setPalette(self, palette):
        self.palette = palette
        
    def setData(self, data):
        self.data = data
        
    def convertPalette(self): #convierte la paleta, invierte 80 por FF      
        d = self.palette

        for i in range(3,len(d),4): #Solo toma los bytes de transparencia
            value = d[i]*2
            if value >= 256: #Si el valor es mayor o igual a 256 se resta 1 al valor
                value = value-1
            elif value <= 0: #Si no el valor es mejor o igual al 0 se queda en 0
                value = 0
            d[i] = value

        if bpp >= 8: #Si la profundidad de bits es mayor o igual a 8 bpp se convierte de BGRA -> RGBA
            d[::4], d[2::4] = d[2::4], d[::4] #BGRA -> RGBA

        self.palette = d

    def convertData(self):
        data_1 = data[::-1]
        
        data_2 = b''
        for i in range(0,len(data_1),64): #Iteraciones cada 64 bytes
            data_2 +=(data_1[i:i+64][::-1]) #Bytes en reversa
            
        self.data = data_2

def writeData():
    my_flag = FLAG(palette,data)

    my_flag.setPalette(palette)
    my_flag.convertPalette()

    my_flag.setData(data)
    my_flag.convertData()

    
    with open('Escudo.bin','w+b') as escudo:
        escudo.write(palette)
        escudo.write(data)
        

file = filedialog.askopenfile(title='Select file',mode='rb',filetypes = [("bmp files","*.bmp"),("all files","*.*")])
if file:
    file_name = file.name
    content = bytearray(file.read())

    width= int.from_bytes(content[18:21], byteorder='little', signed=False)
    height= int.from_bytes(content[22:25], byteorder='little', signed=False)

    #print(width,height)

    bpp = content[28]#Profundidad de bits

    palette_offset = 58 #Comienza la paleta (Empieza en el byte 54 pero se omite el primer color = 4 bytes)
    palette_size = 1020 # 255*4 entries Longitud de la paleta
    palette = content[palette_offset:palette_offset+palette_size]

    data_offset = int.from_bytes(content[10:12], byteorder='little', signed=False)
    data_size = int.from_bytes(content[34:36], byteorder='little', signed=False)

    data = content[data_offset:data_offset+data_size]
    
    writeData()
