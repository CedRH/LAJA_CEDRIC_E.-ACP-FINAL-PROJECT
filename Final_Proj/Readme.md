# EcoFind: Eco-Friendly Product Database 🌿

## Overview

EcoFind is a desktop application designed to help consumers discover, compare, and purchase eco-friendly products. The application provides a user-friendly interface to browse sustainable products, compare their environmental impact, and make informed purchasing decisions.

## Features

## LOG IN & REGISTER
- Register choosen username and create a strong password with "Special Characters, atleast one Capital letter and small letter, and should atleast 1 number.
- Log in the username and password that you registered at the register tab.
### Product Browsing
- View a comprehensive list of eco-friendly products
- Products categorized by type (Cleaning, Clothing, Electronics)
- Detailed product information including sustainability score and carbon footprint

### Search and Filter
- Search products by name, brand, or category
- Filter products by:
  - Product Category
  - Carbon Footprint (Low, Medium, High)

### Product Interaction
- View detailed product information
- Add products to comparison cart
- Add products to shopping cart
- Purchase eco-friendly products

## Technology Stack
- Python
- Tkinter (GUI)
- CustomTkinter (Modern UI Components)
- MySQL (Database)

## Prerequisites

### Software Requirements
- Python 3.x
- MySQL Server
- Required Python Libraries:
  - tkinter
  - customtkinter
  - mysql-connector-python

### Database Setup
1. Create a MySQL database named `ecofind_shpping`
2. Create a table `ecofnd_products` with columns:
   - name
   - brand
   - category
   - eco_certifications
   - carbon_footprint
   - recyclable_content
   - biodegradable
   - location
   - sustainability_score

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ecofind.git
cd ecofind
```

2. Install required libraries
```bash
pip install tkinter customtkinter mysql-connector-python
```

3. Configure database connection in the script
   - Update host
   - Update username
   - Update password

## Running the Application
```bash
python ecofind_app.py
```
## Future changes
- Can have a admin tab where you can add products.
- Implement advanced product lifecycle analysis.
- Add real-time carbon footprint calculation for product comparisons.
- Develop interactive data visualizations of environmental impact.
## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## Contact
- Email: 23-07564@g.batstate-u.edu.ph
- Contact No.: 09912183550