# Final_Project_NutriScan
Nutri-Scan web application using Google Vision API extract text from image of food labels.



Nutrition Score System 

In today's fast-paced world, packaged foods offer convenience, but they often pose health risks. Regulators aim to promote healthier choices, yet the food industry's pursuit of profit sometimes leads to opposition to regulations. The industry may exaggerate benefits or include unhealthy ingredients, creating conflict between public health goals and business interests. This highlights the need for strong regulations and consumer education to address health concerns associated with processed foods.

Nutrition Facts labels at the back of packaging provide essential details about packaged foods, such as serving size and nutrients. They assist consumers in making informed decisions regarding their dietary requirements. However the labels can be complex and time-consuming to read. 

The Nutri-Score is a simplified 5-color rating system (ranging from A to E) designed to aid consumers in easily comparing the nutritional quality of products. While many manufacturers display the Nutri-Score logo on their packaging to promote healthier choices, its universal adoption is still pending. It's important to understand that a low Nutri-Score grade doesn't necessarily imply a product is bad; rather, it indicates lower nutritional value or higher levels of saturated fats and salt. The Nutri-Score system serves as a convenient tool for consumers to make healthier choices, particularly in today's busy lifestyles, where understanding nutrition labels can be challenging.

How to calculate nutrition score

The Nutri-Score is calculated based on various nutritional factors, including energy (calories), sugars, saturated fats, sodium, protein, fiber, and the presence of fruits and vegetables. Each of these components contributes to the total score, which ranges from -15 to 40, with lower scores indicating better nutritional quality.
The final score is determined by subtracting the total positive points from the total negative points.


Web Application NutriScan

At the moment, not all manufacturers are willing to include Nutri-Score labels on their packaging.To bridge the gap and provide easier access to nutritional ratings, I offer a web application tool that allows users to scan images of food labels and receive instant Nutri-Scores. This live tool can be accessed from anywhere, enabling users to make informed decisions and opt for healthier choices

An overview of the project components:

1.	Google Vision API Integration: Utilize Google Vision API to process images of food labels and extract text information.

2.	Text Parsing and Nutri-Score Calculation: Develop Python functions to parse the extracted text and calculate Nutri-Scores based on standard rules.

3.	HTML/CSS Web Page: Create a user-friendly web page using HTML and CSS to display images and interact with the application.

4.	HTML Forms and Flask Integration: Implement HTML forms to take user input for the product name and save it to a file. Flask will handle routing, request handling, and template rendering for the front end, as well as server-side logic for the back end.

5.	Database or File Storage: Utilize a database or file storage system to save product names for future reference, saving users time during their next grocery trip.

By leveraging Python for backend logic, Flask for web server functionality, HTML/CSS for the frontend interface, and Google Cloud Vision API for image text extraction, the application can efficiently process food labels and provide Nutri-Scores to users, promoting healthier choices and facilitating informed decision-making.
