import struct
import io
import os

objectNames = [
		"Attribute",
		"Button",
		"Display",
		"Edit",
		"SmoothMeshShape",
		"SmoothMeshShape.texture",
		"SmoothMeshShape.vertexPositions",
		"TextShape",
		"Transformation",
		"Node",
		"Widget",
		"ScrollButton",
		"ScrollSlider",
		"ArrayAttribute",
		"PopUpButton",
		"ListWidget",
		"Texture",]

CONST_OBFU_KEY = bytearray([0x5c, 0xcd, 0xc7, 0x5e, 0x0b, 0x26, 0x3a, 0xfb])
def DeobfuscateData(data):
    data_size = len(data)
    key = CONST_OBFU_KEY

    first_bytes_as_uint32 = struct.unpack('I', key[0:4])[0]
    key_offset = first_bytes_as_uint32 % data_size

    output = bytearray(data_size)
    for i in range(data_size):
        cur = data[i]
        out_idx = (key_offset+i)%data_size
        key_idx = out_idx%8
        cur_key = key[key_idx]
        out_byte = (cur - cur_key) & 0xff
        output[out_idx] = out_byte

    return output

def GetChunkName(data):
	chunk_bytes = None
	if data != b'PlasmaGraphics' and data != b'Seal':
		chunk_bytes = DeobfuscateData(data)
	else:
		chunk_bytes = data

	return chunk_bytes.decode('utf-8')

class BasicChunk(object):
	def __init__(self, id, data):
		self.id = id
		self.data = data

	@classmethod 
	def ReadFrom(cls, rdr):
		id = struct.unpack('I', rdr.read(4))[0]
		data_size = struct.unpack('I', rdr.read(4))[0]
		data = rdr.read(data_size)
		return cls(id, data)
	"""
	def WriteTo(self, wtr, id=None):
		wtr.write(struct.pack('I', id or self.id))
		wtr.write(struct.pack('I', len(self.data)))
		wtr.write(self.data)
		oid = id or 0
		return oid + 1
	"""
	
class PLX(object):
	def __init__(self, file_name):
		self.id_type_map = {}
		self.file_name = file_name

	def __enter__(self):
		self.fd = open(self.file_name, 'rb')
		return self

	def __exit__(self, type, value, traceback):
		self.fd.close()

	def print_tree(self):
		self.do_tree(self.fd, os.fstat(self.fd.fileno()).st_size)

	def do_tree(self, rdr, data_size, indent_level=0):
		indent = '\t' * indent_level

		while rdr.tell() != data_size:
			chunk = BasicChunk.ReadFrom(rdr)
			if chunk.id == 0:
				name_def = BasicChunk.ReadFrom(io.BytesIO(chunk.data))
				clean_name = GetChunkName(name_def.data)
				self.id_type_map[name_def.id] = clean_name


				print(indent + 'Define Type(ID:{}, Name:{})'.format(name_def.id, clean_name))

			else:
				type_name = self.id_type_map.get(chunk.id, "< Referencing unknown type: {}>".format(chunk.id))
				print(indent + 'Data chunk. Type(ID:{}, Name:{})'.format(chunk.id, type_name))

				if type_name in objectNames:
					self.do_tree(io.BytesIO(chunk.data), len(chunk.data), indent_level+1)


def main():
	with PLX('gui.plx') as plx:
		plx.print_tree()

if __name__ == '__main__':
	main()
