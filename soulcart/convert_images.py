from PIL import Image
import os

folder = '.'
count = 0

for f in os.listdir(folder):
    if f.endswith('.avif'):
        try:
            img = Image.open(os.path.join(folder, f))
            new_name = f.replace('.avif', '.jpg')
            img.convert('RGB').save(os.path.join(folder, new_name), 'JPEG', quality=90)
            print(f'Converted: {new_name}')
            count += 1
        except Exception as e:
            print(f'Failed: {f} — {e}')

print(f'Total converted: {count}')