from build123d import *
from build123d import Mesher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("nameplate_utils")

def generate_plate_model(name: str, surname: str, color1, color2):
    """
    Generates a 3D model of a nameplate with distinct solids for multi-color printing.
    """
    
    # Dimensions
    PLATE_L = 100.0
    PLATE_W = 50.0
    PLATE_H = 4.0
    TEXT_H = 2.0  # Height of text above plate
    RIM_H  = 1.0  # Height of rim above plate
    RIM_W = 2.0   # Width of the border rim
    
    solids_list = []

    # --- 1. Base Plate (Color 1) ---
    with BuildSketch() as base_sk:
        Rectangle(PLATE_L, PLATE_W)
        fillet(base_sk.vertices(), radius=5)
        
        # Keychain Hole (Left side)
        # Position: X=-42 (8mm from left edge), Y=0 (Centered)
        # Radius: 2.5mm (Diameter 5mm)
        with Locations((-42, 0)):
            Circle(radius=2.5, mode=Mode.SUBTRACT)
    
    base_solid = extrude(base_sk.sketch, amount=PLATE_H)
    base_solid.color = color1
    base_solid.label = "Base"
    solids_list.append(base_solid)

    # --- 2. Rim (Color 2) ---
    with BuildSketch() as rim_sk:
        # Outer shape
        rect_outer = Rectangle(PLATE_L, PLATE_W)
        fillet(rim_sk.vertices(), radius=5)
        # Inner shape (hole)
        offset(rim_sk.sketch, amount=-RIM_W, mode=Mode.SUBTRACT)
    
    rim_solid = extrude(rim_sk.sketch, amount=RIM_H)
    rim_solid = rim_solid.move(Location((0, 0, PLATE_H)))
    rim_solid.color = color2
    rim_solid.label = "Rim"
    solids_list.append(rim_solid)

    # --- 3. Text Configuration ---
    name_size = 18
    surname_size = 10
    
    # Positioning Logic
    if surname and surname.strip():
        name_pos_y = 5.0
        surname_pos_y = -10.0
    else:
        name_pos_y = 0.0
        surname_pos_y = 0.0

    # Helper function to create sophisticated text solid (Outline + Inner Face)
    # Returns tuple of lists: (rim_solids, face_solids)
    def create_text_solids(text_str, font_size, y_pos):
        if not text_str or not text_str.strip():
            return ([], [])
            
        with BuildSketch() as t_sk:
            Text(text_str, font_size=font_size, align=(Align.CENTER, Align.CENTER))
        
        text_shape = t_sk.sketch
        
        rims = []
        faces = []
        
        final_loc = Location((0, y_pos, PLATE_H))
        
        # Iterate over each letter (Face) in the text compound
        input_faces = text_shape.faces() if isinstance(text_shape, Compound) else [text_shape]
        
        for face in input_faces:
            try:
                # 2. Create Outline Solid (Color 2) for this letter
                outline_body = extrude(face, amount=TEXT_H)
                
                # 3. Create Inner Face Solid (Color 1)
                inner_body_part = None
                
                # Offset inwards using global offset function which handles holes correctly
                try:
                    # Calculate offset proportional to font size
                    offset_val = -1 * abs(font_size * 0.035) 
                    
                    offset_sk = offset(face, amount=offset_val)
                    inner_faces = offset_sk.faces()
                    
                    if not inner_faces:
                        raise ValueError("Offset resulted in empty geometry")
                        
                    # Extrude the offset face(s)
                    inner_body = extrude(inner_faces[0], amount=TEXT_H)
                    
                    # 4. Subtract Inner from Outline
                    rim_body_part = outline_body - inner_body
                    inner_body_part = inner_body
                    
                except Exception as e_offset:
                    # Fallback
                    rim_body_part = outline_body
                    inner_body_part = None

                # Position and Color
                rim_body_part = rim_body_part.move(final_loc)
                rim_body_part.color = color2
                rims.append(rim_body_part)
                
                if inner_body_part:
                    inner_body_part = inner_body_part.move(final_loc)
                    inner_body_part.color = color1
                    faces.append(inner_body_part)
                    
            except Exception as e:
                logger.warning(f"Failed to process letter in '{text_str}': {e}")
                
        return (rims, faces)

    # Generate Name Solids
    name_rims, name_faces = create_text_solids(name, name_size, name_pos_y)
    
    # Group Name parts
    if name_rims:
        name_rim_grp = Compound(children=name_rims)
        name_rim_grp.label = "Name_Outline"
        for child in name_rim_grp:
            child.color = color2
        name_rim_grp.color = color2
        solids_list.append(name_rim_grp)
        
    if name_faces:
        name_face_grp = Compound(children=name_faces)
        name_face_grp.label = "Name_Face"
        for child in name_face_grp:
            child.color = color1
        name_face_grp.color = color1
        solids_list.append(name_face_grp)
    
    # Generate Surname Solids
    surname_rims, surname_faces = create_text_solids(surname, surname_size, surname_pos_y)
    
    # Group Surname parts
    if surname_rims:
        surname_rim_grp = Compound(children=surname_rims)
        surname_rim_grp.label = "Surname_Outline"
        for child in surname_rim_grp:
            child.color = color2
        surname_rim_grp.color = color2
        solids_list.append(surname_rim_grp)
        
    if surname_faces:
        surname_face_grp = Compound(children=surname_faces)
        surname_face_grp.label = "Surname_Face"
        for child in surname_face_grp:
            child.color = color1
        surname_face_grp.color = color1
        solids_list.append(surname_face_grp)

    return Compound(children=solids_list)

def export_plate(part_compound, filepath):
    """
    Exports the compound to a 3MF file.
    """
    try:
        exporter = Mesher()
        
        def recursive_flatten(shape):
            shapes = []
            if hasattr(shape, 'children') and shape.children:
                for ch in shape.children:
                    shapes.extend(recursive_flatten(ch))
            else:
                shapes.append(shape)
            return shapes

        all_solids = recursive_flatten(part_compound)
        
        for solid in all_solids:
            exporter.add_shape(solid)
            
        exporter.write(filepath)
        print(f"Exported 3MF to: {filepath}")
        
    except Exception as e:
        print(f"Failed to export 3mf via Mesher: {e}.")
        raise e
