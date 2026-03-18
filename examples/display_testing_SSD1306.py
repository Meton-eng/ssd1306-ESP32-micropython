####################
## Simple script to test the functionalities of the SSD1306 Driver. 
####################

from machine import Pin, SoftI2C
from sensores import SSD1306
from time import sleep_ms

## ESP32 pin-up for I2C 
sda = Pin(21)
scl = Pin(22)

## declare and initialize the ESP32 I2C bus
i2c_esp32 = SoftI2C( scl = scl,
                   sda = sda,
                   freq=400_000)
                   
## declare and initialize the display
display = SSD1306(i2c_esp32)

# ## test the flash method, 2 flashes, 200ms on and 50ms off
# display.flash(8, 20000, 50)

sleep_ms(100)

## test to show the 4 lines in the display
display.limpa_tela()
display.texto('First line',  0, 24, 8)
display.texto('Second line', 0, 16, 8)
display.texto('Third line',  0,  8, 8)
display.texto('Fourth line', 0,  0, 8)
display.exibe()
sleep_ms(4000)

## test to show 3 lines using the 8x16 font
display.limpa_tela()
display.texto('First line', 0, 24, 8)
display.texto('Second line', 0, 16, 8)
display.texto('8x16 font line', 0, 0, 16)
display.exibe()
sleep_ms(4000)

## Vertical scroll by software
display.limpa_tela()

display.texto('Vertical Scroll', 0, 24, 8)
display.texto('Vertical Scroll', 0, 16, 8)
display.texto('VerticalScroll', 0, 0, 16)
display.exibe()
sleep_ms(1000)

for a in range(127):
    display.envia_comando(bytearray([0xD3, a]))
    sleep_ms(50)
    display.exibe()
display.envia_comando(bytearray([0xD3, 0]))

sleep_ms(4000)

## Horizontal scroll test using the display built in scroll functionality
display.limpa_tela()

display.texto('Horizont Scroll', 0, 24, 8)
display.texto('Horizont Scroll', 0, 16, 8)
display.texto('HorizontScroll', 0, 0, 16)
display.exibe()

sleep_ms(2000)

display.envia_comando(bytearray([
    0x2E,        # desativa scroll (obrigatório antes de configurar)
    0x26,        # scroll horizontal para direita
    0x00,        # dummy byte
    0x00,        # página inicial (0)
    0x00,        # velocidade (0x00=5 frames, mais rápido, de 0x00 ate 0x07)
    0x03,        # página final (3 = última página do 128x32)
    0x00,        # dummy byte
    0xFF,        # dummy byte
    0x2F,        # ativa scroll
]))
