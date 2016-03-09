from PIL import Image

im = Image.open("extracted.bmp")
pix = im.load()
width, height = im.size

extracted_bits = []
for y in range(height):
	for x in range(width):
		r, g, b = pix[(x,y)]
		extracted_bits.append(r & 1)
		extracted_bits.append(g & 1)
		extracted_bits.append(b & 1)

extracted_byte_bits = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]
with open("extracted2.bmp", "wb") as out:
	for byte_bits in extracted_byte_bits:
                byte_str = ''.join(str(x) for x in byte_bits)
		byte = chr(int(byte_str, 2))
		out.write(byte)



