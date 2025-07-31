#!/usr/bin/env python3
"""
Enhanced LCD control for Lab3 - Full lab requirements
Uses professor's LCD1602.py module with alternating two-screen displays
"""
import sys
import os
import time

# Add current directory to path to find LCD1602
sys.path.insert(0, '/home/gti700lab/Lab3')

try:
    import LCD1602
except ImportError:
    print("ERROR: LCD1602 module not found", file=sys.stderr)
    sys.exit(1)

def display_text(line1="", line2=""):
    """Display text on LCD - exactly 2 lines, 16 chars each"""
    try:
        # Initialize LCD
        if not LCD1602.init(0x27, 1):
            print("ERROR: LCD init failed", file=sys.stderr)
            return False
        
     
        LCD1602.clear()
        
        # Truncate lines to 16 characters max
        line1 = str(line1)[:16]
        line2 = str(line2)[:16]
        
        
        if line1:
            LCD1602.write(0, 0, line1)
        if line2:
            LCD1602.write(0, 1, line2)
        
        print(f"LCD: '{line1}' | '{line2}'", file=sys.stderr)
        return True
        
    except Exception as e:
        print(f"LCD ERROR: {e}", file=sys.stderr)
        return False

def display_alternating_screens(screen1_line1, screen1_line2, screen2_line1, screen2_line2, duration=5.0):
    """
    Display two alternating screens
    Each screen shows for half the total duration
    """
    try:
        screen_time = duration / 2.0
        
        # Screen 1: Min/Max values
        print(f"Screen 1: '{screen1_line1}' | '{screen1_line2}'", file=sys.stderr)
        display_text(screen1_line1, screen1_line2)
        time.sleep(screen_time)
        
        # Screen 2: Average value
        print(f"Screen 2: '{screen2_line1}' | '{screen2_line2}'", file=sys.stderr)
        display_text(screen2_line1, screen2_line2)
        time.sleep(screen_time)
        
        return True
        
    except Exception as e:
        print(f"Alternating display ERROR: {e}", file=sys.stderr)
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: lcd_direct.py 'mode' [data...]")
        print("Modes: local, temp_group, humid_group, weather, full_temp, full_humid")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "local" and len(sys.argv) >= 4:
        # Local sensor: temperature, humidity
        temp = sys.argv[2]
        humid = sys.argv[3]
        display_text(f"[1] Local Data", f"{temp}C  {humid}%")
        
    elif mode == "temp_group" and len(sys.argv) >= 5:
        # Group temperature: min, max, avg
        min_temp = sys.argv[2]
        max_temp = sys.argv[3]
        avg_temp = sys.argv[4]
        display_text(f"[2] T:{min_temp}-{max_temp}C", f"Average: {avg_temp}C")
        
    elif mode == "humid_group" and len(sys.argv) >= 5:
        # Group humidity: min, max, avg
        min_humid = sys.argv[2]
        max_humid = sys.argv[3]
        avg_humid = sys.argv[4]
        display_text(f"[2] H:{min_humid}-{max_humid}%", f"Average: {avg_humid}%")
        
    elif mode == "full_temp" and len(sys.argv) >= 8:
        # Full temperature format - TWO ALTERNATING SCREENS
        # Args: min_temp, min_team, max_temp, max_team, avg_temp
        min_temp = sys.argv[2]
        min_team = sys.argv[3]
        max_temp = sys.argv[4] 
        max_team = sys.argv[5]
        avg_temp = sys.argv[6]
        
        # Screen 1: Min/Max with team numbers
        # screen1_line1 = f"[2] Tmin:{min_temp}C [{min_team}]"[:16]
        # screen1_line2 = f"Tmax:{max_temp}C [{max_team}]"[:16]
        screen1_line1 = f"[2] T-:{min_temp}C ({min_team})"[:16]
        screen1_line2 = f"T+:{max_temp}C ({max_team})"[:16]
        
        # Screen 2: Average
        screen2_line1 = f"[2] Tmoy:{avg_temp}C"[:16]
        screen2_line2 = ""
        
        # Alternate between screens
        display_alternating_screens(screen1_line1, screen1_line2, screen2_line1, screen2_line2, duration=5.0)
        
    elif mode == "full_humid" and len(sys.argv) >= 8:
        # Full humidity format - TWO ALTERNATING SCREENS
        min_humid = sys.argv[2]
        min_team = sys.argv[3]
        max_humid = sys.argv[4]
        max_team = sys.argv[5]
        avg_humid = sys.argv[6]
        
        # Screen 1: Min/Max with team numbers  
        # screen1_line1 = f"[2] Hmin:{min_humid}% [{min_team}]"[:16]
        # screen1_line2 = f"Hmax:{max_humid}% [{max_team}]"[:16]
        screen1_line1 = f"[2] H-:{min_humid}C ({min_team})"[:16]
        screen1_line2 = f"H+:{max_humid}C ({max_team})"[:16] 
        
        # Screen 2: Average
        screen2_line1 = f"[2] Hmoy:{avg_humid}%"[:16]
        screen2_line2 = ""
        
        # Alternate between screens
        display_alternating_screens(screen1_line1, screen1_line2, screen2_line1, screen2_line2, duration=5.0)
        
    elif mode == "weather" and len(sys.argv) >= 5:
        # Weather: temp, humidity, wind
        temp = sys.argv[2]
        humid = sys.argv[3]
        wind = sys.argv[4]
        display_text(f"[3] {temp}C  {humid}%", f"Wind: {wind}km/h")
        
    else:
        # Fallback - display raw text
        text = " ".join(sys.argv[1:])
        if len(text) <= 16:
            display_text(text, "")
        else:
            # Split long text intelligently
            mid = len(text) // 2
            split_point = mid
            for i in range(max(mid-8, 0), min(mid+8, len(text))):
                if i < len(text) and text[i] == ' ':
                    split_point = i
                    break
            display_text(text[:split_point], text[split_point+1:])

if __name__ == "__main__":
    main() 
