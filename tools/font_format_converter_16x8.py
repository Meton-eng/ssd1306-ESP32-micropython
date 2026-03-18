## Script to read files with n lines like this:
##     { 0x1E, 0x33, 0x33, 0x3E, 0x30, 0x18, 0x0E, 0x00},   // U+0039 (9)
##        { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,  },       //0x00, 
## and writes an output file with n lines like this:
## fonte8x8 = [
##     ( 0x1E, 0x33, 0x33, 0x3E, 0x30, 0x18, 0x0E, 0x00),   # Unicode 0x (9)
##             ]
## 
## v0 - Initial version:
##      hardcoded filename
##      only changes the type and format of the byte list
## v1 - Evolved version:
##      transposes bytes from horizontal to vertical format   


name_source_file = 'font_16x8.c'
name_destination_file = 'font_16x8_transpose.py'


## Transposes byte direction. The 8 bits of b0 become byte 0, b1 become byte 1, etc.
def invert_bytes(original_list):
    original_list = bytearray([])
    for a in original_list:
        original_list.append( int( a.strip(), 16) )
        
    list_transp_bytes = bytearray([0] * 16)

    for i in range(8):
        for j in range(8):            
            if ((original_list[i] >> (7 - j) ) & 1):
                list_transp_bytes[(j)] |= (1 << i )
     
    # lower page: rows 8-15 → bytes 8-15 of the result
    for i in range(8):
        for j in range(8):
            if (original_list[i + 8] >> (7 - j)) & 1:
                list_transp_bytes[j + 8] |= (1 << i)
                
    return ([f'{b:#04x}' for b in list_transp_bytes])

## open source file and get a list of lines — each line is one font character
with open(name_source_file, 'r') as obj_source_file:
    lst_formato_c = obj_source_file.readlines()  

## initialize output with Python format header
linhas_formato_py = [('fonte_16x8 = [\n')]

## iterate over each line
for linha in lst_formato_c:
    # split line into 3 parts
    parts = linha.strip().strip('{').partition('}') 
    
    # part 0 contains the byte sequence
    seq_bytes = invert_bytes(parts[0].strip(' ,').split(','))
    
    # part 2 contains the character comment — part 1 is just '}', unused
    coment_caracter = parts[2].strip(' ,').replace('//','  # ').replace(',','')
    
    # build Python-format line and append to output list
    converted_line = (
                '    ( ' + 
                ( ', '.join(seq_bytes) ) + 
                '),' + 
                coment_caracter + 
                '\n'
               )
    linhas_formato_py.append(converted_line)
                       
## join list into a single string for writing
str_py_format = ''.join(linhas_formato_py) + ' ]'


with open(name_destination_file, 'w') as obj_destination_file:
    obj_destination_file.write(f'{str_py_format}')