import wave
#a module for reading .wav files in python

def encode(txt: str, file_name: str):
	audio = wave.open(file_name ,mode="rb")
 	#opens the file in the variable audio
	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
	#gets all audio frames and stores them as bytes
	txt = txt + int((len(frame_bytes)-(len(txt)*8*8))/8) *'#'
 	#converts message to a single bit to replace lsb of audio with 
	bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in txt])))
	#adds all bits of text to this variable
	for i, bit in enumerate(bits):
		frame_bytes[i] = (frame_bytes[i] & 254) | bit
	#uses an and logic gate on each bit of audio and adds the bit from text
	frame_modified = bytes(frame_bytes)
	newAudio =  wave.open('Encoded.wav', 'wb')
	#opens and creates a new audio file
	newAudio.setparams(audio.getparams())
	#adds the same info on original wav file to new, for example authour
	newAudio.writeframes(frame_modified)
	#writes the encoded audio to the file
	newAudio.close()
	audio.close()
	#closes both original and new file

encode("Not a rickroll", "Music.wav")

def decode(file_name: str):
	audio = wave.open(file_name, mode='rb')
	#opens encoded file
	frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
	#reads all the frames of audio
	extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
	#loops through all frames
	txt = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
	#stores all final (least significant) bits in a string
	decoded = txt.split("###")[0]
	#removes extra bits
	print(f"Message is {decoded}")
	#prints message to terminal

decode("Encoded.wav")
