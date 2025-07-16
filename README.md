# 🚛 RathaHub 
**RathaHub** is a comprehensive web-based platform designed for transportation and logistics companies to efficiently manage their operations. Built with Django, it offers streamlined management of vehicles, drivers, customer requests, and live route tracking — all integrated into a single dashboard.

Whether you're a logistics firm, employee transportation provider, or private fleet operator, RathaHub helps organize daily transport workflows with visibility and automation.


## 🧩 Core Features

### 🧭 Operations Management
- 🛣️ **Route Mapping** using Google MapsAPI (source → destination)
- 🚚 **Vehicle Assignment** to transport tasks
- 👨‍✈️ **Driver Allocation** and tracking
- 📊 **Bookings Logs** and history per vehicle or driver
- 🔄 **Role-Based Dashboards** for Admins, Drivers, and Customers
  The system supports **multi-role access**, enabling:
- **Admins** to assign drivers, manage fleet, and monitor operations
- **Drivers** to view assigned tasks, report issues, and track routes
- **Customers** (if included) to view trip status and history'

- ### 💳 Payment Integration
- 💰 **Stripe Payment Gateway** integration

### 📂 Records & Dashboards
- 🚗 View number of **active vehicles**
- 👥 Track **available vs assigned drivers**
- 🗃️ Store and view **Booking history**
- 📈 Display route paths for audit and review
- 💾 Store booking/task data securely in the system

  ### 🛠 Vehicle Maintenance
- 🧾 **Issue Reporting** by drivers for vehicle-related problems
- 🔧 **Repair Tracking** and status updates by the admin
- 📅 **Maintenance history logs** per vehicle

### 🔐 Security & Reliability
- 🔐 API keys stored securely in `.env`
- 🧠 User role management (Driver / Admin / Customer
- 🔐 Secure payments with keys managed via `.env`

---

## 🔧 Tech Stack

| Component         | Technology                                 |
|------------------|---------------------------------------------|
| Frontend          | HTML, CSS, Bootstrap    |
| Backend           | Django, Django REST Framework(API)           |
| Mapping           | Google Maps Embed API, Directions API       |
| Data Storage      | SQLite (can upgrade to PostgreSQL/MySQL)    |
| Payment (optional)| Stripe API (can be integrated as needed)    |

---


## 📸 Screenshots


## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/Palgu09T4/RathaHub.git
cd RathaHub

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate     # On Linux/Mac: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create and configure .env file
touch .env
