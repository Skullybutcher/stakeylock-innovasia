import osmnx as ox
import folium
import streamlit as st
from streamlit.components.v1 import html

# Create the map with road network and traffic flow
def create_map():
    # Define a bounding box 
    north, south, east, west = 17.390, 17.380, 78.500, 78.470
    
    # Download the road network for the specified bounding box
    graph = ox.graph_from_bbox(north, south, east, west, network_type="all")

    # Convert the graph into a GeoDataFrame (edges represent roads)
    gdf_edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Create a Folium map 
    m = folium.Map(location=[17.385044, 78.486671], zoom_start=15)

    # Add roads to the map (color roads based on traffic status)
    for _, row in gdf_edges.iterrows():
        # Coordinates of the road (polyline)
        road_coords = [(lat, lon) for lat, lon in zip(row['geometry'].coords.xy[1], row['geometry'].coords.xy[0])]
        
        # Define traffic status 
        traffic_status = 'high'
    
        if traffic_status == 'high':
            color = 'red'
        elif traffic_status == 'medium':
            color = 'orange'
        else:
            color = 'green'

        # Polyline to represent the road with the respective color
        folium.PolyLine(road_coords, color=color, weight=5, opacity=0.7).add_to(m)

    return m

def main():
    st.title("Traffic Flow on Roads of JNTU, Hyderabad")

    # Create the map with road network and traffic flow
    m = create_map()

    # Embed the map in the Streamlit app
    map_html = m._repr_html_()  # Get the HTML representation of the map
    html(map_html, width=700, height=500)

if __name__ == "__main__":
    main()
