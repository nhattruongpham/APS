import smbus
import time

#name = "Nam"
I2C_ADDR = 0x27
LCD_WIDTH = 16

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08   #on
#LCD_BACKLIGHT = 0x00  #off

ENABLE = 0b00000100

E_PULSE = 0.0005
E_DELAY = 0.0005

#bus = smbus.SMBus(0) # Pi Rev 1
bus = smbus.SMBus(1) # Pi Rev 2


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # ban xem lai nhung lenh co ban o Buoc 2
  lcd_byte(0x32,LCD_CMD) # 
  lcd_byte(0x06,LCD_CMD) # 
  lcd_byte(0x0C,LCD_CMD) # 
  lcd_byte(0x28,LCD_CMD) # 
  lcd_byte(0x01,LCD_CMD) # 
  time.sleep(E_DELAY)

# gui 1 byte xuong LCD
def lcd_byte(bits, mode):
	bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
	bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
	#che do 4 bits: gui byte cao truoc byte thap sau
	# byte cao
	bus.write_byte(I2C_ADDR, bits_high)
	lcd_toggle_enable(bits_high)

	# byte thap
	bus.write_byte(I2C_ADDR, bits_low)
	lcd_toggle_enable(bits_low)

# dua chan E len cao roi thap de truyen du lieu di
def lcd_toggle_enable(bits):
	bus.write_byte(I2C_ADDR, (bits | ENABLE))
	time.sleep(E_PULSE)
	bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
	time.sleep(E_DELAY)

# gui chuoi ki tu xuong LCD
def lcd_string(message,line):
	message = message.ljust(LCD_WIDTH," ")
	lcd_byte(line, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)
	time.sleep(2)

lcd_init()
#while True:
	#lcd_string("Hello Raspi: " + name, LCD_LINE_1)
	#time.sleep(3)