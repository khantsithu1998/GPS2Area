# GPS2Area

## Overview
This program calculates the area of a user-defined shape based on GPS coordinates (latitude and longitude). It utilizes various mathematical methods to estimate the area, including the Trapezoidal Rule, Shoelace Theorem, Spherical Polygon Method, and GIS-based calculations using the Shapely library. The results can be visualized in a plot and saved in GeoJSON format for further use.

## Features
- **User Input**: Allows users to input GPS coordinates interactively.
- **Area Calculation**: Computes the area using multiple methods:
  - Trapezoidal Rule
  - Shoelace Theorem
  - Spherical Polygon Method
  - GIS-based calculation using Shapely
- **Visualization**: Plots the shape and the enclosed area using Matplotlib.
- **GeoJSON Export**: Saves the shape as a GeoJSON file for easy sharing and integration with GIS applications.

## Requirements
To run this program, you need the following Python packages:
- `numpy`
- `scipy`
- `matplotlib`
- `shapely`
- `pyproj`

You can install the required packages using pip:
```bash
pip install numpy scipy matplotlib shapely pyproj
```

## Usage
1. Run the program:
   ```bash
   python main.py
   ```
2. Enter GPS coordinates in the format `latitude longitude`. Type `done` when you finish entering coordinates.
3. The program will calculate the area using the specified methods and display the results.
4. The shape will be plotted, and you will have the option to save the coordinates in a GeoJSON file.

## Example
```
📍 Enter GPS coordinates (latitude longitude). Type 'done' when finished.
Enter latitude and longitude (or 'done' to finish): 34.0522 -118.2437
Enter latitude and longitude (or 'done' to finish): 34.0522 -118.2537
Enter latitude and longitude (or 'done' to finish): 34.0622 -118.2537
Enter latitude and longitude (or 'done' to finish): done
```

## Output
The program will output the estimated areas calculated by each method and save the shape as a GeoJSON file. The plot will also be displayed.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- This program uses the `shapely` library for geometric operations and `pyproj` for coordinate transformations.
- Thanks to the contributors of the libraries used in this project.
