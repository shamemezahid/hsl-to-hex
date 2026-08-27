import re
import sys
from pathlib import Path


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """
    Converts HSL color values to a hexadecimal string (#RRGGBB).
    """
    s_norm = max(0.0, min(100.0, s)) / 100.0
    l_norm = max(0.0, min(100.0, l)) / 100.0
    h_norm = h % 360.0

    c = (1.0 - abs(2.0 * l_norm - 1.0)) * s_norm
    x = c * (1.0 - abs((h_norm / 60.0) % 2.0 - 1.0))
    m = l_norm - c / 2.0

    if 0 <= h_norm < 60:
        r_prime, g_prime, b_prime = c, x, 0.0
    elif 60 <= h_norm < 120:
        r_prime, g_prime, b_prime = x, c, 0.0
    elif 120 <= h_norm < 180:
        r_prime, g_prime, b_prime = 0.0, c, x
    elif 180 <= h_norm < 240:
        r_prime, g_prime, b_prime = 0.0, x, c
    elif 240 <= h_norm < 300:
        r_prime, g_prime, b_prime = x, 0.0, c
    else:
        r_prime, g_prime, b_prime = c, 0.0, x

    r = round((r_prime + m) * 255)
    g = round((g_prime + m) * 255)
    b = round((b_prime + m) * 255)

    return f"#{r:02X}{g:02X}{b:02X}"


def convert_file(input_path: str = "hsl.txt", output_path: str = "hex.txt"):
    # Regex matches space-separated or comma-separated CSS hsl values, with optional 'deg'
    # Examples: hsl(210deg 100% 98.43%), hsl(211.18deg, 95.49%, 26.08%), hsl(0deg 0% 98.82%)
    pattern = re.compile(
        r'hsl\(\s*([\d.]+)(?:deg)?[\s,]+([\d.]+)%[\s,]+([\d.]+)%\s*\)',
        re.IGNORECASE
    )

    def replace_match(match: re.Match) -> str:
        h = float(match.group(1))
        s = float(match.group(2))
        l = float(match.group(3))
        return hsl_to_hex(h, s, l)

    input_file = Path(input_path)
    if not input_file.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    content = input_file.read_text(encoding="utf-8")
    converted_content = pattern.sub(replace_match, content)

    output_file = Path(output_path)
    output_file.write_text(converted_content, encoding="utf-8")
    print(f"Successfully converted '{input_path}' -> '{output_path}'")


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "hsl.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "hex.txt"
    convert_file(in_file, out_file)

