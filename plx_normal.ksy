meta:
  id: plx_normal
  file-extension: PLX
  endian: le
seq:
  - id: field
    type: chunk
    repeat: eos

types:
  chunk_type_zero:
    seq:
      - id: chunk_size
        type: u4
        
      - id: unk_index_1
        type: u4
        if: true
        
      - id: chunk_str_size
        type: u4
        
        
      - id: chunk_str
        size: chunk_size -8
        
      - id: unk_index_2
        type: u4
        

  chunk:
    seq:
      - id: chunk_type
        type: u4
        
      - id: data
        type: chunk_type_zero
        if: chunk_type == 0
        
      - id: associated_data_size
        type: u4
        
      - id: associated_data
        size: associated_data_size
