<div style="text-align: center;">

![Safe Journey Badge](Images/Safe%20Journey%20Badge%20Medium.jpg)
# Safe Journey

**Safe Journey**: Precision routing for maximum safety, leveraging advanced algorithms to determine the most secure path for users.
</div>


#

Safe Journey is a sophisticated routing program designed to prioritize user safety by determining the safest route to a given destination. Developed by Ori Bloch, this project combines a user-friendly interface, address validation, and a unique safety scoring algorithm to offer users a reliable and secure journey.

<div style="text-align: center;">
  <img src="Images/Step 4 Mapping Origin.png" alt="Safe Journey Map" />
</div>



## Features 🚀

- **User-Friendly Interface:** Safe Journey boasts an intuitive user interface that seamlessly captures user input for both origin and destination addresses.

- **Address Validation:** The program ensures accurate geolocation data by validating the entered addresses, contributing to the overall reliability of the routing process.

- **Route Calculation with Google Maps:** Utilizing the Google Maps API, Safe Journey calculates and analyzes multiple routes between the specified points.

- **Safety Scoring Algorithm:** Ori Bloch has devised an innovative algorithm that strategically creates midpoints along each route, assigning safety scores to evaluate the risk level at different locations. The cumulative scores aid in selecting the safest route available.

- **Interactive Map with Accident Data:** Safe Journey generates an interactive map showcasing accidents and color-coded route points to indicate safe and potentially dangerous locations.

- **URL Link Generation:** Upon selecting the safest route, the program generates a URL link for users to access and follow.
- **Map Generation:** Program produces a map highlighting dangerous driving points & accidents along the way.

## Limitations & Possible Improvements ⚠️

- **Computing Limitation:** Currently, Safe Journey is configured to operate exclusively in Colorado due to the vast dataset containing 7.7 million US accidents. Future adaptations for different states require adjustments in the accidents_backend using `data_selection_by_state`.

- **Scoring System Enhancement:** Considerations for further data manipulations may enhance the accuracy of the safety scoring system.

- **Google Maps API Limitation:** Note that the Google Maps API does not highlight the specific route. Prior to copying the link, the program provides guidance on the recommended route.

- **Efficiency Improvements:** Use Matrix Multiplication to better time run efficiency.


## Manual Guide 📖

1. **Get Your Google Maps API Key:**
   - Obtain a Google Maps API key and ensure proper configuration.

2. **Adjust Database for Different State:**
   - If using a state other than Colorado, modify accidents_backend using `data_selection_by_state` and reformat the data accordingly.

3. **Customize Front-End Settings:**
   - Redefine parameters in Front_end:
     - Number of route points for division (higher points for higher accuracy).
     - Number of accidents to consider (more accidents for higher accuracy).
     - Redefine the 'state' variable for the new state.

4. **Run the Program:**
   - Execute the program and follow on-screen instructions.

5. **Enter Origin and Destination Values:**
   - Input the origin and destination addresses, ensuring they include the state used in the program.


# Program Flow

##### [Watch Demo of the Program](#)

<div style="text-align: center;">

|                                                                                     |                                                                                       |
|-------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **Step 2:** Calculation                                                             | **Step 1:** Input                                                                     |
| Validations, routes creation and scoring algorithm                                          | User inputs: origin, destination addresses in Colorado                                            |
| <img src="Images/Step 2 Scoring Origin.png" alt="Step 1" width="200" height="150"/> | <img src="Images/Step 1 Calculating Origin.png" alt="Step 1" width="200" height="150"/> |

|                                                                                          |                                                                                     |
|------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| **Step 3:**                                                                              | **Step 4:** Map Creation                                                            |
| Google-Maps directions URL production for maps                          | Interactive map, highlighted route points & accidents                           |
| <img src="Images/Step 3 Instructions Origin.png" alt="Step 1" width="200" height="150"/> | <img src="Images/Step 4 Mapping Origin.png" alt="Step 1" width="200" height="150"/> |

</div>

# Dependencies

Make sure you have the following dependencies installed before running the project:

1. **pandas - data manipulation and analysis**
   - Documentation: [pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

2. **customtkinter - frontend add-on for tkinter**
   - Documentation: [customtkinter Documentation](https://pypi.org/project/customtkinter/0.3/)

3. **folium - map creation**
   - Documentation: [Folium Documentation](https://python-visualization.github.io/folium/)

4. **requests - HTTP requests**
   - Documentation: [Requests Documentation](https://docs.python-requests.org/en/latest/)

5. **geopy - geocoding and reverse geocoding**
   - Documentation: [Geopy Documentation](https://geopy.readthedocs.io/en/stable/)

5. **googlemaps - driving instructions**
   - Documentation: [GoogleMaps Documentation](https://developers.google.com/maps/documentation)

## Author 🧑‍💻

**Ori Bloch**
- Space Business Development Lead
- Electrical & Computer Engineering Student
- Algorithm Developer



- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Ori_Bloch-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ori-bloch-312768207/)
- [![GitHub](https://img.shields.io/badge/GitHub-Ori_Bloch-black?style=flat-square&logo=github)](https://github.com/OriBloch)
#

<div style="text-align: center;">
  <img src="Images/Safe Journey Badge Small.jpg" alt="Safe Journey Badge" />
</div>
