# Exam Manager Project

This project is designed for managing exam schedules, docimology sessions, and communication for teachers. It provides a comprehensive system to facilitate the organization and administration of exams and related activities.

## Project Structure

The project consists of the following main components:

- **exams**: Manages exam schedules, including exam dates, required teachers, and notifications.
- **docimology**: Handles docimology sessions, defining roles for teachers and session details.
- **communication**: Manages communication between administration and teachers, including sending messages and flash notifications.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd exam_manager
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```
   python manage.py migrate
   ```

5. **Run the development server**:
   ```
   python manage.py runserver
   ```

## Features

- **Exam Management**: Create, update, and view exam schedules.
- **Docimology Sessions**: Manage docimology sessions and roles for teachers.
- **Communication**: Send messages and notifications to teachers.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.

## License

This project is licensed under the MIT License. See the LICENSE file for details.