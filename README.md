<div align="center">
  <img src="./templates/assets/cravengers.png" alt="Cravengers Logo"/>
</div>

## About

<p align="justify">   CRAVENGERS is a gamified web-based food ordering application where cravings meet challenges, turning every meal into an adventure. Users can order their favorite dishes, earn streaks, collect rewards, and level up their foodie journey. Developed using Python (Flask), SQL, HTML, JavaScript, and CSS, Cravengers features two main modules that enhance both user experience and administrative efficiency. The Customer Module allows users to browse menus, place orders, and track their progress through a series of interactive, gamified challenges. On the other hand, the Admin Module enables seamless management of menus, order handling, and real-time monitoring of user activity. Whether you're aiming to unlock your next food badge or simply searching for a tasty bite, Cravengers invites you to assemble your cravings and embark on the ultimate foodie quest. </p>

## Purpose

A project for [COMP010] Information Management under Sir. Espineli.

## Features

<p align="justify"> The application is built with a modular architecture, consisting of a Customer Module and an Admin Module, both securely connected to a robust SQL-based backend protected from SQL injection through the use of parameterized queries and ORM practices. </p>

🔹 Customer Module (User Side)

      Browse and Order Food
         - Users can explore store menus, view product details, and place customized orders.
      
      Cancel Active Orders
         - Allows users to cancel pending or unprocessed orders with a single click.
      
      Track and View Orders
         - Displays a chronological list of active and past orders with status updates.
      
      Gamified Streak & Reward System
         - Users collect streaks for consecutive orders, earn vouchers, and unlock food-themed achievements.
      
      Voucher Redemption
         - Apply percentage-based discounts to orders using valid, unexpired vouchers.
      
      Real-time Price Adjustment
         - Instantly reflects voucher discounts on the order summary before confirmation.

🔸 Admin Module (Manager Side)

      View All Orders
         - Admins can view and filter all user orders by status, date, or customer.
      
      Cancel or Finalize Orders
         - Approve, complete, or cancel orders directly from the admin panel.
      
      Top-Up User Wallets
         - Safely credit user accounts with balance through validated admin actions.
      
      Manage Store Menus
         - Add, edit, or remove products tied to specific stores. Includes product images and pricing.
      
      Order Filtering & Sorting
         - Powerful order management tools to sort by time, amount, or customer.

## Techstack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Installation

      1. Clone the repository:
         ```bash
         git clone <repository-url>
         cd Cravengers
         ```
      2. Install dependencies:
         ```bash
         pip install -r requirements.txt
         ```
      3. Set up the database as required.

## Usage

   ```bash
   python appy.py
   ```

## Contributors

- Bagui, Shayne Marie D.
- Bautista, Danielle Eizy R.
- Coronacion, Mikylla Joy R.
- Francisco, Cian Jake F.
