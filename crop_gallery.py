from PIL import Image, ImageOps
import os

GALLERY_DIR = 'images/galeria'

def aggressive_crop(im):
    # Convert to RGB to ensure standard mode
    im = im.convert('RGB')
    
    # Convert to grayscale
    gray = im.convert('L')
    
    # Invert (so white becomes black, and we look for non-black bbox)
    # But wait, usually bbox looks for non-zero.
    # So if background is white (255), we want to make it 0.
    # Invert: White(255) -> 0. Dark content -> >0.
    inverted = ImageOps.invert(gray)
    
    # Threshold: anything "darker" than tolerance remains, anything "lighter" (background) becomes 0.
    # Since we inverted: 
    # Original White (255) -> Inverted (0). 
    # Original Light Gray (240) -> Inverted (15).
    # We want to treat 0-20 as "background" (0). 
    # So using 'point': if x < threshold: 0 else 255.
    threshold = 30 # Tolerance for "how distinct from white"
    
    # We want to keep pixels that were originally DARK.
    # Original Dark (0) -> Inverted (255).
    # So in inverted version, "signal" is high values. "Noise/Background" is low values.
    # We set low values to 0.
    
    cleaned = inverted.point(lambda x: 0 if x < threshold else 255)
    
    bbox = cleaned.getbbox()
    
    if bbox:
        # Add a small padding if possible so we don't cut too tight?
        # User wants "perfeito", usually tight is better for object-fit covers.
        return im.crop(bbox)
    return im

def process_gallery_images():
    print("Iniciando processamento agressivo de imagens...")
    processed_count = 0
    
    if not os.path.exists(GALLERY_DIR):
        print(f"Diretoria {GALLERY_DIR} não encontrada.")
        return

    for filename in os.listdir(GALLERY_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(GALLERY_DIR, filename)
            try:
                im = Image.open(filepath)
                original_size = im.size
                
                trimmed_im = aggressive_crop(im)
                
                # Check if we actually cropped significantly
                if trimmed_im.size != original_size:
                    # Sanity check: don't crop to empty or tiny
                    if trimmed_im.size[0] > 50 and trimmed_im.size[1] > 50:
                        print(f"Recortando {filename}: {original_size} -> {trimmed_im.size}")
                        trimmed_im.save(filepath)
                        processed_count += 1
                    else:
                        print(f"Crop muito agressivo detectado em {filename}, ignorando.")
                else:
                    print(f"Sem alterações (aparentes) em {filename}")
                    
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

    print(f"Concluído. {processed_count} imagens processadas.")

if __name__ == "__main__":
    process_gallery_images()
