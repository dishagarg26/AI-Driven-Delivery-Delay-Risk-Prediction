import folium
from streamlit_folium import st_folium
import numpy as np

# Indian City Coordinates
CITY_COORDS = {
    'Mumbai': [19.0760, 72.8777],
    'Delhi': [28.7041, 77.1025],
    'Bangalore': [12.9716, 77.5946],
    'Hyderabad': [17.3850, 78.4867],
    'Chennai': [13.0827, 80.2707],
    'Kolkata': [22.5726, 88.3639],
    'Pune': [18.5204, 73.8567],
    'Ahmedabad': [23.0225, 72.5714],
    'Jaipur': [26.9124, 75.7873],
    'Lucknow': [26.8467, 80.9462]
}

def get_midpoint(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]

def create_route_map(source_city, dest_city, risk_score):
    """
    Creates a Folium map with a route between source and destination.
    risk_score: 0 (Low), 1 (Medium), 2 (High)
    """
    
    # Default to Mumbai-Delhi if not found
    src_coords = CITY_COORDS.get(source_city, CITY_COORDS['Mumbai'])
    dest_coords = CITY_COORDS.get(dest_city, CITY_COORDS['Delhi'])
    
    # Calculate center for map initialization
    midpoint = get_midpoint(src_coords, dest_coords)
    
    # determine zoom level based on distance (simplified)
    m = folium.Map(location=midpoint, zoom_start=5, tiles='CartoDB positron')
    
    # Risk Colors
    colors = {
        0: '#146EB4', # Low Risk (Amazon Blue) -> On Time
        1: '#FF9900', # Medium Risk (Amazon Orange) -> Delayed
        2: '#CC0000'  # High Risk (Red) -> At Risk
    }
    route_color = colors.get(risk_score, '#333333')
    
    # Add Source Marker
    folium.Marker(
        src_coords, 
        popup=f"Origin: {source_city}",
        icon=folium.Icon(color='blue', icon='cube', prefix='fa')
    ).add_to(m)
    
    # Add Destination Marker
    folium.Marker(
        dest_coords, 
        popup=f"Destination: {dest_city}",
        icon=folium.Icon(color='green', icon='user', prefix='fa')
    ).add_to(m)
    
    # Simulate a curved path or just straight line for now
    # Drawing a thick polyline
    folium.PolyLine(
        [src_coords, dest_coords],
        color=route_color,
        weight=4,
        opacity=0.8,
        tooltip=f"Route Risk Level: {['Low', 'Medium', 'High'][risk_score]}"
    ).add_to(m)
    
    # Add simulated "Traffic Congestion" circles along the route
    # Just creating 3 random points near the route for visual effect
    for _ in range(3):
        # Interpolate a point on the line
        t = np.random.uniform(0.2, 0.8)
        lat = src_coords[0] + t * (dest_coords[0] - src_coords[0]) + np.random.uniform(-0.5, 0.5)
        lon = src_coords[1] + t * (dest_coords[1] - src_coords[1]) + np.random.uniform(-0.5, 0.5)
        
        folium.Circle(
            location=[lat, lon],
            radius=40000, # 40km radius
            color='#FF0000',
            fill=True,
            fill_opacity=0.2,
            popup="High Traffic Zone"
        ).add_to(m)

    return m
