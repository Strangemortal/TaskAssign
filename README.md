# ✅ TaskAssign: A Simple Task Management System (Django Based)

A role-free, user-focused task assignment system built using Django and Bootstrap. Designed to streamline task tracking between admins and users with clean UI and easy interactions.

---

## 🚀 Features

### 👥 User Authentication

- 🔐 **User Registration**
  - Users can sign up with:
    - Username
    - Email
    - Password
- 🔓 **Login/Logout**
  - Secure session-based authentication.

---

### 👨‍💼 Admin Features

- 📝 **Create Tasks**
  - Admins can:
    - Create tasks with a title, description, and deadline.
    - Assign tasks to **specific users** via a dropdown menu.
    - Use a modern date-time picker (Flatpickr) to set deadlines.

- 📊 **View Task Status**
  - Admins can:
    - View task assignments.
    - Track status updates:
      - `Pending`
      - `In Progress`
      - `Completed`
    - See who submitted the task and when.
    - Accept or reject submitted tasks.
    - Leave feedback comments.

---

### 👤 User Features

- 📋 **View Assigned Tasks**
  - Users can:
    - See all tasks assigned to them.
    - View task details like title, description, deadline, and current status.

- ✍️ **Update Task Status**
  - Change task status to:
    - `Pending`
    - `In Progress`
    - `Completed`

- 🚀 **Submit for Review**
  - After marking a task as `Completed`, users can submit it for admin review.

- 💬 **Task Comments**
  - Users and admins can communicate via a comment section attached to each task.

- 🔁 **Edit Rejected Tasks**
  - Users can revise and resubmit tasks if rejected by the admin.

---

### 🎨 UI & Usability

- ✅ **Bootstrap 5 UI**
  - Responsive and styled interfaces for both admin and user dashboards.
  
- 📅 **Deadline Picker**
  - Integrated Flatpickr for clean deadline selection.

- 📢 **Alerts and Feedback**
  - Uses Bootstrap alerts to show status messages clearly (e.g., task created, submitted, rejected).

---

## 🧰 Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap 5), JavaScript
- **Database:** SQLite (default Django database)

---

## 💻 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Shttps://github.com/Strangemortal/TaskAssign.git
   cd TaskAssign
