meta:
  id: plx_interface
  file-extension: PLX
  endian: le
  application: CubeWorld 0.1.1 / Plasma interface.plx
  # CubeWorld 0.1.1 parsing function at: 0x40cc40
  
seq:
  - id: first
    contents: [0x01, 0x00, 0x00, 0x00]

  - id: skip
    size: 4*3
    
  - id: plsama_string
    contents: "PlasmaGraphics\x00"
    
  - id: string_names_count
    type: u4
    
  - id: string_names
    type: string_name_entry
    repeat: expr
    repeat-expr: string_names_count
    if: string_names_count > 0
    
  ###########################
  # Unused in the only released interface.plx file.
  - id: unused_entries_count
    type: u4
    
  - id: unused_entries
    type: unused_entry
    repeat: expr
    repeat-expr: unused_entries_count
    if: unused_entries_count > 0
    
  ###########################
  # Unknown as to what these represent for know, but they are parsed correctly.
  - id: unk_indices_count
    type: u4
    # if <= 0, return 0
    
  - id: unk_indices
    type: unk_index_entry
    repeat: expr
    repeat-expr: unk_indices_count
    if: unk_indices_count > 0
    
    
types:
  string_name_entry:
    seq:
      - id: size
        type: u4
        # if > 512, return 0
        
      - id: buf
        type: str
        size: size
        encoding: UTF-8
        
      - id: unk1
        type: u4
  
  unused_entry:
    seq:
      - id: unk
        type: u4
        
  unk_index_entry:
    seq:
      - id: unk
        type: u4
    