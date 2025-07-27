"""
Calculation utilities for Down Clock
"""

# Conversion factors for size units (to bytes)
SIZE_FACTORS = {
    "tb": 1024 ** 4,
    "gb": 1024 ** 3,
    "mb": 1024 ** 2,
    "kb": 1024,
    "b": 1
}

# Conversion factors for speed units (to bytes per second)
SPEED_FACTORS = {
    "gbit/s": (1024 ** 3) / 8,
    "mbit/s": (1024 ** 2) / 8,
    "kbit/s": 1024 / 8,
    "bit/s": 1 / 8,
    "mb/s": 1024 ** 2,
    "kb/s": 1024,
    "b/s": 1
}


def sizeToBytes(size, units):
    """
    Convert file size to bytes
    
    Args:
        size (float): The size value
        units (str): The unit (TB, GB, MB, KB, B)
    
    Returns:
        int: Size in bytes
    """
    units = units.lower()
    if units not in SIZE_FACTORS:
        raise ValueError(f"Unknown size unit: {units}")
    return size * SIZE_FACTORS[units]


def speedToBytes(speed, units):
    """
    Convert speed to bytes per second
    
    Args:
        speed (float): The speed value
        units (str): The unit (GBit/s, MBit/s, KBit/s, Bit/s, MB/s, KB/s, B/s)
    
    Returns:
        float: Speed in bytes per second
    """
    units = units.lower()
    if units not in SPEED_FACTORS:
        raise ValueError(f"Unknown speed unit: {units}")
    return speed * SPEED_FACTORS[units]


def calculateDownloadTime(size, sizeUnit, speed, speedUnit):
    """
    Calculate download time in hours
    
    Args:
        size (float): File size
        sizeUnit (str): Size unit
        speed (float): Download speed
        speedUnit (str): Speed unit
    
    Returns:
        float: Download time in hours
    """
    sizeInBytes = sizeToBytes(size, sizeUnit)
    speedInBytes = speedToBytes(speed, speedUnit)
    return sizeInBytes / speedInBytes / 3600


def formatDownloadTime(time_hours):
    """
    Format download time into a human-readable string
    
    Args:
        time_hours (float): Time in hours
    
    Returns:
        str: Formatted time string
    """
    days = int(time_hours // 24)
    hours = int(time_hours % 24)
    minutes = int((time_hours * 60) % 60)
    seconds = int((time_hours * 3600) % 60)
    
    if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
        return "<div style='text-align: center;'><span style='color: #4ade80; font-size: 16px;'><b>⚡ Download Time</b></span><br><span style='color: #4ade80; font-size: 14px;'>Less than a second</span></div>"
    else:
        # Determine color based on total time
        if time_hours < 1/3600:  # Less than 1 second
            color = "#4ade80"  # Light green
        elif time_hours < 1/60:  # Less than 1 minute
            color = "#60a5fa"  # Light blue
        elif time_hours < 1:  # Less than 1 hour
            color = "#fbbf24"  # Light yellow
        else:
            color = "#f87171"  # Light red
        
        time_parts = []
        if days > 0:
            time_parts.append(f"{days} days")
        if hours > 0 or days > 0:  # Show hours if there are days or hours
            time_parts.append(f"{hours} hours")
        if minutes > 0 or hours > 0 or days > 0:  # Show minutes if there are larger units
            time_parts.append(f"{minutes} minutes")
        if seconds > 0 or minutes > 0 or hours > 0 or days > 0:  # Show seconds if there are larger units
            time_parts.append(f"{seconds} seconds")
        
        time_text = "<br>".join(time_parts)
        
        return f"<div style='text-align: center;'><span style='color: {color}; font-size: 16px;'><b>⏱️ Download Time</b></span><br><span style='color: {color}; font-size: 14px;'>{time_text}</span></div>" 