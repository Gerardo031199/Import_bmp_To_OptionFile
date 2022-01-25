from tkinter import filedialog

class FLAG:
    def __init__(self, bpp, palette, data):
        self.bpp = bpp
        self.palette = palette
        self.data = data
        self.convertPalette()
        self.convertData()
        
    def convertPalette(self): #convierte la paleta, invierte 80 por FF      

        for i in range(3,len(self.palette),4): #Solo toma los bytes de transparencia
            value = self.palette[i]*2
            if value >= 256: #Si el valor es mayor o igual a 256 se resta 1 al valor
                value = value-1
            elif value <= 0: #Si no el valor es menor o igual al 0 se queda en 0
                value = 0
            self.palette[i] = value

        if self.bpp >= 8: #Si la profundidad de bits es mayor o igual a 8 bpp se convierte de BGRA -> RGBA
            self.palette[::4], self.palette[2::4] = self.palette[2::4], self.palette[::4] #BGRA -> RGBA


    def convertData(self):
        data_2 = b''
        for i in range(0,len(self.data),64): #Iteraciones cada 64 bytes
            data_2 +=(self.data[i:i+64][::-1]) #Bytes en reversa
            
        self.data = data_2

def main():          
    file = filedialog.askopenfile(title='Select file',mode='rb',filetypes = [("bmp files",".bmp"),("all files",".*")])
    if file:
        file_name = file.name
        content = bytearray(file.read())

        width= int.from_bytes(content[18:21], byteorder='little', signed=False)
        height= int.from_bytes(content[22:25], byteorder='little', signed=False)

        bpp = content[28]#Profundidad de bits

        palette_offset = 58 #Comienza la paleta (Empieza en el byte 54 pero se omite el primer color = 4 bytes)
        palette_size = 1020 # 255*4 entries Longitud de la paleta
        palette = content[palette_offset:palette_offset+palette_size]

        data_offset = int.from_bytes(content[10:12], byteorder='little', signed=False)
        data_size = int.from_bytes(content[34:36], byteorder='little', signed=False)

        data = content[data_offset:data_offset+data_size][::-1]
        
        my_flag = FLAG(bpp, palette, data,)
        with open('Escudo.bin','w+b') as escudo:
            escudo.write(my_flag.palette)
            escudo.write(my_flag.data)

main()
