![Cravengers Logo](./templates/assets/cravengers.png)

# Cravengers: Online Food Ordering System

## About

CRAVENGERS is a gamified web-based food ordering application where cravings meet challenges, turning every meal into an adventure. Users can order their favorite dishes, earn streaks, collect rewards, and level up their foodie journey. Developed using Python (Flask), SQL, HTML, JavaScript, and CSS, Cravengers features two main modules that enhance both user experience and administrative efficiency. The Customer Module allows users to browse menus, place orders, and track their progress through a series of interactive, gamified challenges. On the other hand, the Admin Module enables seamless management of menus, order handling, and real-time monitoring of user activity. Whether you're aiming to unlock your next food badge or simply searching for a tasty bite, Cravengers invites you to assemble your cravings and embark on the ultimate foodie quest.

## Purpose

A project for [COMP010] Information Management under Sir. Espineli.

## Features

The application is built with a modular architecture, consisting of a Customer Module and an Admin Module, both securely connected to a robust SQL-based backend protected from SQL injection through the use of parameterized queries and ORM practices.

🔹 Customer Module (User Side)
Browse and Order Food

Users can explore store menus, view product details, and place customized orders.

Cancel Active Orders

Allows users to cancel pending or unprocessed orders with a single click.

Track and View Orders

Displays a chronological list of active and past orders with status updates.

Gamified Streak & Reward System

Users collect streaks for consecutive orders, earn vouchers, and unlock food-themed achievements.

Voucher Redemption

Apply percentage-based discounts to orders using valid, unexpired vouchers.

Real-time Price Adjustment

Instantly reflects voucher discounts on the order summary before confirmation.

🔸 Admin Module (Manager Side)
View All Orders

Admins can view and filter all user orders by status, date, or customer.

Cancel or Finalize Orders

Approve, complete, or cancel orders directly from the admin panel.

Top-Up User Wallets

Safely credit user accounts with balance through validated admin actions.

Manage Store Menus

Add, edit, or remove products tied to specific stores. Includes product images and pricing.

Order Filtering & Sorting

Powerful order management tools to sort by time, amount, or customer.

Security Integration

Prevents SQL injection via parameterized queries and strict input validation.

Live Dashboard

Real-time activity monitoring and performance overview of the platform.


## Techstack

- Python (Flask)
- SQL (SQLite/MySQL)
- HTML
- CSS
- JavaScript

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

- Bautista, Danielle Eizy
- Bagui, Shayne
- Coronacion, Mikylla
- Francisco, Cian Jake
